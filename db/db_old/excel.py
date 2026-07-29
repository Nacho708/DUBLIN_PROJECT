import pandas as pd


def read_excel(file, sheet_name=0):

    df = pd.read_excel(
        file,
        sheet_name=sheet_name
    )

    return df