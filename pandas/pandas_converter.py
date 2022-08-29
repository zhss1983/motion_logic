import pandas as pd


def convert_json_csv():
    with open("test.json", encoding="utf-8") as inputfile:
        df = pd.read_json(inputfile)
    df.to_csv("test.csv", encoding="utf-8", index=False)
    print(df)


def unicle_owners():
    df = pd.read_csv("test.csv")
    for owner in df["owner"].unique():
        print(f"Рестораны компании", owner + ":", len(df[df["owner"] == owner]))


if __name__ == "__main__":
    convert_json_csv()
    unicle_owners()
