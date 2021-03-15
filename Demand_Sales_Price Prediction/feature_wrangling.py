
#import packages
import io
import os
import configparser as cp
import pandas as pd

#only minimal data concepts are demonstrated here. 
#There is a separate folder for data concepts. 
#that covers- Feature analysis, Outlier treatment, feature reduction, PCA etc.

#this functionality is used to get the details from config file
def read_properties_file(file_path):
    with open(file_path) as f:
        config = io.StringIO()
        config.write('[dummy_section]\n')
        config.write(f.read().replace('%', '%%'))
        config.seek(0, os.SEEK_SET)
        cp1 = cp.ConfigParser()
        cp1.read_file(config)
        return dict(cp1.items('dummy_section'))
    
#this functionality is used to modify categorical fields
def handle_categorical_fields(data_mod_df):	
    for i in range(len(data_mod_df)):
        data_mod_df.loc[i:i,'weather']=strings_to_numbers((str(data_mod_df['weather'][i])).lower())
        data_mod_df.loc[i:i,'holiday'][i]=strings_to_numbers((str(data_mod_df['holiday'][i])).lower())
        data_mod_df.loc[i:i,'festival'][i]=strings_to_numbers((str(data_mod_df['festival'][i])).lower())
    return data_mod_df
        
    
# Function to convert number into string 
# Switcher is dictionary data type here
# While numbering you may also weight the numbers helps sometimes
# in this set the numbers are increasing with tendency to buy a coat.
def strings_to_numbers(argument): 
    switcher = { 
        "sunny": 100, 
        "cloudy": 200, 
        "drizzle": 250,
        "rain": 300,
        "fog": 500,
        "snow": 600,
        "none": 0
    } 
  
# get() method of dictionary data type returns  
# value of passed argument if it is present  
# in dictionary otherwise second argument will 
# be assigned as default value of passed argument 
    return switcher.get(argument, 1) 

#Date is a important field in continous data treatment. 
#this function is called when we need to prepare the dataset for
#either training or predicting demand
def adding_features_dataframe(data_mod_df):
    #preparing dataset for training  
    data_mod_df['date'] = pd.to_datetime(data_mod_df['date'])
    data_mod_df['year'] = data_mod_df['date'].dt.year
    data_mod_df['month'] = data_mod_df['date'].dt.month
    data_mod_df['day'] = data_mod_df['date'].dt.day
    data_mod_df['week'] = data_mod_df['date'].dt.week
    data_mod_df['weekofyear'] = data_mod_df['date'].dt.weekofyear
    data_mod_df['dayofweek'] = data_mod_df['date'].dt.dayofweek
    data_mod_df['weekday'] = data_mod_df['date'].dt.weekday
    data_mod_df['dayofyear'] = data_mod_df['date'].dt.dayofyear
    data_mod_df['quarter'] = data_mod_df['date'].dt.quarter
    data_mod_df['is_month_start'] = data_mod_df['date'].dt.is_month_start
    data_mod_df['is_month_end'] = data_mod_df['date'].dt.is_month_end
    data_mod_df['is_quarter_start'] = data_mod_df['date'].dt.is_quarter_start
    data_mod_df['is_quarter_end'] = data_mod_df['date'].dt.is_quarter_end
    data_mod_df['is_year_start'] = data_mod_df['date'].dt.is_year_start
    data_mod_df['is_year_end'] = data_mod_df['date'].dt.is_year_end
    
    
    categorical_var = ['is_month_start', 'is_month_end', 'is_quarter_start', 'is_quarter_end', 'is_year_start', 
                      'is_year_start', 'is_year_end']
    
    for var in categorical_var:
        data_mod_df[var] = data_mod_df[var].astype('category')
        
    data_mod_df[categorical_var] = data_mod_df[categorical_var].apply(lambda x: x.cat.codes)
    
    return data_mod_df
        
        
        