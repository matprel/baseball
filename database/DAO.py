from database.DB_connect import DBConnect
from model.salarioS import SalarioS
from model.squadra import Squadra


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllSquadre():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query ="""  select *
                    from teams t 
                    where t.year >= 1980
                    """
        cursor.execute(query)

        for row in cursor:
            result.append(Squadra(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalari(anno, idMap):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT t.teamCode , t.ID , sum(s.salary) as totSalary
                    FROM salaries s , teams t , appearances a 
                    WHERE s.`year` = t.`year` and t.`year` = a.`year` 
                    and a.`year` = %s
                    and t.ID = a.teamID 
                    and s.playerID = a.playerID 
                    GROUP by t.teamCode"""
        cursor.execute(query, (anno,))

        for row in cursor:
            result[idMap[row["ID"]]] = row["totSalary"]
        cursor.close()
        conn.close()
        return result
