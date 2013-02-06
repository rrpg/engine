# -*- coding: utf8 -*-

from Model import Model


class GenderModel:
    @staticmethod
    def getGenders():
        genders = []

        query = "\
            SELECT\
                id_gender,\
                name\
            FROM\
                gender\
        "

        results = Model.fetchAllRows(query, {})
        for v in results:
            genders.append({
                'id': v[0],
                'name': str(v[1])
            })

        return genders
