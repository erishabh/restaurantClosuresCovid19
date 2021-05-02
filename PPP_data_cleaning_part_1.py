import pandas as pd
from helper_functions import *

# Importing the original data files
ppp_150_1 = pd.read_csv('raw_data/public_up_to_150k_1.csv')
ppp_150_2 = pd.read_csv('raw_data/public_up_to_150k_2.csv')
ppp_150_plus = pd.read_csv('raw_data/public_150k_plus.csv')

# Combining app PPP data into 1 dataframe
ppp_all = pd.concat([ppp_150_1, ppp_150_2, ppp_150_plus])

#################### cleaning city ####################

# Finding all unique city names
city_set = set(ppp_all['BorrowerCity'])

# Converting the set to a dataframe
city_df = pd.DataFrame(list(city_set))

# Exporting the dataframe as a csv
city_df.to_csv('data_cleaning_helper/PPP_city.csv', index = False, header = False)

print('********************** EXPORT COMPLETE **********************')

# Import manually cleaned list of cities in SF
city_SF = pd.read_csv('data_cleaning_helper/PPP_city_clean.csv')

# Convert city_SF to list
city_SF_list = city_SF["City"].tolist()

# Extracting rows in SF
ppp_SF = ppp_all.loc[ppp_all['BorrowerCity'].isin(city_SF_list)]

#################### cleaning zip ####################

# Extracting 5 digit zipcode
ppp_SF['zip_5'] = (ppp_SF['BorrowerZip'].astype(str).str[:5]).astype(int)

# Finding all unique zip codes
zip_set = set(ppp_SF['zip_5'])

# Converting the set to a dataframe
zip_df = pd.DataFrame(list(zip_set))

# Exporting the dataframe as a csv
zip_df.to_csv('data_cleaning_helper/PPP_zip.csv', index = False, header = False)

print('********************** EXPORT COMPLETE **********************')

# Import manually cleaned list of zip in SF
zip_SF = pd.read_csv('data_cleaning_helper/PPP_zip_clean.csv')

# Convert zip_SF to list
zip_SF_list = zip_SF["Zip"].tolist()

# Extracting rows in SF
ppp_SF_zip = ppp_SF.loc[ppp_SF['zip_5'].isin(zip_SF_list)]

# Exporting the dataframe as a csv
ppp_SF_zip.to_csv('clean_data_parts/PPP_SF.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')

#################### extracting NAICS ####################

# Dropping zip_5
ppp_SF_zip.drop(columns = ['zip_5'], inplace = True)

# Storing the NAICS code 
code_drink = 7224
code_food = 7225

# Selecting rows that that have code_food
ppp_SF_food = naicsExtract(ppp_SF_zip, 'NAICSCode', code_food)

# Selecting rows that that have code_food
ppp_SF_drink = naicsExtract(ppp_SF_zip, 'NAICSCode', code_drink)

#################### cleaning address ####################

ppp_SF_food_clean = addressCleaner(ppp_SF_food, 'BorrowerAddress', 'BorrowerCity', 'BorrowerState',
    'BorrowerZip', 'street_address')

ppp_SF_drink_clean = addressCleaner(ppp_SF_drink, 'BorrowerAddress', 'BorrowerCity', 'BorrowerState',
    'BorrowerZip', 'street_address')

# Creating dataframe with both food and drink
ppp_SF_food_drink = pd.concat([ppp_SF_food_clean, ppp_SF_drink_clean])

# Splitting the dataframe into geocodable sections
ppp_SF_food_drink_1 = ppp_SF_food_drink.iloc[:970, :]
ppp_SF_food_drink_2 = ppp_SF_food_drink.iloc[970:1940, :]
ppp_SF_food_drink_3 = ppp_SF_food_drink.iloc[1940:2910, :]
ppp_SF_food_drink_4 = ppp_SF_food_drink.iloc[2910:, :]

# Exporting the dataframe as a csv
ppp_SF_food_drink.to_csv('clean_data_parts/PPP_SF_food_drink.csv', index = False, header = True)
ppp_SF_food_drink_1.to_csv('ppp_data_parts/PPP_SF_food_drink_1.csv', index = False, header = True)
ppp_SF_food_drink_2.to_csv('ppp_data_parts/PPP_SF_food_drink_2.csv', index = False, header = True)
ppp_SF_food_drink_3.to_csv('ppp_data_parts/PPP_SF_food_drink_3.csv', index = False, header = True)
ppp_SF_food_drink_4.to_csv('ppp_data_parts/PPP_SF_food_drink_4.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')