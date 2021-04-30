import pandas as pd

def addressCleaner(df, address, city, state, zip_code, new_col):
    """
    Cleans the address of a given data frame by consolidating it from
    different columns in a dataframe. 

    addressCleaner(df, address, city, state, zip_code, new_col)

    Arguments:
    df:         DataFrame with columns that contain the address columns
    address:    Column name in df that contains the street address
    city:       Column name in df that contains the city
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
    df_copy[city] = df_copy[city].str.lower()

    # Making state uppercase
    df_copy[state] = df_copy[state].str.upper()

    # Splitting relevent columns on non-word elements [Street Address, City]
    df_copy['street_add_list'] = df_copy[address].str.split(pat = r'\b\W')
    df_copy['city_list'] = df_copy[city].str.split(pat = r'\b\W')

    # Extracting first 5 digits from zip code
    df_copy['zip_5'] = df_copy[zip_code].astype(str).str[:5]

    # Combining lists in clumns with ' '
    df_copy['street_add_list_join'] = df_copy['street_add_list'].str.join(sep = ' ')
    df_copy['city_list_join'] = df_copy['city_list'].str.join(sep = ' ')

    # Joining all street address columns together
    df_copy[new_col] = (df_copy['street_add_list_join'] + ', ' + df_copy['city_list_join'] 
        + ', ' + df_copy[state] + ', ' + df_copy['zip_5'])

    # Deleting extraneous columns
    df_copy.drop(columns = ['street_add_list', 'city_list', 'zip_5', 'street_add_list_join', 
        'city_list_join', address, city, state, zip_code], inplace = True)

    # Returning the dataframe
    return df_copy

