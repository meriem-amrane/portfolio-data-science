import pandas as pd
import numpy as no
import seaborn 
from sqlalchemy import create_engine



df= pd.read_csv('data\olist_dataset.csv')

def clean_df(df):
   
    # Create a copy to avoid modifying the original dataframe
    df_clean = df.copy()
     
    print("----- Starting data cleaning process -----")
    
    #Data Conversions
    
     # 1. Convert date columns to datetime
    print("\n1. Converting date columns...")
    date_columns = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date',
        'review_creation_date',
        'review_answer_timestamp',
        'shipping_limit_date'
    ]
    
    for col in date_columns:
        df_clean[col] = pd.to_datetime(df_clean[col] )
        
    # 2. Handling missing values
    print('\n2. Handling missing values')
    
    #For numerical data
    numerical_columns = df_clean.select_dtypes(include=['float64','int64']).columns
    
    for col in numerical_columns:
        if df_clean[col].isnull().sum() >0 :
            median_value = df_clean[col].median()
            df_clean[col].fillna(median_value,inplace=True)
            print(f"Filled missing values in {col} with median: {median_value}")
    
    #for categorical data
    categorical_columns = df_clean.select_dtypes(include = ['object']).columns
    for col in categorical_columns:
        if df_clean[col].isnull().sum()>0:
            mode_value = df_clean[col].mode()[0]
            df_clean[col].fillna(mode_value,inplace=True)
            print(f"Filled missing values in {col} with mode: {mode_value}")
    
    # 3. Handling outliers in numerical columns 
    print('\n3. Handling outliers in numerical columns')
    for col in numerical_columns:
        if col not in ['order_id', 'customer_id', 'seller_id', 'product_id','review_id','order_item_id']:  
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
        # Count outliers
            outliers = ((df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)).sum()
            if outliers > 0:
                print(f"Found {outliers} outliers in {col}")
                # Cap outliers
                df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
        
        
        # 4. Clean string columns
    print("\n4. Cleaning string columns...")
    for col in categorical_columns:
        if df_clean[col].dtype == 'object':
            # Convert to lowercase
            df_clean[col] = df_clean[col].str.lower()
            # Remove extra whitespace
            df_clean[col] = df_clean[col].str.strip()
            # Replace multiple spaces with single space
            df_clean[col] = df_clean[col].str.replace('\s+', ' ', regex=True)
    
    # 5. Remove duplicates
    print("\n5. Removing duplicates...")
    initial_rows = len(df_clean)
    df_clean.drop_duplicates(inplace=True)
    final_rows = len(df_clean)
    if initial_rows != final_rows:
        print(f"Removed {initial_rows - final_rows} duplicate rows")
    
    
     # 6. Create new features
    print("\n6. Creating new features...")
    
    # Calculate delivery time in days
    df_clean['delivery_time_days'] = (df_clean['order_delivered_customer_date'] - 
                                    df_clean['order_purchase_timestamp']).dt.days
    
    # Calculate if delivery was late
    df_clean['is_late_delivery'] = df_clean['delivery_time_days'] > (
        df_clean['order_estimated_delivery_date'] - 
        df_clean['order_purchase_timestamp']
    ).dt.days
    
    # Calculate total order value
    df_clean['total_order_value'] = df_clean['price'] + df_clean['freight_value']
    
    # Extract date components
    df_clean['purchase_year'] = df_clean['order_purchase_timestamp'].dt.year
    df_clean['purchase_month'] = df_clean['order_purchase_timestamp'].dt.month
    df_clean['purchase_day'] = df_clean['order_purchase_timestamp'].dt.day
    df_clean['purchase_hour'] = df_clean['order_purchase_timestamp'].dt.hour
    
    print("\nData cleaning completed!")
        

    
    return df_clean

clean_df(df).to_csv("transformed_data.csv", index=False)