import psycopg2
from psycopg2 import Error


def updateTable(Datenbank, Daten):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="0705Rapha!",
                                      host="localhost",
                                      port="5432",
                                      database="Novaland")

        # Erstellen einen Cursor, welche für die Datenbanken Operationen zuständig ist
        cursor = connection.cursor()

        cursor.callproc()

        # Stellt die Postgres Details da
        print("PostgresSQL server Informationen")
        print(connection.get_dsn_parameters(), "\n")

        cursor.execute("SELECT version();")

        record = cursor.fetchone()
        print("Du bist verbunden mit - ", record, "\n")

    except(Exception, Error) as error:
        print("Fehler beim verbinden mit dem PostgresSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("Die PostgresSQL Verbindung ist geschlossen.")
