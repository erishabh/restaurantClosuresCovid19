import pandas as pd
from helper_functions import addressCleaner

# Importing the original data file
business_CA = pd.read_csv('SF_open_data_portal_business_raw.csv')

# Deleteing all rows with address outside CA
business_CA = business_CA[business_CA['State'] == 'CA']

#################### cleaning business address ####################

# Using function to clean address
business_CA_st_ad = addressCleaner(business_CA, 'Street Address', 'City', 'State', 'Source Zipcode', 
    'street_address')

#################### Cleaning mail address ####################

# Using function to clean address
business_CA_all_ad = addressCleaner(business_CA_st_ad, 'Mail Address', 'Mail City', 'Mail State', 
    'Mail Zipcode', 'mail_address')

# Replacing nan in mail_address with street_address
business_CA_all_ad['mail_address'].fillna(business_CA_all_ad['street_address'], inplace = True)

# Exporting dataframe as csv file
business_CA_all_ad.to_csv('SF_open_data_business_clean.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')