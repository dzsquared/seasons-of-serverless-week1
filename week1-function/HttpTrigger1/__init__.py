import logging
import pyodbc
import json
import os
import time
import azure.functions as func

# Driver={ODBC Driver 13 for SQL Server};Server=tcp:serverless-fun.database.windows.net,1433;Database=serverless1;Uid=sqladmin;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # 'DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password
    sqlConnectionString = os.environ["serverlessdb"]
    turkeySize = 0
    messages = []
    statusCode = 200
    ingredients = []

    try:
        turkeySize = float(req.params.get('turkey'))
        logging.info(str(turkeySize))
    except:
        messages.append('Use the query string "turkey" to send a turkey weight.')
        return generateHttpResponse(ingredients, messages, 400)

    try:
        ingredients = getIngredients(sqlConnectionString, turkeySize)
    except pyodbc.DatabaseError:
        time.sleep(45)
        ingredients = getIngredients(sqlConnectionString, turkeySize)
        messages.append('Thanks for waithing, the database had to be started.')

    return generateHttpResponse(ingredients, messages, statusCode)

def generateHttpResponse(ingredients, messages, statusCode):
    return func.HttpResponse(
        json.dumps({"Messages": messages, "Ingredients": ingredients}, sort_keys=True, indent=4),
        status_code=statusCode
    )


def getIngredients(sqlConnectionString, turkeySize):
    logging.info('contacting DB')
    results = []
    sqlConnection = pyodbc.connect(sqlConnectionString)
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute('EXEC calculateRecipe '+str(turkeySize))
    columns = [column[0] for column in sqlCursor.description]
    for row in sqlCursor.fetchall():
        results.append(dict(zip(columns, row)))
    return results