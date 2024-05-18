import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filepath):
    # Load data from CSV
    df = pd.read_csv(filepath)
    
    return df

def hypothesis_1(df):
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])

    df['Transaction Hour'] = df['Transaction Date'].dt.hour

    df['Is Fraudulent'] = df['Is Fraudulent'].apply(lambda x: True if x == 1 else False)

    fraud_counts = df.groupby('Transaction Hour')['Is Fraudulent'].sum()

    
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

def save_processed_data(data, filepath):
    data.to_csv(filepath, index=False) 

def main():
    data_filepath = 'backend\dataset\Fraudulent_E-Commerce_Transaction_Data.csv'
    data = load_data(data_filepath)

    hypothesis_2(data)
    
if __name__ == "__main__":
    main()
