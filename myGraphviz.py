

import sqlite3
from sqlite3 import Error
from graphviz import Graph
from graphviz import Digraph

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def actividadReservada(conn,dot):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM ActividadReservada")

    rows = cur.fetchall()
    with dot.subgraph(name='clusterActividadReservada') as c:
        c.attr(style='filled', color='lightgrey')
        c.attr(label='Actividad Reservada')
        c.attr('node', shape='rectangle',style='filled', color='w')
        for row in rows:
            #print(row)
            c.node('A'+str(row[0]).encode("utf-8","ignore"), row[1].encode("utf-8","ignore"))

def competeciaEspecifica(conn,dot):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM competeciaEspecifica")

    rows = cur.fetchall()
    with dot.subgraph(name='clusterCompeteciaEspecifica') as c:
        c.attr(color='blue')
        c.attr(label='Competencia Especificas')

        for row in rows:
            #print(row)
            c.node('E'+str(row[0]).encode("utf-8","ignore"), row[1].encode("utf-8","ignore"))


def CONFEDISubCapacidades(conn,dot):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM CONFEDISubCapacidades")

    rows = cur.fetchall()
    with dot.subgraph(name='clusterCONFEDISubCapacidades') as c:
        c.attr(color='red')
        c.attr(label='CONFEDI SubCapacidades')

        for row in rows:
            #print(row)
            c.node('sC'+str(row[0]).encode("utf-8","ignore")+"."+str(row[1]).encode("utf-8","ignore")+"."+str(row[2]).encode("utf-8","ignore"), row[3].encode("utf-8","ignore"))





def relacionCompEspConSubCapacidad(conn,dot):
    sql = "SELECT  ce.id as idCE, \
                ce.Nombre as competenciaEspecifica, \
                csc.idComGen as ComGen,  \
                csc.idCap as Cap, \
                csc.IdSubCap as subCap, \
                cc.Nombre as SubCapacidad \
            FROM competeciaEspecifica ce  \
            JOIN CEvSubCapacidad csc  \
                ON csc.idCE  = ce.id  \
            JOIN CONFEDISubCapacidades cc \
                ON cc.idCapGen = csc.idComGen AND csc.idCap = cc.idCap AND csc.IdSubCap = cc.id  "
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()
    for row in rows:
            #print(row)
            dot.edge('E'+str(row[0]).encode("utf-8","ignore"),  
                     'sC'+str(row[2]).encode("utf-8","ignore")+"."+str(row[3]).encode("utf-8","ignore")+"."+str(row[4]).encode("utf-8","ignore"))
            #c.node('E'+str(row[0]).encode("utf-8","ignore"), row[1].encode("utf-8","ignore"))



def relacionesActividadCompetencia(conn,dot):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM RelacionActividadCompetencia")

    rows = cur.fetchall()

    for row in rows:
        #print(row)
        dot.edge('A'+str(row[1]), 'E'+str(row[0]))


def main():
    database = "prueba.db"
    dot = Digraph('G', filename='relaciones.gv', comment='Relaciones')
    dot.graph_attr['rankdir'] = 'LR'
    # create a database connection
    conn = create_connection(database)
    with conn:
    
        #print("2. Query all tasks")
        actividadReservada(conn,dot)
        competeciaEspecifica(conn,dot)
        CONFEDISubCapacidades(conn,dot)
        relacionesActividadCompetencia(conn,dot)
        relacionCompEspConSubCapacidad(conn,dot)
        

    
    #dot.node('A', 'King Arthur')
    #dot.node('B', 'Sir Bedevere the Wise')
    #dot.node('L', 'Sir Lancelot the Brave')

    #dot.edges(['AB', 'AL'])

    #dot.view()
    print(dot.source)

if __name__ == '__main__':
    main()