def search_data(data, search_term):
    search_term = str(search_term).lower()

    mask = data.astype(str).apply(
        lambda column: column.str.lower().str.contains(
            search_term, 
            na=False
        )
    )

    return data[mask.any(axis=1)]