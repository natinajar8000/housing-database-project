# Database of housing in the Netherlands for students
### Group 13

## What is this database about?

This database stores housing information of students located in the Netherlands. 

## How to run our database:

1. Have python 3.14.7 installed
2. Set .venv as the kernel for the project
3. Input your own username and password for MySQL
4. Depending on what you want to run:
5. Go to schema.sql
6. Run the file in order to create the tables

Housing database without integrated data (up to week 4):
1. Go to housing_database.ipynb
2. Edit the first cells with your own SQL account information
3. Run all the cells up to the desired one

Housing database with integrated data (after week 4):
1. Go to real_data_integration.ipynb
2. Edit the first cells with your own SQL account information
3. Run the file either up to the desired cell or just the whole file

7. Run the queries that you want through queries.ipynb

## Structure

```housing-database-project
├── ProductVideo.mov
├── README.md
├── data
│   ├── clean
│   │   ├── accommodation.csv
│   │   ├── address.csv
│   │   └── city.csv
│   └── raw
│       ├── duo_ingeschrevenen_hbo.csv
│       ├── duo_ingeschrevenen_wo.csv
│       └── kamernet_properties.json
├── erd_diagram.png
├── reports
│   ├── Student housing in the Netherlands.pdf
│   ├── assignment_1_report.pdf
│   └── assignment_2_report.pdf
├── scripts
│   └── map_real_data.py
└── sql_files
    ├── housing_database.ipynb
    ├── real_data_integration.ipynb
    └── schema.sql
```

## Notes on questions and queries

The queries provide an answer to our societal problem by showing actual records. Only by running the queries were we able to draw  conclusions. Running the queries shows the raw numbers which makes it later possible to formulate the answers. All questions above the queries are relevant to the problem, since they're all tackling availibility, low prices and satisfiability of the properties in the database.

## Normalization of the database

Since our database was normalized at the very start, it was not difficult to integrate the real databases. The normalization after integrating the data remained just as correct as in the report that can be found in the assignment_2_report.pdf. Instead of going through with the whole process again, firstly, the raw databases were cleaned and then modified to fit into our database. The changes made and variables added can be seen in "Notes on real data integration" section down below. They don't affect how normalised our database is at all.

## Notes on real data integration:

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

## Authors
The authors of this database are:
- Natalia Jarmakowska (natinajar8000)
- Hanna Serafin (h-a-n-i-a)
- Andrei Hoptiar (AndreiHoptiar)
- Kolja Nitschke (kolja079)