# -*- coding: utf8 -*-

"""
This module provides the needed tools to execute the basic CRUD operations
on a sqlite database (Insert, update, delete, load all elements, load
elements from a pk, load rows from a given condition...).
"""

import config
import sqlite3
import registry


class Model(object):
	"""
	This is the base class.
	If a model class has to use it, it must extends it.
	From this point, the table associated to the class will be the module name,
	the table's primary key will be id_<module-name>
	"""

	_db = None

	#public:
	@staticmethod
	def fetchAllRows(query, params={}):
		"""
		c.fetchAllRows(query, params) -> list()

		Returns all the rows of the given query with the given parameters.

		@param query string Sql query to execute
		@param params dict the query's parameters

		@return list the result of the query, will be a list of dict, and
			an empty list if there's no result.
		"""

		Model.connect()
		c = Model._db.cursor()
		result = []
		currentRow = {}
		nbCols = 0
		c.execute(query, list(params))

		#~ Get the columns names
		column_names = [d[0] for d in c.description]
		result = c.fetchall()
		resultList = list()
		for r in result:
			resultList.append(Model._createRow(r, column_names))

		Model._db.close()
		return resultList

	@staticmethod
	def fetchOneRow(query, params={}):
		"""
		c.fetchOneRow(query, params) -> dict()

		Returns the first row of the given query with the given parameters.

		@param query string Sql query to execute
		@param params dict the query's parameters

		@return dict the result of the query, will be a dict, and
			an empty dict if there's no result.
		"""

		Model.connect()
		c = Model._db.cursor()
		result = dict()
		nbCols = 0
		c.execute(query, params)
		r = c.fetchone()

		#~ Get the colums names
		column_names = [d[0] for d in c.description]
		if r is not None:
			result = Model._createRow(r, column_names)

		Model._db.close()
		return result

	@classmethod
	def save(cls, fields, where=list()):
		"""
		c.save(fields, where)

		Save a row in the database.
		If the where parameter is not null, an update will be executed, else
		the row will be inserted.

		@param fields dict of fields with as keys the table's fields and as
			values, the row's values.
		@param where tuple with as first element the SQL where and as second
			element the where's params
		"""

		#~ insert
		if len(where) == 0:
			cls.insert(fields)
		else:  # update
			cls.update(fields, where)

	@classmethod
	def insert(cls, fields):
		"""
		Insert a new row in the database
		"""
		Model.connect()
		c = Model._db.cursor()

		fields = cls.filterFields(fields)
		fieldsNames = list(map(lambda x: '"' + x + '"', fields.keys()))
		values = ['?'] * len(fieldsNames)

		query = "INSERT INTO %s (%s) VALUES (%s)" % (
			cls.__module__, ','.join(fieldsNames), ','.join(values)
		)

		c.execute(query, list(fields.values()))
		Model._db.commit()
		Model._db.close()

		return c.lastrowid

	@classmethod
	def update(cls, fields, where):
		Model.connect()
		c = Model._db.cursor()

		fields = cls.filterFields(fields)
		fieldsNames = map(lambda x: '"' + x + '" = ?', fields.keys())

		query = "UPDATE %(table)s SET %(values)s WHERE %(where)s" %\
			{'table': cls.__module__, 'values': ','.join(fieldsNames), 'where': where[0]}
		c.execute(query, list(fields.values()) + where[1])
		Model._db.commit()
		Model._db.close()

	@classmethod
	def delete(cls, where):
		Model.connect()
		c = Model._db.cursor()

		query = "DELETE FROM %(table)s WHERE %(where)s" %\
			{'table': cls.__module__, 'where': where[0]}
		r = c.execute(query, where[1])
		Model._db.commit()
		Model._db.close()
		return r

	@staticmethod
	def connect():
		Model._db = sqlite3.connect(registry.get("world"))


	@staticmethod
	def _createRow(sqliteRow, columns):
		row = {}
		for i, v in enumerate(sqliteRow):
			row[columns[i]] = v

		return row

	@classmethod
	def loadAll(cls, fields=None):
		fields = cls.prepareFieldsForSelect(fields)

		query = "\
			SELECT\
				%(fields)s\
			FROM\
				%(table)s\
		" % {'fields': fields, 'table': cls.__module__}

		return Model.fetchAllRows(query, {})

	@classmethod
	def loadById(cls, id, fields=None):
		fields = cls.prepareFieldsForSelect(fields)

		table = cls.__module__
		query = "\
			SELECT\
				%(fields)s\
			FROM\
				%(table)s\
			WHERE\
				%(where)s\
		" % {'fields': fields, 'table': table, 'where': 'id_' + table + ' = ?'}

		return Model.fetchOneRow(query, [id])

	@classmethod
	def loadBy(cls, filters, fields=None):
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
			'table': cls.__module__,
			'where': ' AND '.join(filtersNames)
		}

		return Model.fetchAllRows(query, filters.values())

	@classmethod
	def prepareFieldsForSelect(cls, fields=None):
		if not fields:
			fields = cls.fields

		if isinstance(fields, list) or isinstance(fields, tuple):
			fields = ', '.join(fields)
		elif isinstance(fields, dict):
			fields = ', '.join(map(lambda x: fields[x] + ' AS ' + x, fields))
		elif not isinstance(fields, basestring):
			raise TypeError('Unexpected type of fields (%s)' % type(fields))

		return fields

	@classmethod
	def filterFields(cls, fields):
		return dict((k, fields[k]) for k in cls.fields if k in fields)
