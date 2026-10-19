import pandas as pd


def split_into_sheets(data, column):
    sheets = {}

    clean_data = data.copy()

    clean_data[column] = (
        clean_data[column]
        .astype(str)
        .str.strip()
    )

    for value in clean_data[column].dropna().unique():
        sheet_data = clean_data[
            clean_data[column] == value
        ].copy()

        sheets[str(value)] = sheet_data

    return sheets