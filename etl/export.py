################################################################################
##                                  LIBRARIES                                 ##
################################################################################

################
##  EXTERNAL  ##
################

import psycopg2
import pandas as pd
import os


################################################################################
##                                  CONSTANTS                                 ##
################################################################################

SQL_FOLDER = os.path.join('sql')
DATA_FOLDER = os.path.join("data")


################################################################################
##                                  FUNCTIONS                                 ##
################################################################################

def export_data(db_params:dict):
    # Establish a database connection
    conn = psycopg2.connect(**db_params)


    for filename in os.listdir(SQL_FOLDER):
        if filename.endswith('.sql'):
            with open(os.path.join(SQL_FOLDER, filename), 'r') as sql_file:
                sql_query = sql_file.read()

                # Execute the SQL query
                cursor = conn.cursor()
                cursor.execute(sql_query)

                # Fetch query results
                results = cursor.fetchall()
                cursor.close()

                # Export results to CSV
                csv_filename = os.path.splitext(filename)[0] + '.csv'
                csv_path = os.path.join(DATA_FOLDER, csv_filename)
                df = pd.DataFrame(results, columns=[desc[0] for desc in cursor.description])
                df.to_csv(csv_path, index=False)

    # Close the database connection
    conn.close()