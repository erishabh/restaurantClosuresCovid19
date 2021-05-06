import pandas as pd
from helper_functions import *

# Importing data file
data = pd.read_csv('clean_data/PPP_ACS_Covid_food_drink.csv')
orbis = pd.read_excel('raw_data/orbis.xlsx', sheet_name = 1)

# Filling in Nan
orbis[['Address line 1\nLatin Alphabet', 'Address line 2\nLatin Alphabet', 'Address line 3\nLatin Alphabet', 'Address line 4\nLatin Alphabet']] = (
    orbis[['Address line 1\nLatin Alphabet', 'Address line 2\nLatin Alphabet', 'Address line 3\nLatin Alphabet', 'Address line 4\nLatin Alphabet']].fillna(value = ''))

# combining address col
orbis['address_name'] = (orbis['Address line 1\nLatin Alphabet'] + orbis['Address line 2\nLatin Alphabet'] + 
    orbis['Address line 3\nLatin Alphabet'] + orbis['Address line 4\nLatin Alphabet'])

# Creating a state column
orbis['state'] = 'CA'

# Cleaning city
orbis_clean = addressCleaner(orbis, 'address_name', 'City\nLatin Alphabet', 'state',
    'Postcode\nLatin Alphabet', 'street_address')
    
# Dropping other cols
orbis_clean.drop(columns = ['Address line 1\nLatin Alphabet', 'Address line 2\nLatin Alphabet',
    'Address line 3\nLatin Alphabet', 'Address line 4\nLatin Alphabet'], inplace = True)

#################### extracting NAICS ####################

# Storing the NAICS code 
code_drink = 7224
code_food = 7225

# Selecting rows that that have code_food
orbis_clean_food = naicsExtract(orbis_clean, 'NAICS 2017, core code (4 digits)', code_food)

# Selecting rows that that have code_food
orbis_clean_drink = naicsExtract(orbis_clean, 'NAICS 2017, core code (4 digits)', code_drink)

# Combining both data frames
orbis_clean = pd.concat([orbis_clean_food, orbis_clean_drink])

# Joining the two tables
data = data.merge(orbis_clean, how = 'inner', left_on = 'street_address', right_on = 'street_address')

# Exporting the dataframe as a csv
data.to_csv('clean_data/PPP_ACS_Covid_ORBIS_food_drink.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')
print(len(data.index))