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
		result = list()
		nbCols = 0
		c.execute(query, params)
		r = c.fetchone()

		#~ Get the colums names
		column_names = [d[0] for d in c.description]
		if r is not None:
			result = Model._createRow(r, column_names)

		return result

	@staticmethod
	def save(table, fields, where=list()):
		#~ insert
		if len(where) == 0:
			Model.insert(table, fields)
		else:  # update
			Model.insert(table, update)

	@staticmethod
	def insert(table, fields):
		Model._connect()
		c = Model._db.cursor()

		query = "INSERT INTO " + table

		nbFields = len(fields)
		current = 0
		fieldsStr = ''
		valuesStr = ''

		for k, v in fields.items():
			fieldsStr += '"' + k + '"'
			valuesStr += '?'
			if current < nbFields - 1:
				fieldsStr += ', '
				valuesStr += ', '
			current += 1

		query = query + " (" + fieldsStr + ") VALUES (" + valuesStr + ")"

		c.execute(query, fields.values())
		Model._db.commit()

		return c.lastrowid

	@staticmethod
	def update(table, fields, where):
		Model._connect()
		c = Model._db.cursor()

		nbFields = len(fields)
		current = 0
		fieldsStr = ''

		params = list()
		for k, v in fields.items():
			fieldsStr += '"' + k + '" = ?'
			params.append(v)
			if current < nbFields - 1:
				fieldsStr += ', '
			current += 1

		query = "UPDATE %s SET %s WHERE %s" % (table, fieldsStr, where[0])
		c.execute(query, params + where[1])
		Model._db.commit()

		return c.lastrowid

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
