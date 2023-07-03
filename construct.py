import pandas as pd
import click
from pathlib import Path
import json
import requests

# Turn off nag about chained asignment since I'm not doing it
pd.options.mode.chained_assignment = None  # default='warn'


@click.command()
@click.argument("cube", type=click.Path(exists=True, path_type=Path))
def construct(cube: Path()) -> None:
    qube_config = json.load(cube.open())

    # hacky
    # df_dict = pd.read_excel("totalpspreferencetables2020.xlsx", sheet_name=["3", "5", "7"])

    r = requests.get(qube_config["source"])

    df_dict = pd.read_excel(r.content, sheet_name=["3", "5", "7"])

    df_cube = pd.DataFrame()

    # 3 "Quality Adjusted Productivity"; Titles: Row 4, Units 5
    df = df_dict["3"]
    measure = "Quality Adjusted Productivity"
    if measure in df.columns[0]:
        df = df[4:]

        df.columns = [
            "Year",
            "Healthcare",
            "Education",
            "Adult Social Care",
            "Social Security Administration",
            "Children's Social Care",
            "Public Order & Safety",
            "Police",
            "Defence",
            "Other",
            "Total",
            "Total Quality Adjustment Index",
        ]

        df = df.melt(id_vars="Year", var_name="Service Area", value_name="obs")

        df["measure"] = measure + " Index (1997 base)"

        df_cube = pd.concat([df_cube, df])
    else:
        raise ValueError(f"Worksheet \"{measure}\" expected but not found.")

    # 5 "Quality Adjusted Output"; Titles: Row 4, Units 5
    df = df_dict["5"]
    measure = "Quality Adjusted Output"
    if measure in df.columns[0]:
        df = df[4:]

        df.columns = [
            "Year",
            "Healthcare",
            "Education",
            "Adult Social Care",
            "Social Security Administration",
            "Children's Social Care",
            "Public Order & Safety",
            "Police",
            "Defence",
            "Other",
            "Total",
            "Total Quality Adjustment Index",
        ]

        df = df.melt(id_vars="Year", var_name="Service Area", value_name="obs")

        df["measure"] = measure + " Index (1997 base)"

        df_cube = pd.concat([df_cube, df])
    else:
        raise ValueError(f"Worksheet \"{measure}\" expected but not found.")

    # 7 "Input Indicies"; Titles: Row 3, Units 4
    df = df_dict["7"]
    measure = "Input Indices"
    if measure in df.columns[0]:
        df = df[4:]

        df.columns = [
            "Year",
            "Healthcare",
            "Education",
            "Adult Social Care",
            "Social Security Administration",
            "Children's Social Care",
            "Public Order & Safety",
            "Police",
            "Defence",
            "Other",
            "Total",
        ]

        df = df.melt(id_vars="Year", var_name="Service Area", value_name="obs")

        df["measure"] = measure + " Index (1997 base)"

        df_cube = pd.concat([df_cube, df])
    else:
        raise ValueError(f"Worksheet \"{measure}\" expected but not found.")

    df_cube.to_csv(cube.stem + ".csv", index=False)

    return


if __name__ == "__main__":
    construct()
