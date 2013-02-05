# -*- coding: utf8 -*-

import config, sqlite3

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
        return c.fetchall()

    @staticmethod
    def fetchOneRow(query, params):
        Model._connect()
        c = Model._db.cursor()
        result = list()
        nbCols = 0
        c.execute(query, params)
        r = c.fetchone()
        if r != None:
            result = Model._createRow(r)

        return result

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


    #protected:
    @staticmethod
    def _connect():
        if Model._db == None:
            Model._db = sqlite3.connect(config.db)

        return True

    @staticmethod
    def _createRow(sqliteRow, nbCols = None):
        if nbCols == 0:
            nbCols = len(sqliteRow)

        row = {}
        for i, v in enumerate(sqliteRow):
            row[i] = v

        return row


