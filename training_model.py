
#import required packages
import xgboost as xgb
import pickle
from sklearn import tree
import os

#this function selects the appropriate model for training
#Hyper parameters need to be adjusted specific to your case

def get_train_model(model_name):
    if model_name == 'DecisionTree':
        model = tree.DecisionTreeRegressor()
    elif model_name == 'XGBoost':
        model = xgb.XGBRegressor(objective ='reg:linear', 
                          learning_rate =0.1,
                          n_estimators=28,
                          max_depth=3,
                          min_child_weight=3,
                          gamma=0,
                          subsample=0.83,
                          colsample_bytree=0.62,
                          nthread=3,
                          scale_pos_weight=1,
                          reg_alpha=0.02,
                          seed=34,
                          )
						  
        
    return model

    
#function for training the product to predict sales
def training_model(training_df,Product_name,model_path,model_name):
    try:
        msg = "Error in training %s Product" % Product_name
        #make a list of features required for training the model
        selected_columns = ['Raincoat','Rainpant','ShellJacket','Sweatshirt','Umbrella','Hat'] 
        
        #select the respective products from the training dataframe  
        Product = training_df.loc[training_df['Product_name'] == Product_name]
        Product = Product.reset_index()
        Product.drop('index',axis=1,inplace=True)
    
        train_new = Product[Product['sales'].notnull()]
        #features which are used for training        
        X = train_new[selected_columns]
        #output variable
        y = train_new['sales']

        #get the respective training model
        model = get_train_model(model_name)
        model.fit(X, y)
    
        #filename to save the trained model    
        file_name = model_path + "model_" + product_name + ".pkl"

        #if the file exists, delete it	
        if os.path.exists(file_name):
            os.remove   
        #save the trained model
        pickle.dump(model, open(file_name, "wb"))
        msg = "Completed training %s Product" % Product_name
        return msg
    except:
        msg="Error in training"
        return msg
    

    