# -*- coding: utf8 -*-

import config
import sqlite3


class Model(object):
	_db = None

	#public:
	@staticmethod
	def fetchAllRows(query, params):
		Model._connect()
		c = Model._db.cursor()
		result = []
		currentRow = {}
		nbCols = 0
		c.execute(query, params)

		#~ Get the columns names
		column_names = [d[0] for d in c.description]
		result = c.fetchall()
		resultList = list()
		for r in result:
			resultList.append(Model._createRow(r, column_names))

		return resultList

	@staticmethod
	def fetchOneRow(query, params):
		Model._connect()
		c = Model._db.cursor()
		result = dict()
		nbCols = 0
		c.execute(query, params)
		r = c.fetchone()

		#~ Get the colums names
		column_names = [d[0] for d in c.description]
		if r is not None:
			result = Model._createRow(r, column_names)

		return result

	@classmethod
	def save(cls, fields, where=list()):
		#~ insert
		if len(where) == 0:
			cls.insert(fields)
		else:  # update
			cls.update(fields, where)

	@classmethod
	def insert(cls, fields):
		Model._connect()
		c = Model._db.cursor()

		fields = cls.filterFields(fields)
		fieldsNames = map(lambda x: '"' + x + '"', fields.keys())
		values = ['?'] * len(fieldsNames)

		query = "INSERT INTO %s (%s) VALUES (%s)" % (
			cls.__module__, ','.join(fieldsNames), ','.join(values)
		)

		c.execute(query, fields.values())
		Model._db.commit()

		return c.lastrowid

	@classmethod
	def update(cls, fields, where):
		Model._connect()
		c = Model._db.cursor()

		fields = cls.filterFields(fields)
		fieldsNames = map(lambda x: '"' + x + '" = ?', fields.keys())

		query = "UPDATE %s SET %s WHERE %s" %\
			(cls.__module__, ','.join(fieldsNames), where[0])
		c.execute(query, fields.values() + where[1])
		Model._db.commit()

	#protected:
	@staticmethod
	def _connect():
		if Model._db is None:
			Model._db = sqlite3.connect(config.db)

		return True

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

		if isinstance(fields, list):
			fields = ', '.join(fields)
		elif isinstance(fields, dict):
			fields = ', '.join(map(lambda x: fields[x] + ' AS ' + x, fields))
		elif not isinstance(fields, basestring):
			raise TypeError('Unexpected type of fields (%s)' % type(fields))

		return fields

	@classmethod
	def filterFields(cls, fields):
		return dict((k, fields[k]) for k in cls.fields if k in fields)
