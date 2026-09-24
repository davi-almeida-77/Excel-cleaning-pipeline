import pandas as pd
from pathlib import Path


BASE = Path(__file__).resolve().parent

RAW = BASE / "data" / "raw"

df = pd.read_excel(RAW / "sales_january_2026.xlsx", header=5)

canonical_map = {
    "Order": "order",
    "Date": "date",
    "Customer": "customer",
    "Product" : "product",
    "Qty": "quantity",
    "Unit Price": "unit_price",
    "Total": "total",    
}

FORMATS = [
    "%B %d, %Y",
    "%d-%b-%Y",
    "%d/%m/%Y",
    "%Y-%m-%d",
]


df = df.rename(columns=canonical_map)

def parse_date(raw):

    if pd.isna(raw):
        return pd.NaT, "empty"

    if isinstance(raw, (int, float)):
        return pd.to_datetime(raw, unit="D", origin="1899-12-30"), None

    s = str(raw).strip()

    for fmt in FORMATS:
        try:
            return pd.to_datetime(s, format=fmt), None
        except ValueError:
            continue

    if s.isdigit():
        return pd.to_datetime(float(s), unit="D", origin="1899-12-30"), None

    return pd.NaT, "unrecognized format"

df["date_raw"] = df["date"]
result = df["date"].apply(parse_date)
df["date"] = result.apply(lambda t: t[0])
df["date_error"] = result.apply(lambda t: t[1])

print(df[["order", "date_raw", "date", "date_error"]].head(20))


print(f"Total: {len(df)}")
print(f"Parsed: {df['date'].notna().sum()}")
print(df[df["date_error"].notna()][["order", "date_raw", "date_error"]])