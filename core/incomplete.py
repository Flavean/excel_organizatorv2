def separate_incomplete_rows(data, required_columns):
    complete = data.dropna(
        subset=required_columns
    )

    incomplete = data[
        ~data.index.isin(complete.index)
    ]

    return complete, incomplete