import pandas as pd

# Importing the original data file
pop_orig = pd.read_excel('raw_data/ACS_data/SF_total_population.xlsx', sheet_name = 1, header = [0, 1])

# Dropping the first column
pop_drop = pop_orig.drop(columns = ['Unnamed: 0_level_0'], level = 0)

# Compressing the heraders
pop_drop.columns = [' '.join(col).strip() for col in pop_drop.columns.values]

# Dropping MOE columns
pop_drop = pop_drop[pop_drop.columns.drop(list(pop_drop.filter(regex = 'Margin of Error')))]

# Pivoting rows and columns
pop_pivot = pop_drop.transpose()

# Resitng index of dataframe and renaming column names
pop_pivot = pop_pivot.reset_index()
pop_pivot = pop_pivot.rename(columns = {'index' : 'census_tract', 0 : 'total_pop'})

# Reformatting [total_pop] column
pop_pivot['total_pop'] = pop_pivot['total_pop'].replace(regex = r'(,)', value = '')
pop_pivot['total_pop'] = pop_pivot['total_pop'].astype(int)

# Extracting census tract
pop_pivot['census_tract'] = pop_pivot['census_tract'].str.extract(r'((\d+\.\d+)|(\d+))')

# Exporting dataframe as csv file
pop_pivot.to_csv('clean_data/ACS/SF_total_pop_clean.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')