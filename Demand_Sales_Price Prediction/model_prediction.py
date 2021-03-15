
#import packages
import pandas as pd
import pickle


#functionality to predict the demand of a product
def model_predict_demand(training_df,product_name,filepath,rep_df,model_path):
    
    #load the training data in another dataframe
    df_1 = training_df.copy()
    product = df_1.loc[df_1['product_name'] == product_name]
    product = product.reset_index()
    product.drop('index', axis=1, inplace=True)
    product_category = product['product_category'][0]
    
    #find the start and end date for new predictions    
    start_date = df_1['date'].max()
    start_date = start_date.to_pydatetime()
    start_date = start_date + pd.DateOffset(days=1)
    end_date = df_1['date'].max()
    end_date = end_date.to_pydatetime()
    end_date = end_date + pd.DateOffset(months=3)  
    
    #using the start date and end date
    #get the index positions
    #from the repository dataframe 
    for i in range(len(rep_df)):
        if start_date == rep_df['date'][i]:
            start_index = i
        if end_date == rep_df['date'][i]:
            end_index = i + 1
        
    #prepate the future predicted dataframe    
    future_df = rep_df.filter(['date'],axis=1)  
    future_df = future_df[start_index:end_index]

    #list of selected columns required to make predictions 
    selected_columns = ['Raincoat','Rainpant','ShellJacket','Sweatshirt','Umbrella','Hat'] 

    #prepare data for prediction
    data_predicted = rep_df[selected_columns]
    data_predicted = data_predicted[start_index:end_index]
  
    # load the trained model
    file_name = model_path + "model_" + ancillary_name + ".pkl"
    model_loaded = pickle.load(open(file_name, "rb"))
    
    #start prediction
    predict1 = model_loaded.predict(data_predicted)

    #rounding off the predicted value    
    predicted_value = []
    for i in range(len(predict1)):
        t = round(predict1[i])
        predicted_value.append(t)

    #complete the future predicted dataframe
    future_df.insert(1, 'product_category', product_category)
    future_df.insert(2, 'product_name', product_name)
    future_df.insert(3, 'predicted_sale', predicted_value)
    future_df = future_df.rename(columns={"date": "future_date"})
    future_df = future_df.reset_index()
    future_df.drop('index',axis=1,inplace=True)

    return future_df
    
    
    
    
    