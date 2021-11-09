

# ATENTION! First install dependencies (example for Linux): 
# sudo apt install python3-dev libpq-dev
# pip install psycopg2

# Error handling took from: https://kb.objectrocket.com/postgresql/python-error-handling-with-the-psycopg2-postgresql-adapter-645
# Error handling must be improved, not working with queries

import psycopg2
from psycopg2 import OperationalError, errorcodes, errors



class POSTGRE_DB_FETCH_JSON_TIMESERIES:

    def __init__(self):
        self.conn = None
        self.cursor = None
        
    def schedule(self, event_name, event_value,
                 host, port, user, password, dbname,
                 table_name, values):

        if event_name == 'INIT':    
            
            # catch exception for invalid SQL connection
            try:
                # declare a new PostgreSQL connection object
                self.conn = psycopg2.connect(dbname=dbname, 
                    user=user, 
                    password=password,
                    host="localhost",
                    port="5432")
                self.cursor = self.conn.cursor()

            except OperationalError as err:
                print(err)

                # set the connection to 'None' in case of error
                self.conn = None

            finally:
                return [event_value, None]

        elif event_name == 'RUN':
            if self.conn != None:
                # values must be a string with the exact number of values the table has
                # values must be separated by "," and appropriately formated, do not forget to escape \" strings         
                query = """SELECT * FROM {0} WHERE {0}.timestamp {1});""".format(table_name,values)
                print(query)
                
                # catch exception for invalid SQL statement#
                try:
                    self.cursor.execute(query)
                    self.conn.commit()

                except Exception as err:
                    print(err)

                    # rollback the previous transaction before starting another
                    self.conn.rollback()

                finally:
                    # self.cursor.close()
                    # self.conn.close()
                    return [None, event_value]
            else:
                print("No active connection to PostgreSQL DB.")
                return [event_value, None]