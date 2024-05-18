from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from .country import countries

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

dataset_filepath = 'dataset/Fraudulent_E-Commerce_Transaction_Data.csv'
dataset = pd.read_csv(dataset_filepath)

hypo1 = None
hypo2 = None
hypo3 = None
hypo4 = None
hypo5 = None
hypo6 = None
hypo7 = None
hypo8 = None
hypo9 = None
basic_analysis_result = None

@app.get("/")
async def root():
    return {"message": "Hello Triple K"}


@app.get("/hypothesis_1")
async def hypothesis_1():
    global hypo1
    if hypo1 is None:
        hypo1 = analyse_fraudulent_transaction(dataset)
    return hypo1

@app.get("/hypothesis_2")
async def hypothesis_2():
    global hypo2
    if hypo2 is None:
        hypo2 = analyse_account_day(dataset)
    return hypo2

@app.get("/hypothesis_3")
async def hypothesis_3():
    global hypo3
    if hypo3 is None:
        hypo3 = analyse_transaction_amount(dataset)
    return hypo3

@app.get("/hypothesis_4")
async def hypothesis_4():
    global hypo4
    if hypo4 is None:
        hypo4 = analyse_product_quantity(dataset)
    return hypo4

@app.get("/hypothesis_5")
async def hypothesis_5():
    global hypo5
    if hypo5 is None:
        hypo5 = analyse_payment_method(dataset)
    return hypo5


@app.get("/hypothesis_6")
async def hypothesis_6():
    global hypo6
    if hypo6 is None:
        hypo6 = analyse_location(dataset)
    return hypo6


@app.get("/hypothesis_7")
async def hypothesis_7():
    global hypo7
    if hypo7 is None:
        hypo7 = analyse_device_used(dataset)
    return hypo7


@app.get("/hypothesis_8")
async def hypothesis_8():
    global hypo8
    if hypo8 is None:
        hypo8 = analyse_most_scam_age_group(dataset)
    return hypo8


@app.get("/hypothesis_9")
async def hypothesis_9():
    global hypo9
    if hypo9 is None:
        hypo9 = analyse_by_product_category(dataset)
    return hypo9

@app.get("/basic_analysis")
async def basic_analysis():
    global basic_analysis_result
    if basic_analysis_result is None:
        basic_analysis_result = {
            "total_transaction": len(dataset), 
            "total_fraudulent": count_total_fraudulent(dataset), 
            "total_fraudulent_amount": count_total_fraudulent_amount(dataset),
            "fraudulent_rate": round(count_total_fraudulent(dataset) / len(dataset) * 100, 3)
        }
    return basic_analysis_result


def count_total_fraudulent(dataset):
    count: int = 0
    for i in range(len(dataset)):
        if dataset.iloc[i]['Is Fraudulent'] == 1:
            count += 1
    return count


def count_total_fraudulent_amount(dataset):
    total_fraudulent_amount: float = 0
    for i in range(len(dataset)):
        if dataset.iloc[i]['Is Fraudulent'] == 1:
            total_fraudulent_amount += dataset.iloc[i]['Transaction Amount']
    return round(total_fraudulent_amount, 2)


def analyse_fraudulent_transaction(dataset):
    dataset['Transaction Date'] = pd.to_datetime(dataset['Transaction Date'])

    dataset['Transaction Hour'] = dataset['Transaction Date'].dt.hour
    dataset['Transaction Month'] = dataset['Transaction Date'].dt.month
    dataset['Transaction Year'] = dataset['Transaction Date'].dt.year

    dataset['Is Fraudulent'] = dataset['Is Fraudulent'].apply(lambda x: True if x == 1 else False)

    fraud_counts_hour = dataset.groupby('Transaction Hour')['Is Fraudulent'].sum().reset_index()
    fraud_counts_month = dataset.groupby('Transaction Month')['Is Fraudulent'].sum().reset_index()
    fraud_counts_year = dataset.groupby('Transaction Year')['Is Fraudulent'].sum().reset_index()
    
    result = {
        "Fraudulent Transactions by Hour": fraud_counts_hour.to_dict(orient='records'),
        "Fraudulent Transactions by Month": fraud_counts_month.to_dict(orient='records'),
        "Fraudulent Transactions by Year": fraud_counts_year.to_dict(orient='records')
    }

    global hypo1
    hypo1 = result

    return result

def analyse_account_day(dataset):
    dataset['Account Age Days'] = pd.to_numeric(dataset['Account Age Days'], errors='coerce')

    dataset['Is Fraudulent'] = dataset['Is Fraudulent'].apply(lambda x: 1 if x == 1 else 0)  # Convert to numeric for easier processing
    # dataset['Is Fraudulent'] = dataset['Is Fraudulent'].apply(lambda x: True if x == 1 else False)

    dataset['Account Age Category'] = pd.cut(dataset['Account Age Days'], bins=[-float('inf'), 90, float('inf')], labels=['New', 'Old'])

    fraud_counts = dataset.groupby(['Account Age Category', 'Is Fraudulent']).size().reset_index(name='Count')
    # fraud_counts = dataset.groupby('Account Age Category')['Is Fraudulent'].sum().reset_index()

    result_json = fraud_counts.to_json(orient='records')

    print(result_json)

    return result_json

def analyse_transaction_amount(dataset):
    dataset['Is Fraudulent'] = dataset['Is Fraudulent'].apply(lambda x: True if x == 1 else 0)
    
    q3 = dataset['Transaction Amount'].quantile(0.75)
    
    high_value_transactions = dataset[dataset['Transaction Amount'] > q3]
    
    fraud_count = high_value_transactions['Is Fraudulent'].sum()
    non_fraud_count = high_value_transactions.shape[0] - fraud_count
    
    result = [
        {"High Value Threshold": q3},
        {"Is Fraudulent": False, "Transaction Count": non_fraud_count},
        {"Is Fraudulent": True, "Transaction Count": fraud_count}
    ]
    
    result_json = pd.Series(result).to_json(orient='records')
    print(result_json)
    return result_json

def analyse_product_quantity(dataset):
    dataset['Is Fraudulent'] = dataset['Is Fraudulent'].apply(lambda x: True if x == 1 else False)
    
    high_quantity_threshold = dataset['Quantity'].quantile(0.75)
    
    high_quantity_transactions = dataset[dataset['Quantity'] > high_quantity_threshold]
    
    fraud_counts = high_quantity_transactions.groupby('Product Category')['Is Fraudulent'].sum().reset_index()
    total_counts = high_quantity_transactions['Product Category'].value_counts().reset_index()
    total_counts.columns = ['Product Category', 'Total Transactions']
    
    fraud_rates = pd.merge(fraud_counts, total_counts, on='Product Category')
    fraud_rates['Non-Fraudulent Transactions'] = fraud_rates['Total Transactions'] - fraud_rates['Is Fraudulent']
    
    result_json = fraud_rates.to_json(orient='records')
    print(result_json)
    return result_json

def analyse_payment_method(dataset):
    dataset['Is Fraudulent'] = dataset['Is Fraudulent'].apply(lambda x: True if x == 1 else False)
    result = []
    fraud_counts = dataset.groupby('Payment Method')['Is Fraudulent'].sum().reset_index()
    total_counts = dataset['Payment Method'].value_counts().reset_index()
    total_counts.columns = ['Payment Method', 'Total Transactions']

    for i in range(len(fraud_counts)):
        temp_payment = fraud_counts.iloc[i]['Payment Method']
        temp_count: int = fraud_counts.iloc[i]['Is Fraudulent']
        temp_total: int = total_counts[total_counts['Payment Method'] == temp_payment]['Total Transactions'].values[0]
        temp = {"payment_method": temp_payment, "fraud_rate": temp_count / temp_total, "fraud_count": int(str(temp_count)), "total_transaction": int(str(temp_total))}
        result.append(temp)
    
    global hypo5
    hypo5 = result

    return result


def analyse_location(dataset):
    cache_dataset = dataset.copy()
    result = []
    country_list = cache_dataset['Customer Location'].unique()
    for i in range(len(country_list)):
        country = country_list[i]
        temp = {
          "country": country_list[i], 
          "country_continent": countries[country]['continent'], 
          "country_iso_alpha": countries[country]['iso_alpha'], 
          "country_iso_num": countries[country]['iso_num'], 
          "fraud_count": 0, "total_transaction": 0, "fraud_rate": 0
        }
        result.append(temp)

    cache_dataset['Is Fraudulent'] = cache_dataset['Is Fraudulent'].apply(lambda x: True if x == 1 else False)
    for i in range(len(cache_dataset)):
        country = cache_dataset.iloc[i]['Customer Location']
        if country in country_list:
            result[country_list.tolist().index(country)]['total_transaction'] += 1
            if cache_dataset.iloc[i]['Is Fraudulent']:
                result[country_list.tolist().index(country)]['fraud_count'] += 1
            
    for i in range(len(result)):
        result[i]['fraud_rate'] = result[i]['fraud_count'] / result[i]['total_transaction']
            
    global hypo6
    hypo6 = result

    return result

def analyse_device_used(dataset):
    dataset['Is Fraudulent'] = dataset['Is Fraudulent'].apply(lambda x: True if x == 1 else False)
    result = []
    fraud_counts = dataset.groupby('Device Used')['Is Fraudulent'].sum().reset_index()
    total_counts = dataset['Device Used'].value_counts().reset_index()
    total_counts.columns = ['Device Used', 'Total Transactions']

    for i in range(len(fraud_counts)):
        temp_device = fraud_counts.iloc[i]['Device Used']
        temp_count: int = fraud_counts.iloc[i]['Is Fraudulent']
        temp_total: int = total_counts[total_counts['Device Used'] == temp_device]['Total Transactions'].values[0]
        temp = {"device_used": temp_device, "fraud_rate": temp_count / temp_total, "fraud_count": int(str(temp_count)), "total_transaction": int(str(temp_total))}
        result.append(temp)

    global hypo7
    hypo7 = result

    return result


def analyse_most_scam_age_group(dataset):
    default_age_group = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    result = []
    for i in range(len(default_age_group)):
        temp = {"age_group": default_age_group[i], "count": 0}
        result.append(temp)
    
    cache_dataset = dataset[dataset['Is Fraudulent'] == 1]
    for i in range(len(cache_dataset)):
        age = cache_dataset.iloc[i]['Customer Age']
        for j in range(len(default_age_group)):
            if '-' in default_age_group[j]:
                age_range = default_age_group[j].split('-')
                if int(age_range[0]) <= age <= int(age_range[1]):
                    result[j]['count'] += 1
            else:
                if age >= int(default_age_group[j][:-1]):
                    result[j]['count'] += 1
    global hypo8
    hypo8 = result

    return result


def analyse_by_product_category(dataset):
    products_list = dataset['Product Category'].unique()
    cache_dataset = dataset.copy()
    result = []
    for i in range(len(products_list)):
        product = products_list[i]
        temp = {"product_category": product, "fraud_count": 0, "total_transaction": 0}
        result.append(temp)

    for i in range(len(cache_dataset)):
        product = cache_dataset.iloc[i]['Product Category']
        if product in products_list:
            result[products_list.tolist().index(product)]['total_transaction'] += 1
            if cache_dataset.iloc[i]['Is Fraudulent']:
                result[products_list.tolist().index(product)]['fraud_count'] += 1

    global hypo9
    hypo9 = result

    return result