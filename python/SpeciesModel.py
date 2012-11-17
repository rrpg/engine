# -*- coding: utf8 -*-

from Model import Model

class SpeciesModel:
    @staticmethod
    def getSpecies(gender):
        species = []

        query = "\
            SELECT\
                id_species,\
                ";
        if gender == "male":
            query += "name_m,"
        else:
            query += "name_f,"

        query += "\
                description\
            FROM\
                species\
        "

        results = Model.fetchAllRows(query, {})
        for v in results:
            species.append({
                'id': v[0],
                'name': str(v[1]),
                'description': str(v[2])
            })

        return species

