import pandas as pd

def addressCleaner(df, address, city, state, zip_code, new_col):
    """
    Cleans the address of a given data frame by consolidating it from
    different columns in a dataframe. 

    addressCleaner(df, address, city, state, zip_code, new_col)

    Arguments:

    df:         DataFrame with columns that contain the address columns
    address:    Column name in df that contains the street address
    city:       Column name in df that contains the city (only used for column deletion)
    state:      Column name in df that contains the state
    zip_code:   Column name in df that contains the zip code
    new_col:    Column name that will contain the consolidated address

    Returns:
    
    df_copy:    A copy of the input df with new_col and all other address columns dropped
    """

    # Making a copy of the dataframe
    df_copy = df.copy()

    # Making columns lowercase [Street Address, City]
    df_copy[address] = df_copy[address].str.lower()

    # Making state uppercase
    df_copy[state] = df_copy[state].str.upper()

    # Splitting relevent columns on non-word elements [Street Address, City]
    df_copy['street_add_list'] = df_copy[address].str.split(pat = r'\b\W')

    # Extracting first 5 digits from zip code
    df_copy['zip_5'] = df_copy[zip_code].astype(str).str[:5]

    # Combining lists in clumns with ' '
    df_copy['street_add_list_join'] = df_copy['street_add_list'].str.join(sep = ' ')

    # Joining all street address columns together
    df_copy[new_col] = (df_copy['street_add_list_join'] + ', san francisco, ' + df_copy[state] 
        + ', ' + df_copy['zip_5'])

    # Deleting extraneous columns
    df_copy.drop(columns = ['street_add_list', 'zip_5', 'street_add_list_join', 
        address, city, state, zip_code], inplace = True)

    # Returning the dataframe
    return df_copy

def naicsExtract(df, code_col, code):
    """
    Stracts rows from a dataframe that correspond to the specific NAICS code (starting 4 digits)

    naicsExtract(df, code_col, code)

    Arguments:

    df:         DataFrame with columns that contain the data
    code_col:   Column name in the df that contains the NAICS code
    code:       NAICS code to be matched - starting 4 digits

    Returns:
    
    df_copy_naics:    A copy of the input df with only rows corresponding to the NAICS code

    """

    # Making a copy of the dataframe
    df_copy = df.copy()

    # Making sure that all NAICS codes are full
    df_copy[code_col].fillna(1111, inplace = True)

    # Extracting naics code from dataset
    df_copy['naics_4'] = (df_copy[code_col].astype(str).str[:4]).astype(int)

    # Selecting rows that that have code_food
    df_copy_naics = df_copy.loc[df_copy['naics_4'] == code]

    # Dropping the naics_4 columns
    df_copy_naics.drop(columns = ['naics_4'], inplace = True)

    return df_copy_naics