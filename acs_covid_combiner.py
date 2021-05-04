import pandas as pd

# Importing the original data file
acs_data = pd.read_csv('clean_data/SF_acs_data_clean.csv')
covid_data = pd.read_csv('clean_data/SF_covid_conc.csv')

# Combining the two dataframes
combined_data = acs_data.merge(covid_data, on = 'census_tract')

# Renaming some columns
combined_data = combined_data.rename(columns = {'count' : 'covid_count', 'acs_population' : 'covid_pop'})

# Exporting dataframe as csv file
combined_data.to_csv('clean_data/SF_ACS_covid.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')