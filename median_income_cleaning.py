import pandas as pd

# Importing the original data file
med_orig = pd.read_excel('raw_data/ACS_data/SF_median_income.xlsx', sheet_name = 1, header = [0, 1, 2])

# Dropping the first column
med_drop = med_orig.drop(columns = ['Unnamed: 0_level_0'], level = 0)

# Compressing the heraders
med_drop.columns = [' '.join(col).strip() for col in med_drop.columns.values]

# Dropping MOE columns and the family columns
med_drop = med_drop[med_drop.columns.drop(list(med_drop.filter(regex = r'((Families)|(Nonfamily)|(families))')))]
med_drop = med_drop[med_drop.columns.drop(list(med_drop.filter(regex = 'Margin of Error')))]

# Pivoting rows and columns
med_pivot = med_drop.transpose()

# Resitng index of dataframe and renaming column names
med_pivot = med_pivot.reset_index()
med_pivot = med_pivot.rename(columns = {'index' : 'census_tract', 0 : 'median_household_income'})

# Reformatting [median_household_income] column
med_pivot['median_household_income'] = med_pivot['median_household_income'].replace(regex = r'(,)', value = '')
med_pivot['median_household_income'] = med_pivot['median_household_income'].replace(regex = r'(-)', value = '0')
med_pivot['median_household_income'] = med_pivot['median_household_income'].astype(int)

# Extracting census tract
med_pivot['census_tract'] = med_pivot['census_tract'].str.extract(r'((\d+\.\d+)|(\d+))')

# Exporting dataframe as csv file
med_pivot.to_csv('clean_data/ACS/SF_med_hhold_inc_clean.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')
