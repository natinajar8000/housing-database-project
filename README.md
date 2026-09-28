# housing-database-project

### How to run our database:

1. Have python 3.14.7 installed

2. Set .venv as the kernel for the project

3. Input your own username and password for MySQL

4. Either run the whole code or up to the desired cell

## Real Data Integration

### Data used:

A) Kamernet listings, Jul 2019 - Mar 2020 (Kaggle: juangesino/netherlands-rent-properties).

- License
  - **CC BY 4.0**  Kaggle's dataset information (published: 2020-03-04)
  - https://github.com/michael-william/Netherlands-Rental-Prices/blob/master/data/properties.json**

B) DUO "Ingeschrevenen hoger onderwijs" (WO + HBO), CC-BY, onderwijsdata.duo.nl dataset p01hoinges.

- License:
  - **CC BY** DUO open data catalogue (publisher: DUO) (published 2023-03-23)
  - last updated(2026-04-08)
  - [https://onderwijsdata.duo.nl/dataset/p01hoinges](https://onderwijsdata.duo.nl/dataset/p01hoinges)

### Changes made to Database schema and constraints

- Added student_population to city
- Added accomodation_type to accomodation
- Added accomodation_furnished to Accomodation
