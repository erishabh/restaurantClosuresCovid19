import pandas as pd

# Importing the original data file
low_orig = pd.read_excel('raw_data/ACS_data/SF_low_income.xlsx', sheet_name = 1, header = [0, 1, 2], index_col = 0)

# Compressing the heraders
low_orig.columns = [' '.join(col).strip() for col in low_orig.columns.values]

# Dropping MOE columns and the percet, owner, and renter columns
low_drop = low_orig[low_orig.columns.drop(list(low_orig.filter(regex = r'((Percent)|(Owner)|(Renter))')))]
low_drop = low_drop[low_drop.columns.drop(list(low_drop.filter(regex = 'Margin of Error')))]

# Pivoting rows and columns
low_pivot = low_drop.transpose()

# Reformatting data
low_clean = low_pivot.astype(int)

# Calculating the total low income population per tract
low_clean['low_income_pop'] = low_clean.sum(axis = 1)

# Dropping the individual columns
low_clean = low_clean[['low_income_pop']]

# Reseting index and renaming columns
low_clean = low_clean.reset_index()
low_clean = low_clean.rename(columns = {'index' : 'census_tract'})

# Extracting census tract
low_clean['census_tract'] = low_clean['census_tract'].str.extract(r'((\d+\.\d+)|(\d+))')

# Exporting dataframe as csv file
low_clean.to_csv('clean_data/ACS/SF_low_inc_pop_clean.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')