

DROP TABLE IF EXISTS StudentPreference;
DROP TABLE IF EXISTS Contract;
DROP TABLE IF EXISTS Accommodation;
DROP TABLE IF EXISTS Landlord;
DROP TABLE IF EXISTS Agency;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Address;
DROP TABLE IF EXISTS City;

-- City table 
CREATE TABLE City(
    city_code VARCHAR(25) PRIMARY KEY,
    euro_sqm DECIMAL(10,2),
    min_rent DECIMAL(10,2),
    max_rent DECIMAL(10,2),
    student_population INT -- added for real data integration purposes
);

-- Student table
CREATE TABLE Student(
    student_id INT  PRIMARY KEY AUTO_INCREMENT,
    nationality VARCHAR(56),
    phone_number VARCHAR(15) NOT NULL UNIQUE, -- must include + in the beginning
    email VARCHAR(345) NOT NULL UNIQUE,
    max_rent DECIMAL(10,2),
    search_city_code VARCHAR(25),

     FOREIGN KEY (search_city_code)
        REFERENCES City(city_code)
);
-- Student Preference table
CREATE TABLE StudentPreference(
    student_id INT,
    accommodation_type VARCHAR(30),

    PRIMARY KEY (student_id, accommodation_type),

    FOREIGN KEY (student_id)
        REFERENCES Student(student_id)
);

-- Address table
CREATE TABLE Address(
    address_id INT PRIMARY KEY AUTO_INCREMENT,
    city_code VARCHAR(25),
    street VARCHAR(61),
    house_number SMALLINT(5), -- changed from NOT NULL to include NULL values for real data integration purposes
    zip_code VARCHAR(7), -- must include 4 numbers in the beginning, space and 2 letters at the end

    FOREIGN KEY (city_code)
        REFERENCES City(city_code)
);

-- Agency table
CREATE TABLE Agency(
    agency_id INT PRIMARY KEY AUTO_INCREMENT,
    address_id INT, 
    name VARCHAR(747) NOT NULL,
    phone_number VARCHAR(15) NOT NULL UNIQUE, -- must include + in the beginning
    email VARCHAR(345) NOT NULL UNIQUE,

    FOREIGN KEY (address_id)
        REFERENCES Address(address_id)
);

-- Landlord table
CREATE TABLE Landlord(
    landlord_id INT PRIMARY KEY AUTO_INCREMENT,
    agency_id INT,
    address_id INT,
    name VARCHAR(747) NOT NULL,
    phone_number VARCHAR(15) NOT NULL UNIQUE, -- must include + in the beginning
    email VARCHAR(345) NOT NULL UNIQUE,

    FOREIGN KEY (agency_id)
        REFERENCES Agency(agency_id),
    FOREIGN KEY (address_id)
        REFERENCES Address(address_id)
);

-- Accommodation table
CREATE TABLE Accommodation(
    accommodation_id INT PRIMARY KEY AUTO_INCREMENT,
    landlord_id INT, 
    agency_id INT,
    address_id INT,
    subsidy_possible CHAR(3), -- yes/no only
    square_meters SMALLINT(5) UNSIGNED, -- not null(?)
    rent_price SMALLINT(5) UNSIGNED, -- not null
    accomodation_type VARCHAR(30), -- added for real data integration purposes (e.g. room, studio, apartment)
    accomodation_furnished BOOL, -- added for real data integration purposes

    FOREIGN KEY (landlord_id)
        REFERENCES Landlord(landlord_id),
    FOREIGN KEY (agency_id)
        REFERENCES Agency(agency_id),
    FOREIGN KEY (address_id)
        REFERENCES Address(address_id)
);

-- Contract table
CREATE TABLE Contract(
    contract_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT, -- foreign key
    accommodation_id INT, -- foreign key
    start_date DATE,
    end_date DATE,
    min_duration INT,
    max_duration INT,
    cancellation_time DATE,
    deposit SMALLINT(5) UNSIGNED, -- can have a tag if its illegal
    CHECK (min_duration > 0),
    CHECK (max_duration >= max_duration) 

    FOREIGN KEY (student_id)
        REFERENCES Student(student_id),
    FOREIGN KEY (accommodation_id)
        REFERENCES Accommodation(accommodation_id)
);