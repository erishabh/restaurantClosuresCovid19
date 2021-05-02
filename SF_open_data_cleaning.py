import pandas as pd
from helper_functions import addressCleaner

# Importing the original data file
business_CA = pd.read_csv('SF_open_data_portal_business_raw.csv')

# Deleteing all rows with address outside CA
business_CA = business_CA[business_CA['State'] == 'CA']

#################### cleaning city ####################

# Finding all unique city names
city_set = set(business_CA['City'])

# Converting the set to a dataframe
city_df = pd.DataFrame(list(city_set))

# Exporting the dataframe as a csv
city_df.to_csv('SF_open_data_city.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')

# Import manually cleaned list of cities in SF
city_SF = pd.read_csv('SF_open_data_city_clean.csv')

# Convert city_SF to list
city_SF_list = city_SF["City"].tolist()

# Extracting rows in SF
business_CA = business_CA[business_CA['City'].isin(city_SF_list)]

# Exporting the dataframe as a csv
business_CA.to_csv('SF_open_data_city_only.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')

#################### cleaning zip ####################

# Extracting 5 digit zipcode
business_CA['zip_5'] = business_CA['Source Zipcode'].astype(str).str[:5]

# Finding all unique zip codes
zip_set = set(business_CA['zip_5'])

# Converting the set to a dataframe
zip_df = pd.DataFrame(list(zip_set))

# Exporting the dataframe as a csv
zip_df.to_csv('SF_open_data_zip.csv', index = False, header = False)

print('********************** EXPORT COMPLETE **********************')

# Import manually cleaned list of zip in SF
zip_SF = pd.read_csv('SF_open_data_zip_clean.csv')

# Converting from int to str
zip_SF['Zip'] = zip_SF['Zip'].astype(str)

# Convert zip_SF to list
zip_SF_list = zip_SF["Zip"].tolist()

# Extracting rows in SF
business_CA = business_CA.loc[business_CA['zip_5'].isin(zip_SF_list)]

# Dropping zip_5
business_CA.drop(columns = ['zip_5'], inplace = True)

# Cleaning business address
business_CA_clean = addressCleaner(business_CA, 'Street Address', 'City', 'State', 'Source Zipcode', 
    'street_address')

# Exporting dataframe as csv file
business_CA_clean.to_csv('SF_open_data_business_clean.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')