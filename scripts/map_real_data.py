
import json
import re
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW, CLEAN = ROOT / "data" / "raw", ROOT / "data" / "clean"

SOURCES = {
    "kamernet_properties.json": "https://raw.githubusercontent.com/michael-william/Netherlands-Rental-Prices/master/data/properties.json",
    "duo_ingeschrevenen_wo.csv": "https://onderwijsdata.duo.nl/dataset/978f900e-088e-4d27-804f-2d897c161c70/resource/6a7e10c1-6ae8-4949-89da-b6e59151698c/download/ingeschrevenenwo.csv",
    "duo_ingeschrevenen_hbo.csv": "https://onderwijsdata.duo.nl/dataset/978f900e-088e-4d27-804f-2d897c161c70/resource/7761bd6a-b87b-4389-a943-829872116f92/download/ingeschrevenenhbo.csv",
}
# mapping lower to upper case cities
CITY_CODES = {
    "Maastricht": "MAASTRICHT", "Amsterdam": "AMSTERDAM", "Rotterdam": "ROTTERDAM",
    "Utrecht": "UTRECHT", "Den Haag": "DEN HAAG", "'s-Gravenhage": "DEN HAAG",
    "Eindhoven": "EINDHOVEN", "Groningen": "GRONINGEN", "Nijmegen": "NIJMEGEN",
    "Tilburg": "TILBURG", "Leiden": "LEIDEN",
}
# Kamernet propertyType = StudentPreference.accommodation_type
TYPES = {"Room": "room", "Studio": "studio", "Apartment": "apartment",
         "Anti-squat": "anti-kraak", "Student residence": "room"}


#subsidy approximation since we dont have real data on that  

LIBERALISATION_LIMIT_2019 = 720.42
ID_OFFSET = 1000  # keeps away from our mock data 


def download_missing():
    RAW.mkdir(parents=True, exist_ok=True)
    for name, url in SOURCES.items():
        if not (RAW / name).exists():
            print("downloading", name)
            urllib.request.urlretrieve(url, RAW / name)


def load_listings():
    rows = []
    with open(RAW / "kamernet_properties.json", encoding="utf-8") as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:  # mirror is truncated mid-record at the end
                pass
    df = pd.DataFrame(rows)
    df = df[df.city.isin(CITY_CODES) & df.propertyType.isin(TYPES)]
    # drop obvious junk (rent of 1 euro, 675 m2 "rooms", ...)
    df = df[df.rent.between(100, 5000) & df.areaSqm.between(6, 300)]
    return df.drop_duplicates("externalId")


def self_contained(r):
    return all(r.get(k) == "Own" for k in ("kitchen", "shower", "toilet"))


def build_tables(df, students):
    df = df.assign(
        city_code=df.city.map(CITY_CODES),
        street=df.title.str.strip().str[:61],
        zip_code=df.postalCode.str.replace(r"^(\d{4})([A-Z]{2})$", r"\1 \2", regex=True),
    )

    # Address 
    address = df[["city_code", "street", "zip_code"]].drop_duplicates().reset_index(drop=True)
    address.insert(0, "address_id", address.index + 1 + ID_OFFSET)
    address["house_number"] = pd.NA
    df = df.merge(address, on=["city_code", "street", "zip_code"])

    accommodation = pd.DataFrame({
        "accommodation_id": range(1 + ID_OFFSET, len(df) + 1 + ID_OFFSET),
        "landlord_id": pd.NA,  # private landlords no data available 
        "agency_id": pd.NA,
        "address_id": df.address_id.values,
        "subsidy_possible": [
            "yes" if self_contained(r) and r["rent"] <= LIBERALISATION_LIMIT_2019 else "no"
            for r in df.to_dict("records")
        ],
        "square_meters": df.areaSqm.astype(int).values,
        "rent_price": df.rent.astype(int).values,
        "accommodation_type": df.propertyType.map(TYPES).values,
        "furnished": df.furnish.replace("", pd.NA).values,
        "deposit": df.deposit.astype("Int64").values,
        "source_id": df.externalId.values,
    })

    per_city = df.assign(eur_sqm=df.rent / df.areaSqm).groupby("city_code")
    city = pd.DataFrame({
        "euro_sqm": per_city.eur_sqm.mean().round(2),
        "min_rent": per_city.rent.min().astype(float),
        "max_rent": per_city.rent.max().astype(float),
    }).join(students).reset_index()
    return city, address[["address_id", "city_code", "street", "house_number", "zip_code"]], accommodation


def load_students():
    duo = pd.concat(pd.read_csv(RAW / f, dtype={"STUDIEJAAR": int})
                    for f in ("duo_ingeschrevenen_wo.csv", "duo_ingeschrevenen_hbo.csv"))
    duo = duo[(duo.STUDIEJAAR == duo.STUDIEJAAR.max()) & duo.GEMEENTENAAM.isin(CITY_CODES)]
    print("DUO year used:", duo.STUDIEJAAR.max())
    return (duo.assign(city_code=duo.GEMEENTENAAM.map(CITY_CODES))
               .groupby("city_code").AANTAL_INGESCHREVENEN.sum()
               .rename("student_population"))


def check(city, address, accommodation):
    assert set(city.city_code) == set(CITY_CODES.values()), "a city has no data"
    assert city.student_population.gt(0).all()
    assert address.zip_code.str.fullmatch(r"\d{4} [A-Z]{2}").all()
    assert accommodation.address_id.isin(address.address_id).all()
    assert accommodation.accommodation_id.is_unique and address.address_id.is_unique
    assert set(accommodation.accommodation_type) <= set(TYPES.values())
    assert set(accommodation.subsidy_possible) <= {"yes", "no"}


if __name__ == "__main__":
    download_missing()
    city, address, accommodation = build_tables(load_listings(), load_students())
    check(city, address, accommodation)
    CLEAN.mkdir(parents=True, exist_ok=True)
    for name, t in [("city", city), ("address", address), ("accommodation", accommodation)]:
        t.to_csv(CLEAN / f"{name}.csv", index=False)
        print(f"{name}.csv: {len(t)} rows")
    print(city.to_string(index=False))
