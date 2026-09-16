def filter_data(data, column, value):
    value = str(value).strip().lower()

    mask = (
        data[column]
        .astype(str)
        .str.strip()
        .str.lower()
        == value
    )

    return data[mask]