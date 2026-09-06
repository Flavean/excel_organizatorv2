import pandas as pd

from core.cleaner import clean_data


data = pd.DataFrame({
    "Name": ["  Apple  ", "Banana", "  Apple  ", None, "Orange"],
    "Price": [10, 15, 10, None, 20]
})

options = {
    "remove_empty_rows": True,
    "remove_duplicates": True,
    "clean_spaces": True
}

cleaned_data = clean_data(data, options)

print(cleaned_data)