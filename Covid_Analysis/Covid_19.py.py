import pandas as pd
import requests

#step 1 Data Collection

url = 'https://en.wikipedia.org/wiki/Template:COVID-19_pandemic_data'
req = requests.get(url)
data_list = pd.read_html(req.text)
target_df = data_list[0]

# Step 2: Data Cleaning

#issue 1: change column names
target_df.columns = ['col0','Country Name','Total Cases','Total Deaths','Total Recoveries','col5']

#issue 2: remove 1st and 5th column
target_df = target_df[['Country Name','Total Cases','Total Deaths','Total Recoveries']]

#issue 3: last and second last rows
#target_df = target_df.drop([238,239]) (not dynamic)
last_idx = target_df.index[-1]
target_df = target_df.drop([last_idx, last_idx-1])

#issue 4: inconsistent country names
target_df['Country Name'] = target_df['Country Name'].str.replace('\[.*\]', '')

#issue 5: replace"not data value" cell by "0"
target_df['Total Recoveries'] = target_df['Total Recoveries'].str.replace('No data', '0')
target_df['Total Deaths'] = target_df['Total Deaths'].str.replace('No data', '0')
target_df['Total Cases'] = target_df['Total Cases'].str.replace('No data', '0')
target_df['Total Deaths'] = target_df['Total Deaths'].str.replace('+', '')

#issue 6: Change data type
print(target_df.dtypes) #to check data types of entitities)
target_df['Total Cases'] = pd.to_numeric(target_df['Total Cases'])
target_df['Total Deaths'] = pd.to_numeric(target_df['Total Deaths'])
target_df['Total Recoveries'] = pd.to_numeric(target_df['Total Recoveries'])

#Step 3: Export data
#target_df.to_csv(r'Covid_19_dataset.csv') (use if required)
target_df.to_excel(r'Covid_19_dataset.xlsx')
