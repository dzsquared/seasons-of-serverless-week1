import logging
import pyodbc
import json
import os
import azure.functions as func

# Driver={ODBC Driver 13 for SQL Server};Server=tcp:serverless-fun.database.windows.net,1433;Database=serverless1;Uid=sqladmin;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
    sqlConnectionString = os.environ["serverlessdb"]
    sqlConnection = pyodbc.connect(sqlConnectionString)
    sqlCursor = sqlConnection.cursor()

    turkeySize = req.params.get('turkey')

    sqlCursor.execute('EXEC calculateRecipe '+turkeySize)

    columns = [column[0] for column in sqlCursor.description]

    results = []
    for row in sqlCursor.fetchall():
        results.append(dict(zip(columns, row)))

    output = {"Ingredients": results}

    return func.HttpResponse(
        json.dumps(output, sort_keys=True, indent=4),
        status_code=200
    )
