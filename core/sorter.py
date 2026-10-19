def sort_data(data, column, ascending=True):
    sorted_data = data.copy()

    if sorted_data[column].dtype == "object":
        sorted_data["_sort_key"] = (
            sorted_data[column]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        sorted_data = sorted_data.sort_values(
            by="_sort_key",
            ascending=ascending,
            na_position="last"
        )

        sorted_data = sorted_data.drop(columns="_sort_key")

    else:
        sorted_data = sorted_data.sort_values(
            by=column,
            ascending=ascending,
            na_position="last"
        )

    return sorted_data