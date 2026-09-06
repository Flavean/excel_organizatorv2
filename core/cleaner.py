def remove_empty_rows(data):
    return data.dropna(how="all")

def remove_empty_columns(data):
    return data.dropna(axis=1, how="all")

def remove_sparse_columns(data, threshold):
    limit = len(data) * threshold

    columns_to_keep = data.isna().sum() <= limit

    return data.loc[:, columns_to_keep]

def remove_duplicates(data):
    return data.drop_duplicates()

def clean_spaces(data):
    data = data.copy()

    for column in data.select_dtypes(include="object").columns:
        data[column] = data[column].str.strip()

    return data

    return data
def clean_data(data, options):
    if options["remove_empty_rows"]:
        data = remove_empty_rows(data)

    if options["remove_empty_columns"]:
        dara = remove_empty_columns(data)

    if options["remove_sparse_columns"]:
        data = remove_sparse_columns(data, options["threshold"])

    if options["remove_duplicates"]:
        data = remove_duplicates(data)

    if options["clean_spaces"]:
        data = clean_spaces(data)

    return data