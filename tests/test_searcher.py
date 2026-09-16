import pandas as pd

from core.searcher import search_data


data = pd.DataFrame({
    "Name": ["Apple", "Banana", "Orange", "Pineapple"],
    "Price": [10, 15, 20, 25]
})


result = search_data(data, "apple")

print("Search results:")
print(result)