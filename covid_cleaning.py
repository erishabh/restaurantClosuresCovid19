import pandas as pd
import shapely.wkt as shp

# Importing the original data file
covid_orig = pd.read_csv('raw_data/covid_19_cases_geog.csv')

# Deleting unecesary columns - [area_type, last_updated_at, deaths, rate]
covid_drop = covid_orig.drop(columns = ['area_type', 'last_updated_at', 'deaths', 'rate'])

# Converting data in [id] to string
covid_drop['id'] = covid_drop['id'].astype(str)

# Extracting cencus tract number from [id] column
covid_drop['census_tract_unf'] = covid_drop['id'].str.extract(r'(.{6}$)')
covid_drop['census_tract_first'] = covid_drop['census_tract_unf'].str.extract(r'(^.{4})')
covid_drop['census_tract_last'] = covid_drop['census_tract_unf'].str.extract(r'(.{2}$)')
covid_drop['census_tract_last'] = covid_drop['census_tract_last'].replace({'00' : ''})
covid_drop['census_tract'] = covid_drop['census_tract_first'].str.cat(covid_drop['census_tract_last'], sep = '.')
covid_drop['census_tract'] = covid_drop['census_tract'].replace(regex = r'(\.)$', value = '')
covid_drop['census_tract'] = covid_drop['census_tract'].replace(regex = r'(^0)', value = '')

# Dropping all columns used in census tract extraction
covid_clean = covid_drop.drop(columns = ['census_tract_unf', 'census_tract_first', 'census_tract_last', 'id'])

# Cleaning [acs_population] column
covid_clean['acs_population'] = covid_clean['acs_population'].replace(regex = r'(,)', value = '')

# Creating [covid_percent] column
covid_clean['acs_population'] = covid_clean['acs_population'].astype(int)
covid_clean['covid_percent'] = (covid_clean['count'] / covid_clean['acs_population']) * 100

# Reorder columns in dataframe
covid_clean = covid_clean[['census_tract', 'count', 'acs_population', 'covid_percent', 'multipolygon']]

# Sorting the dataframe based on census tract
covid_clean = covid_clean.sort_values(by = ['census_tract'], ascending = True)

# Renaming the multipolygon column to geometry
covid_clean = covid_clean.rename(columns = {'multipolygon': 'geometry'})

# Converting the multipoygon column to polygon data type
covid_clean['geometry'] = covid_clean['geometry'].apply(lambda x: shp.loads(x))

# Exporting dataframe as csv file
covid_clean.to_csv('clean_data/SF_covid_conc.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')