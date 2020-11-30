import logging
import pyodbc
import json
import os
import time
import azure.functions as func

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
        messages.append('Use the query string "turkey" to send a turkey weight in lbs.')
        return generateHttpResponse(ingredients, messages, 400)

    try:
        sqlConnection = getSqlConnection(sqlConnectionString)
        ingredients = getIngredients(sqlConnection, turkeySize)
    except pyodbc.DatabaseError:
        messages.append('Unable to connect to the database, please try again later.')
        statusCode=500

    return generateHttpResponse(ingredients, messages, statusCode)

def generateHttpResponse(ingredients, messages, statusCode):
    return func.HttpResponse(
        json.dumps({"Messages": messages, "Ingredients": ingredients}, sort_keys=True, indent=4),
        status_code=statusCode
    )

def getSqlConnection(sqlConnectionString):
    i = 0
    while i < 6:
        logging.info('contacting DB')
        try:
            sqlConnection = pyodbc.connect(sqlConnectionString)
        except pyodbc.DatabaseError:
            time.sleep(10) # wait 10s before retry
            i+=1
        else:
            return sqlConnection
    raise pyodbc.DatabaseError('Failed to connect after retries')

def getIngredients(sqlConnection, turkeySize):
    logging.info('getting ingredients')
    results = []
    sqlCursor = sqlConnection.cursor()
    sqlCursor.execute('EXEC calculateRecipe '+str(turkeySize))
    results = json.loads(sqlCursor.fetchone()[0])
    sqlCursor.close()
    return results