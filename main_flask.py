
#import packages

from flask import Flask,json
import os
import sql_connector as sc
import feature_wrangling as fw
import training_model as train
import model_prediction as mp


#set the current working directory
os.chdir("//home//projects//....//Historical_prediction//")


#This function calls methods 
#to wrangle data, train our models and predict.
#it reads and writes data to SQL Database


def prediction_main():
    try:
        #read properties file, get other filepaths
        config_Path = 'filepath.properties'
        propList = fw.read_properties_file(config_Path)
        filepath = propList['filepath']
        model_path = propList['model_path']
        #call to sql to get training data
        try:
            training_df = sc.sql_fetch_train_data()
	#massage your data as needed - rename, drop etc.
	#Complete guide on feature analysis covered separately.
            training_df = training_df.rename(columns={"transaction_date": "date"})
            training_df = training_df.sort_values(['Product_name','date'])
            training_df = training_df.reset_index()
            training_df.drop('index',axis=1,inplace=True)
	#drop a message - helps to debug
            msg = "Fetched Training Data from Database"
            print(msg)
        except:
            msg = "Error while fetching Training Data from Database"
            print(msg)
        
        #modify the values of Weather,Holiday and Festival fields       
        try:
            training_df = fw.handle_categorical_fields(training_df)
            training_df['holiday']=training_df.holiday.astype(int)
            training_df['festival']=training_df.festival.astype(int)
            msg = "Modified categorical fields on Training Data"
            print(msg)
        except:
            msg = "Error while performing data modifications on Training Data"
            print(msg)
            
        #adding features required for training the model
	#date field details will be utilized in detail in a timeseries example.
        try:
            training_df = fw.adding_features_dataframe(training_df)
            msg = "Added features to Training Data"
            print(msg)
        except:
            msg = "Error while adding date features on Training Data"
            print(msg)    

        #In reality, we will need different data fit different models.Just to demostrate:
	#model1 is rain related items and model2 is sun related. 
	#though these products have a cross appicability     
        model_1 = ['Raincoat','Rainpant','ShellJacket']
        model_2 = ['Sweatshirt','Umbrella','Hat']
        #complete list of ancillaries
        all_products = ['Raincoat','Rainpant','ShellJacket','Sweatshirt','Umbrella','Hat']           

        #call training model - trained by Decision Tree
        for i in model_1:
            try:
                product_name = i       
                model_name = 'DecisionTree'
                msg = train.training_model(training_df,product_name,model_path,model_name)
                #msg = "Completed training %s product" % product_name
                print(msg)
            except:
                msg = "Error while training %s product" % product_name
                print(msg)

        #call training model trained by XGboost Tree
	for i in model_2		
            try:
		product_name = i
                model_name = 'XGBoost'
                msg = train.training_model(training_df,product_name,model_path,model_name)
                #msg = "Completed training %s product" % product_name
                print(msg)
            except:
                msg = "Error while training %s product" % product_name
                print(msg)

        #call to sql to get test data
	#Typically this data will be refreshed latest
	#And the older data is pushed to the train set 
	#(assuming Incremental training is not set up)
        try:
            rep_df = sc.sql_fetch_test_data()
            rep_df = rep_df.sort_values(['date'])
            rep_df = rep_df.reset_index()
            rep_df.drop('index',axis=1,inplace=True)
            msg = "Fetched Test Data from Database"
            print(msg)
        except:
            msg = "Error while fetching Test Data from Database"
            print(msg)
            
        #modify the values of weather,holiday and festival fields
        try:
            rep_df = fw.handle_categorical_fields(rep_df)
            rep_df['weather']=rep_df.weather.astype(int)
            rep_df['holiday']=rep_df.holiday.astype(int)
            rep_df['festival']=rep_df.festival.astype(int)
        except:
            msg = "Error while performing data modifications on Test Data"
            print(msg)
        #add features to Test data    
        try:
            rep_df = fw.adding_features_dataframe(rep_df)
            msg = "Added features to Test Data"
            print(msg)
        except:
            msg = "Error while adding features on Training Data"
            print(msg)
            
        
        # call Sale prediction code
        for i in all_ancillaries:
            try:
                product_name = i
                pred_sales_df = mp.model_predict_sales(training_df,product_name,filepath,rep_df,model_path)
                msg = "Predicted sales of %s product" % product_name
                print(msg)
            except:
                msg = "Error while predicting sales of %s" % product_name
                print(msg)

            #insert the predicted record in database
            try:
                sc.insert_predictions(pred_sales_df)
            except:
                msg = "Error while inserting predicted data of %s product into Database" % product_name
                print(msg)
            
               			
        msg = "Completed"
        print(msg)
        """
        response = app.response_class(
            response=json.dumps(msg),
            status=200,
            mimetype='application/json'
        )
        return response
        """
    except:
        msg = "Error!!!!"
        print(msg)
        """
        response = app.response_class(
            response=json.dumps(msg),
            status=500,
            mimetype='application/json'
        )
        return response
