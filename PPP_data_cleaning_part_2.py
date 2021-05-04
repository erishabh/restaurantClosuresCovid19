import pandas as pd

# Importing the original data files
ppp_fd_1 = pd.read_csv('ppp_data_parts_geocoded/PPP_SF_food_drink_1_coded.csv')
ppp_fd_2 = pd.read_csv('ppp_data_parts_geocoded/PPP_SF_food_drink_2_coded.csv')
ppp_fd_3 = pd.read_csv('ppp_data_parts_geocoded/PPP_SF_food_drink_3_coded.csv')
ppp_fd_4 = pd.read_csv('ppp_data_parts_geocoded/PPP_SF_food_drink_4_coded.csv')

# Combining app PPP data into 1 dataframe
ppp_fd = pd.concat([ppp_fd_1, ppp_fd_2, ppp_fd_3, ppp_fd_4])

# Exporting the dataframe as a csv
ppp_fd.to_csv('clean_data/PPP_SF_food_drink_tract.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')

#################### cleaning census tract ####################

# Finding all unique census tracts
tract_set = set(ppp_fd['Census Tract Code'])

# Converting the set to a dataframe
tract_df = pd.DataFrame(list(tract_set))

# Exporting the dataframe as a csv
tract_df.to_csv('data_cleaning_helper/PPP_census_tract.csv', index = False, header = False)

print('********************** EXPORT COMPLETE **********************')

# Import manually cleaned list of census tracts
tract_SF = pd.read_csv('data_cleaning_helper/PPP_census_tract_clean.csv')

# Making sure that all columns are string
ppp_fd['Census Tract Code'] = ppp_fd['Census Tract Code'].astype(str)
tract_SF['orig_tract'] = tract_SF['orig_tract'].astype(str)
tract_SF['clean_tract'] = tract_SF['clean_tract'].astype(str)

# Combining food+drink db with clean census tract db
ppp_fd = ppp_fd.merge(tract_SF, how = 'left', left_on = 'Census Tract Code', right_on = 'orig_tract')

# Cleaning census 
ppp_fd['clean_tract'] = ppp_fd['clean_tract'].replace(regex = r'(\.0)$', value = '')

# Dropping other tract columns
ppp_fd.drop(columns = ['orig_tract', 'Census Tract Code', 'Full FIPS (tract)'], inplace = True)

# Dropping rows where clean_tract == 0
ppp_fd = ppp_fd.loc[ppp_fd['clean_tract'] != '0']

#################### merging ACS data ####################

# Importing the acs data = covid data
acs_data = pd.read_csv('clean_data/SF_ACS_covid.csv')

# Making sure that all columns are string
acs_data['census_tract'] = acs_data['census_tract'].astype(str)

# Cleaning census 
acs_data['census_tract'] = acs_data['census_tract'].replace(regex = r'(\.0)$', value = '')

# Merging the two datasets
ppp_fd = ppp_fd.merge(acs_data, how = 'left', left_on = 'clean_tract', right_on = 'census_tract', validate = 'm:1')

# Dropping other tract columns
ppp_fd.drop(columns = ['clean_tract', 'geometry'], inplace = True)

# Exporting the dataframe as a csv
ppp_fd.to_csv('clean_data/PPP_ACS_Covid_food_drink.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')