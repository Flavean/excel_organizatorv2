import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table


def load_excel(file_path):
    return pd.read_excel(file_path)

def save_excel(data, file_path):
    if file_path.endswitch(".xlsx"):
        data.to_excel(file_path, index=False)

    elif file_path.endswitch(".csv"):
        data.to_csv(file_path, index=False)

    elif file_path.endswitch(".json"):
        data.to_json(file_path, orient="records", indent=4)

    elif file_path.endswitch(".html"):
        data.to_html(file_path, index=False)


def save_pdf(data, file_path):
    document = SimpleDocTemplate(file_path)


    table_data = [data.column.tolist()] + data.fillna("").astype(str).values.tolist()

    table = Table(table_data)

    document.build([table])