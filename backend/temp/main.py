import pandas as pd
import math

def load_data(filepath):
    df = pd.read_csv(filepath)
    
    return df

def hypothesis_1(df):
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])

    # Extract hour, month, and year
    df['Transaction Hour'] = df['Transaction Date'].dt.hour
    df['Transaction Month'] = df['Transaction Date'].dt.month
    df['Transaction Year'] = df['Transaction Date'].dt.year

    # Ensure 'Is Fraudulent' is boolean
    df['Is Fraudulent'] = df['Is Fraudulent'].apply(lambda x: True if x == 1 else False)

    # Group by hour, month, and year and calculate fraud counts
    fraud_counts_hour = df.groupby('Transaction Hour')['Is Fraudulent'].sum().reset_index()
    fraud_counts_month = df.groupby('Transaction Month')['Is Fraudulent'].sum().reset_index()
    fraud_counts_year = df.groupby('Transaction Year')['Is Fraudulent'].sum().reset_index()
    
    
    # Prepare results in JSON format
    result_json = {
        "Fraudulent Transactions by Hour": fraud_counts_hour.to_dict(orient='records'),
        "Fraudulent Transactions by Month": fraud_counts_month.to_dict(orient='records'),
        "Fraudulent Transactions by Year": fraud_counts_year.to_dict(orient='records')
    }

    print(result_json)
    return result_json

    
#Newer customer accounts are more likely to commit fraud. (Account Age Day and Fraud Count)
#Elaboration: The older or the newer account (90 days ? )
def hypothesis_2(df):
    df['Account Age Days'] = pd.to_numeric(df['Account Age Days'], errors='coerce')

    df['Is Fraudulent'] = df['Is Fraudulent'].apply(lambda x: True if x == 1 else False)

    df['Account Age Category'] = pd.cut(df['Account Age Days'], bins=[-float('inf'), 90, float('inf')], labels=['New', 'Old'])

    fraud_counts = df.groupby('Account Age Category')['Is Fraudulent'].sum().reset_index()

    result_json = fraud_counts.to_json(orient='records')
    print(result_json)
    return result_json

def hypothesis_3(df):
    df['Is Fraudulent'] = df['Is Fraudulent'].apply(lambda x: True if x == 1 else False)
    
    q3 = df['Transaction Amount'].quantile(0.75)
    
    high_value_transactions = df[df['Transaction Amount'] > q3]
    
    fraud_count = high_value_transactions['Is Fraudulent'].sum()
    non_fraud_count = high_value_transactions.shape[0] - fraud_count
    
    result = [
        {"High Value Trnasaction(Q3)": q3},
        {"Is Fraudulent": False, "Transaction Count": non_fraud_count},
        {"Is Fraudulent": True, "Transaction Count": fraud_count}
    ]
    
    result_json = pd.Series(result).to_json(orient='records')
    print(result_json)
    return result_json

def hypothesis_4(df):
    df['Is Fraudulent'] = df['Is Fraudulent'].apply(lambda x: True if x == 1 else False)
    
    high_quantity_threshold = df['Quantity'].quantile(0.75)
    
    high_quantity_transactions = df[df['Quantity'] > high_quantity_threshold]
    
    fraud_count = high_quantity_transactions['Is Fraudulent'].sum()
    non_fraud_count = high_quantity_transactions.shape[0] - fraud_count
    
    result = [
        {"Is Fraudulent": False, "Transaction Count": non_fraud_count},
        {"Is Fraudulent": True, "Transaction Count": fraud_count}
    ]
    
    result_json = pd.Series(result).to_json(orient='records')
    print(result_json)
    return result_json

def hypothesis_5(df):
    df['Is Fraudulent'] = df['Is Fraudulent'].apply(lambda x: True if x == 1 else False)
    
    fraud_counts = df.groupby('Payment Method')['Is Fraudulent'].sum().reset_index()
    total_counts = df['Payment Method'].value_counts().reset_index()
    total_counts.columns = ['Payment Method', 'Total Transactions']
    
    fraud_rates = pd.merge(fraud_counts, total_counts, on='Payment Method')
    
    fraud_rates['Fraud Rate'] = fraud_rates['Is Fraudulent'] / fraud_rates['Total Transactions']
    

    result_json = fraud_rates.to_json(orient='records')
    print(result_json)
    return result_json

def hypothesis_6(df):
    df['Is Fraudulent'] = df['Is Fraudulent'].apply(lambda x: True if x == 1 else False)
    
    fraud_counts = df.groupby('Customer Location')['Is Fraudulent'].sum().reset_index()
    total_counts = df['Customer Location'].value_counts().reset_index()
    total_counts.columns = ['Customer Location', 'Total Transactions']
    
    fraud_rates = pd.merge(fraud_counts, total_counts, on='Customer Location')
    
    fraud_rates['Fraud Rate'] = fraud_rates['Is Fraudulent'] / fraud_rates['Total Transactions']

    result_json = fraud_rates.to_json(orient='records')
    print(result_json)
    return result_json

def hypothesis_7(df):
    df['Is Fraudulent'] = df['Is Fraudulent'].apply(lambda x: True if x == 1 else False)
    
    fraud_counts = df.groupby('Device Used')['Is Fraudulent'].sum().reset_index()
    total_counts = df['Device Used'].value_counts().reset_index()
    total_counts.columns = ['Device Used', 'Total Transactions']
    
    fraud_rates = pd.merge(fraud_counts, total_counts, on='Device Used')
    
    fraud_rates['Fraud Rate'] = fraud_rates['Is Fraudulent'] / fraud_rates['Total Transactions']
    
    result_json = fraud_rates.to_json(orient='records')
    print(result_json)
    return result_json

def hypothesis_8(df, starting_age=18, interval=5):
    df['Is Fraudulent'] = df['Is Fraudulent'].apply(lambda x: True if x == 1 else False)
    
    # Group by age group and calculate fraud counts
    def get_age_group(age):
        age_group_start = starting_age + math.floor((age - starting_age) / interval) * interval
        age_group_end = age_group_start + interval - 1
        return f"{age_group_start} - {age_group_end}"
    
    df['Age Group'] = df['Customer Age'].apply(get_age_group)
    fraud_counts = df.groupby('Age Group')['Is Fraudulent'].sum().reset_index()
    
    most_scam_age_group = fraud_counts.loc[fraud_counts['Is Fraudulent'].idxmax()]
    
    result = {
        "Age Group": most_scam_age_group['Age Group'],
        "Fraudulent Transaction Count": int(most_scam_age_group['Is Fraudulent'])
    }

    result_json = pd.Series(result).to_json()

    print(result_json)
    return result_json

def save_processed_data(data, filepath):
    data.to_csv(filepath, index=False) 

def main():
    data_filepath = 'backend\dataset\Fraudulent_E-Commerce_Transaction_Data.csv'
    data = load_data(data_filepath)

    hypothesis_5(data)
    
if __name__ == "__main__":
    main()
