import pandas as pd

# Importing the original data file
race_orig = pd.read_excel('raw_data/ACS_data/SF_race_ethnicity.xlsx', sheet_name = 1, header = [0, 1], index_col = 0)

# Compressing the heraders
race_orig.columns = [' '.join(col).strip() for col in race_orig.columns.values]

# Dropping MOE columns and the percet, owner, and renter columns
race_drop = race_orig[race_orig.columns.drop(list(race_orig.filter(regex = r'((Percent)|(Margin of Error))')))]

# Pivoting rows and columns
race_pivot = race_drop.transpose()

# Reformatting data
race_int = race_pivot.replace(regex = r'(,)', value = '')
race_int = race_int.astype(int)

# Creating [bipoc] and [indigenous] column
race_int['bipoc_pop'] = race_int['Total population'] - race_int['White alone']
race_int['indigenous_pop'] = race_int['American Indian and Alaska Native alone'] + race_int['Native Hawaiian and Other Pacific Islander alone']

# Drop columns
race_drop_calc = race_int.drop(columns = ['Total population', 'White alone', 'American Indian and Alaska Native alone', 'Native Hawaiian and Other Pacific Islander alone'])

# Renaming columsn for ease of use
race_clean = race_drop_calc.rename(columns = {'Hispanic or Latino (of any race)' : 'hispanic_pop', 'Black or African American alone' : 'afam_pop', 'Asian alone' : 'asian_pop'})
race_clean = race_clean[['hispanic_pop', 'afam_pop', 'asian_pop', 'indigenous_pop', 'bipoc_pop']]

# Reseting index and renaming columns
race_clean = race_clean.reset_index()
race_clean = race_clean.rename(columns = {'index' : 'census_tract'})

# Extracting census tract
race_clean['census_tract'] = race_clean['census_tract'].str.extract(r'((\d+\.\d+)|(\d+))')

# Exporting dataframe as csv file
race_clean.to_csv('clean_data/ACS/SF_race_clean.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')