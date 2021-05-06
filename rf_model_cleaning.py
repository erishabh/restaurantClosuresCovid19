import pandas as pd
from helper_functions import yCreate2, yCreate4, yCreate7

# Importing data file
data = pd.read_csv('clean_data/PPP_ACS_Covid_food_drink.csv')

# Dropping record that has no census value or business type (only 1 of each)
data = data.loc[data['BorrowerName'] != 'SSF RESTAURANT LLC']
data = data.loc[data['BusinessType'].notnull()]

# Removing columns that have the same value for all records
data.drop(columns = ['BorrowerName', 'SBAGuarantyPercentage', 'InitialApprovalAmount', 'RuralUrbanIndicator', 
    'street_address', 'Latitude', 'Longitude', 'census_tract'], inplace = True)

# Filling NaN in proceed columns
data[['UTILITIES_PROCEED', 'PAYROLL_PROCEED', 'MORTGAGE_INTEREST_PROCEED', 'RENT_PROCEED', 'REFINANCE_EIDL_PROCEED', 'HEALTH_CARE_PROCEED', 'DEBT_INTEREST_PROCEED']] = (
    data[['UTILITIES_PROCEED', 'PAYROLL_PROCEED', 'MORTGAGE_INTEREST_PROCEED', 'RENT_PROCEED', 'REFINANCE_EIDL_PROCEED', 'HEALTH_CARE_PROCEED', 'DEBT_INTEREST_PROCEED']].fillna(value = 0))

# Converting proceed columns to 1/0
data[['UTILITIES_PROCEED', 'PAYROLL_PROCEED', 'MORTGAGE_INTEREST_PROCEED', 'RENT_PROCEED', 'REFINANCE_EIDL_PROCEED', 'HEALTH_CARE_PROCEED', 'DEBT_INTEREST_PROCEED', 'UndisbursedAmount']] = (
    data[['UTILITIES_PROCEED', 'PAYROLL_PROCEED', 'MORTGAGE_INTEREST_PROCEED', 'RENT_PROCEED', 'REFINANCE_EIDL_PROCEED', 'HEALTH_CARE_PROCEED', 'DEBT_INTEREST_PROCEED', 'UndisbursedAmount']].astype(bool).astype(int))

# Converting Term and NAICS code to string
data[['Term', 'NAICSCode']] = data[['Term', 'NAICSCode']].astype(str)

# One Hot Encoding Categorical Variables
col_enc = ['LoanStatus', 'Term', 'HubzoneIndicator', 'LMIIndicator', 'BusinessAgeDescription', 'NAICSCode', 
    'BusinessType']

data_enc = pd.get_dummies(data = data, drop_first = True)

# Creating the Y column
data_enc['Y_2'] = data_enc.apply(lambda row: yCreate2(row), axis = 1)
data_enc['Y_4'] = data_enc.apply(lambda row: yCreate4(row), axis = 1)
data_enc['Y_7'] = data_enc.apply(lambda row: yCreate7(row), axis = 1)

# Making sure there are no NaN
data_enc = data_enc.fillna(value = 0)

# Exporting the dataframe as a csv
data_enc.to_csv('clean_data/rf_model.csv', index = False, header = True)

print('********************** EXPORT COMPLETE **********************')