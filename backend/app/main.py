from fastapi import FastAPI
import pandas as pd

app = FastAPI()

dataset_filepath = 'dataset/Fraudulent_E-Commerce_Transaction_Data.csv'
dataset = pd.read_csv(dataset_filepath)

hypo1 = None
hypo5 = None
hypo7 = None
hypo8 = None

@app.get("/")
async def root():
    return {"message": "Hello Triple K"}


@app.get("/hypothesis_1")
async def hypothesis_1():
    global hypo1
    if hypo1 is None:
        hypo1 = analyse_fraudulent_transaction(dataset)
    return hypo1


@app.get("/hypothesis_5")
async def hypothesis_5():
    global hypo5
    if hypo5 is None:
        hypo5 = analyse_payment_method(dataset)
    return hypo5


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

