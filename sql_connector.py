
#import packages
import mysql.connector
import pandas as pd
import json
from sqlalchemy import create_engine

#read the db_settions json file in order to establish sql connection
with open("db_settings.json") as jsonfile:
    db_data = json.load(jsonfile)

db_user = db_data['user']
db_pwd = db_data['password']
db_host = db_data['host']
db_port = db_data['port']
db_name = db_data['database']
    
# Connecting to mysql by providing a sqlachemy engine
engine = create_engine('mysql+mysqlconnector://'+db_user+':'+db_pwd+'@'+db_host+':'+db_port+'/'+db_name, echo=False)

#function to fetch training data
def sql_fetch_train_data():
    try:
        sql_query = "select * from training_data"
        with engine.begin() as conn:
            result = conn.execute(sql_query)
            training_data = result.fetchall()
        training_df = pd.DataFrame(training_data)
        training_df.columns = training_data[0].keys()
        print ("Training records fetched successfully")
    except mysql.connector.Error as error :
        print ("Failed to fetch records from MySQL training_data table {}".format(error))

    return training_df

#function to fetch repository data
def sql_fetch_test_data():
    try:
        sql_query = "select * from test_data"
        with engine.begin() as conn:
            result = conn.execute(sql_query)
            rep_data = result.fetchall() 
        rep_df = pd.DataFrame(rep_data)
        rep_df.columns = rep_data[0].keys()
        print ("Repository records fetched successfully")
    except mysql.connector.Error as error :
        print ("Failed to fetch records from MySQL repository table {}".format(error))

    return rep_df


#function to fetch product data
def get_product_data():
    try:
        sql_query = "select * from product_data"
        with engine.begin() as conn:
            result = conn.execute(sql_query)
            ancillary_data = result.fetchall() 
        product_data_df = pd.DataFrame(product_data)
        product_data_df.columns = product_data[0].keys()
        print ("Product records fetched successfully")
    except mysql.connector.Error as error :
        print ("Failed to fetch records from MySQL product_data table {}".format(error))

    return Product_data_df   

        
        
