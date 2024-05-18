from fastapi import FastAPI
import pandas as pd

app = FastAPI()

dataset_filepath = 'dataset/Fraudulent_E-Commerce_Transaction_Data.csv'
dataset = pd.read_csv(dataset_filepath)

hypo8 = None

@app.get("/")
async def root():
    return {"message": "Hello Triple K"}


@app.get("/hypothesis_8")
async def hypothesis_8():
    global hypo8
    if hypo8 is None:
        hypo8 = analyse_most_scam_age_group(dataset)
    return hypo8


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

