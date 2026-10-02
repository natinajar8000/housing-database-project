# housing-database-project

### How to run our database:

1. Have python 3.14.7 installed
2. Set .venv as the kernel for the project
3. Input your own username and password for MySQL
4. Run the whole code or up to the desired cell in housing_database.ipynb
5. After running housing_database.ipynb you can populate database with real data in real_data_integration.ipynb (mock data from previous assignmnets is kept on beggining indexes while real data is added after that)

## Real Data Integration

### Data used:

A) Kamernet listings, Jul 2019 - Mar 2020 (Kaggle: juangesino/netherlands-rent-properties).

* https://github.com/michael-william/Netherlands-Rental-Prices/blob/master/data/properties.json**

- License
  - **CC BY 4.0**  Kaggle's dataset information (published: 2020-03-04)

B) DUO "Ingeschrevenen hoger onderwijs" (WO + HBO), CC-BY, onderwijsdata.duo.nl dataset p01hoinges.

- last updated(2026-04-08)
- https://onderwijsdata.duo.nl/dataset/p01hoinges
- License:

  - **CC BY** DUO open data catalogue (publisher: DUO) (published 2023-03-23)

C) AI genarated data for students, landlords, contracts and agiencies since we dont have access to personal data. It was added to maintain completenes of data and ensure smooth querring. Its clearly labeled as ai mock. To create them we used an ai generated python script.

### Changes made to Database schema and constraints

- Added student_population to city
- Added accomodation_type to accomodation
- Added accomodation_furnished (BOOL) to Accomodation
