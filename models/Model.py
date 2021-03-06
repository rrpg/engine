# -*- coding: utf-8 -*-

"""
This module provides the needed tools to execute the basic CRUD operations
on a sqlite database (Insert, update, delete, load all elements, load
elements from a pk, load rows from a given condition...).
"""

from core import config
import sqlite3


class Model(object):
	"""
	This is the base class.
	If a model class has to use it, it must extends it.
	From this point, the table associated to the class will be the module name,
	the table's primary key will be id_<module-name>
	"""

	_table = None

	_defaultDB = None

	@classmethod
	def getClass(cls):
		return cls.__module__.split('.').pop()

	#public:
	@classmethod
	def fetchAllRows(cls, query, params={}, db=None):
		"""
		c.fetchAllRows(query, params) -> list()

		Returns all the rows of the given query with the given parameters.

		@param query string Sql query to execute
		@param params dict the query's parameters
		@param db string path to the sqlite db to use

		@return list the result of the query, will be a list of dict, and
			an empty list if there's no result.
		"""

		db = cls.connect(db)
		c = db.cursor()
		result = []
		currentRow = {}
		nbCols = 0
		c.execute(query, list(params))

		#~ Get the columns names
		column_names = [d[0] for d in c.description]
		result = c.fetchall()
		resultList = list()
		for r in result:
			resultList.append(cls._createRow(r, column_names))

		db.close()
		return resultList

	@classmethod
	def fetchOneRow(cls, query, params={},db=None):
		"""
		c.fetchOneRow(query, params) -> dict()

		Returns the first row of the given query with the given parameters.

		@param query string Sql query to execute
		@param params dict the query's parameters
		@param db string path to the sqlite db to use

		@return dict the result of the query, will be a dict, and
			an empty dict if there's no result.
		"""

		db = cls.connect(db)
		c = db.cursor()
		result = dict()
		nbCols = 0
		c.execute(query, params)
		r = c.fetchone()

		#~ Get the colums names
		column_names = [d[0] for d in c.description]
		if r is not None:
			result = cls._createRow(r, column_names)

		db.close()
		return result

	@classmethod
	def insert(cls, fields, db=None):
		"""
		Insert a new row in the database
		"""
		db = cls.connect(db)
		c = db.cursor()

		fields = cls.filterFields(fields)
		fieldsNames = list(map(lambda x: '"' + x + '"', fields.keys()))
		values = ['?'] * len(fieldsNames)
		query = "INSERT INTO %s (%s) VALUES (%s)" % (
			cls.getClass(), ','.join(fieldsNames), ','.join(values)
		)

		c.execute(query, list(fields.values()))
		cls.disconnect(db)

		return c.lastrowid

	@classmethod
	def update(cls, fields, where, db=None):
		db = cls.connect(db)
		c = db.cursor()

		fields = cls.filterFields(fields)
		fieldsNames = map(lambda x: '"' + x + '" = ?', fields.keys())

		query = "UPDATE %(table)s SET %(values)s WHERE %(where)s" %\
			{'table': cls.getClass(), 'values': ','.join(fieldsNames), 'where': where[0]}
		c.execute(query, list(fields.values()) + where[1])
		cls.disconnect(db)

	@classmethod
	def delete(cls, where, db=None):
		db = cls.connect(db)
		c = db.cursor()

		query = "DELETE FROM %(table)s WHERE %(where)s" %\
			{'table': cls.getClass(), 'where': where[0]}
		c.execute(query, where[1])
		cls.disconnect(db)

	@classmethod
	def connect(cls, db=None):
		if db is None:
			db = cls._defaultDB
		db = sqlite3.connect(db)
		db.text_factory = str
		return db

	@classmethod
	def setDB(cls, db):
		cls._defaultDB = db

	@classmethod
	def getDB(cls):
		return cls._defaultDB

	@classmethod
	def disconnect(cls, db):
		db.commit()
		db.close()

	@staticmethod
	def _createRow(sqliteRow, columns):
		row = {}
		for i, v in enumerate(sqliteRow):
			row[columns[i]] = v

		return row

	@classmethod
	def loadAll(cls, fields=None, db=None):
		fields = cls.prepareFieldsForSelect(fields)

		query = "\
			SELECT\
				%(fields)s\
			FROM\
				%(table)s\
		" % {'fields': fields, 'table': cls.getClass()}

		return cls.fetchAllRows(query, db=db)

	@classmethod
	def loadById(cls, id, fields=None, db=None):
		fields = cls.prepareFieldsForSelect(fields)

		table = cls.getClass()
		query = "\
			SELECT\
				%(fields)s\
			FROM\
				%(table)s\
			WHERE\
				%(where)s\
		" % {'fields': fields, 'table': table, 'where': 'id_' + table + ' = ?'}

		return cls.fetchOneRow(query, [id], db)

	@classmethod
	def loadBy(cls, filters, fields=None, db=None):
		fields = cls.prepareFieldsForSelect(fields)

		filters = cls.filterFields(filters)
		filtersNames = map(lambda x: '"' + x + '" = ?', filters.keys())

		query = "\
			SELECT\
				%(fields)s\
			FROM\
				%(table)s\
			WHERE\
				%(where)s\
		" % {
			'fields': fields,
			'table': cls.getClass(),
			'where': ' AND '.join(filtersNames)
		}

		return cls.fetchAllRows(query, filters.values(), db=db)

	@classmethod
	def prepareFieldsForSelect(cls, fields=None):
		if not fields:
			fields = cls.fields

		if isinstance(fields, list) or isinstance(fields, tuple):
			fields = ', '.join(fields)
		elif isinstance(fields, dict):
			fields = ', '.join(map(lambda x: fields[x] + ' AS ' + x, fields))
		elif not isinstance(fields, str):
			raise TypeError('Unexpected type of fields (%s)' % type(fields))

		return fields

	@classmethod
	def filterFields(cls, fields):
		return dict((k, fields[k]) for k in cls.fields if k in fields)

	@classmethod
	def executeQuery(cls, cursor, query, params):
		cursor.execute(query, params)
