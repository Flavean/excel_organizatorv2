import pandas as pd

from core.cleaner import clean_data


data = pd.DataFrame({
    "Name": ["  Apple  ", "Banana", "  Apple  ", None, "Orange"],
    "Price": [10, 15, 10, None, 20]
})


options = {
    "remove_empty_rows": True,
    "remove_empty_columns": True,
    "remove_duplicates": True,
    "clean_spaces": True,
    "remove_sparse_columns": False,
    "threshold": 0.8
}


cleaned_data = clean_data(data, options)

print(cleaned_data)


from core.sorter import sort_data


sorted_data = sort_data(
    data,
    "Price",
    ascending=False
)

print("\nSorted data:")
print(sorted_data)