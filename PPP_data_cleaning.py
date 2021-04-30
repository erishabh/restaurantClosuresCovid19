import pandas as pd
from helper_functions import addressCleaner

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
city_df.to_csv('PPP_city.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')

# # Converting all city to lowercase
# ppp_all['BorrowerCity'] = ppp_all['BorrowerCity'].str.lower()

# # Splitting the city into non-word elements
# ppp_all['BorrowerCity'] = ppp_all['BorrowerCity'].str.split(pat = r'\b\W')

# # Joining the city
# ppp_all['BorrowerCity'] = ppp_all['BorrowerCity'].str.join(sep = ' ')

# # Extracting San Francisco
# ppp_SF = ppp_all.loc[ppp_all['BorrowerCity'] == 'san francisco']

# #################### Extracting NAICS Code ####################

# # Storing the NAICS code 
# code_drinks = 7224
# code_food = 7225

# # 


# print(len(ppp_SF.index))
# print(set(ppp_all['BorrowerCity']))