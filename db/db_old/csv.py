import csv

import pandas as pd
from charset_normalizer import from_path


def read_csv(file):

    encoding = from_path(file).best().encoding

    with open(file, encoding=encoding) as f:

        sample = f.read(5000)

        delimiter = csv.Sniffer().sniff(sample).delimiter

    df = pd.read_csv(
        file,
        sep=delimiter,
        encoding=encoding
    )

    return df