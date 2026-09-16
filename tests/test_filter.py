import pandas as pd

from core.filter import filter_data


data = pd.DataFrame({
    "Name": ["Apple", "Banana", "Orange", "Pineapple"],
    "Category": ["Fruit", "Fruit", "Fruit", "Fruit"],
    "Price": [10, 15, 20, 25]
})


result = filter_data(data, "Price", 20)

print("Filter results:")
print(result)