import pandas as pd


def merge_files(file_paths):
    dataframes = []

    for file_path in file_paths:
        data = pd.read_excel(file_path)
        dataframes.append(data)

    if not dataframes:
        return pd.DataFrame()

    return pd.concat(
        dataframes,
        ignore_index=True
    )