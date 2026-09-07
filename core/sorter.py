def sort_data(data, column, ascending=True):
    return data.sort_values(
        by=column, 
        ascending=ascending, 
        na_position="last",
    )