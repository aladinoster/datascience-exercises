"""
Data Cleaning
=============
"""

import pandas as pd
from pathlib import Path

def load_data():
    p = Path(".") / "data"
    p = p.resolve()
    files = [f for f in p.glob("*DRS.csv")]
    dfs = [pd.read_csv(f, sep=";") for f in files]
    return dict(zip(files,dfs))

def clean_data(df: pd.DataFrame):
    cols = [
        "Date",
        "Heure",
        "Etat",
        "Mnémonique",
        "Train",
        "Loc1",
        "Loc2",
        "vr_cpresssuspetf1_air",
    ]
    df_clean = df[cols]
    codes = [
        "F_DRS_PerteMaintienSup12",
        "F_DRS_DefautPorte",
        "F_DRS_DefautPorteGeneral",
        "F_DRS_DefautPorteTresLente",
    ]
    df_clean = df_clean[df_clean["Mnémonique"].isin(codes)]
    code_mapper = ["Pressure", "Door", "DoorGeneral", "SlowDoor"]
    code_mapper = dict(zip(codes, code_mapper))
    loc1 = {
        "Train": "T",
        "ZRBxp": "C1",
        "ZB": "C2",
        "ZAB": "C3",
        "ZBx": "C4",
        "ZRBxi": "C5",
    }
    col_mapper = {
                "Etat": "State",
                "Heure": "Hour",
                "Mnémonique": "code",
                "Loc1": "CarNumber",
                "Loc2": "Equipement",
                "vr_cpresssuspetf1_air": "Pressure",
            }
    df_clean["Train"] = (
        (df_clean["Train"] - 3600).astype("string").apply(lambda x: x + "TR_")
    )
    return (
        df_clean.replace(code_mapper).replace(loc1).rename(columns=col_mapper)
    )

def save_data(data, file_n):
    data.to_csv(f"data/file_{i}.csv")


if __name__ == "__main__":

    ldf = load_data()
    pdf = list(map(clean_data, ldf.values()))
    for i, df in enumerate(pdf):
        save_data(df, i)

