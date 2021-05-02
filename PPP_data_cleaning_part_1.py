import pandas as pd
from helper_functions import naicsExtract

# Importing the original data files
ppp_150_1 = pd.read_csv('public_up_to_150k_1.csv')
ppp_150_2 = pd.read_csv('public_up_to_150k_2.csv')
ppp_150_plus = pd.read_csv('public_150k_plus.csv')

# Combining app PPP data into 1 dataframe
ppp_all = pd.concat([ppp_150_1, ppp_150_2, ppp_150_plus])

#################### cleaning city ####################

# Finding all unique city names
city_set = set(ppp_all['BorrowerCity'])

# Converting the set to a dataframe
city_df = pd.DataFrame(list(city_set))

# Exporting the dataframe as a csv
city_df.to_csv('PPP_city.csv', index = False, header = False)

print('********************** EXPORT COMPLETE **********************')

# Import manually cleaned list of cities in SF
city_SF = pd.read_csv('PPP_city_clean.csv')

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
zip_df.to_csv('PPP_zip.csv', index = False, header = False)

print('********************** EXPORT COMPLETE **********************')

# Import manually cleaned list of zip in SF
zip_SF = pd.read_csv('PPP_zip_clean.csv')

# Convert zip_SF to list
zip_SF_list = zip_SF["Zip"].tolist()

# Extracting rows in SF
ppp_SF_zip = ppp_SF.loc[ppp_SF['zip_5'].isin(zip_SF_list)]

# Exporting the dataframe as a csv
ppp_SF_zip.to_csv('PPP_SF.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')

#################### extracting NAICS ####################

# Storing the NAICS code 
code_drink = 7224
code_food = 7225
dummy_code = 7224000000

# Selecting rows that that have code_food
ppp_SF_food = naicsExtract(ppp_SF_zip, 'NAICSCode', code_food)

# Selecting rows that that have code_food
ppp_SF_drink = naicsExtract(ppp_SF_zip, 'NAICSCode', code_drink)

# Creating dataframe with both food and drink
ppp_SF_food_drink = pd.concat([ppp_SF_food, ppp_SF_drink])

# Exporting the dataframe as a csv
ppp_SF_food.to_csv('PPP_SF_food.csv', index = False, header = True)
ppp_SF_drink.to_csv('PPP_SF_drink.csv', index = False, header = True)
ppp_SF_food_drink.to_csv('PPP_SF_food_drink.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')