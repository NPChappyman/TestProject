from pathlib import Path

import pandas as pd


def load_table(files: list[str]) -> pd.DataFrame:
    dataframes = []

    for file in files:
        path = Path(file)

        if not path.exists():
            raise FileNotFoundError(f"{path} не найден")

        if path.suffix == ".csv":
            current_df = pd.read_csv(path)

        elif path.suffix == ".xlsx":
            current_df = pd.read_excel(path)

        elif path.suffix == ".parquet":
            current_df = pd.read_parquet(path)

        else:
            raise ValueError(f"Неподдерживаемый формат: {path.suffix}")

        dataframes.append(current_df)

    return pd.concat(dataframes, ignore_index=True)