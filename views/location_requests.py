import sqlite3
import json
from models import Location, Employee, Animal

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]


def get_all_locations():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
           l.id,
           l.name,
           l.address
        FROM location l
        """)

        # Initialize an empty list to hold all location representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Location class above.
            location = Location(row['id'], row['name'], row['address'],
                                )

            # see the notes below for an explanation on this line of code.
            locations.append(location.__dict__)

    return locations


def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
                    SELECT
                        l.id,
                        l.name,
                        l.address
                    FROM location l
                    WHERE l.id = ?
                     """, (id, ))
        location_data = db_cursor.fetchone()

        location = Location(
            location_data['id'], location_data['name'], location_data['address'])

        db_cursor.execute("""
                    SELECT
                        e.id,
                        e.name,
                        e.address,
                        e.location_id
                    FROM employee e
                    WHERE e.location_id = ?
                     """, (id, ))
        employee_data = db_cursor.fetchall()

        for row in employee_data:
            employee = Employee(row['id'], row['name'],
                                row['address'], row['location_id'])
            location.employees.append(employee.__dict__)

        db_cursor.execute("""
                    SELECT
                        a.id,
                        a.name,
                        a.status,
                        a.breed,
                        a.customer_id,
                        a.location_id
                    FROM animal a 
                    WHERE a.location_id = ?
                     """, (id, ))
        animal_data = db_cursor.fetchall()

        for row in animal_data:
            animal = Animal(row['id'], row['name'],
                            row['status'], row['breed'], row['customer_id'], row['location_id'])
            location.animals.append(animal.__dict__)

        return location.__dict__


def delete_location(id):
  # Initial -1 value for location index, in case one isn't found
    location_index = -1

  # Iterate the LOCATIONS list, but use enumerate() so that you
  # can access the index value of each item
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Store the current index.
            location_index = index

    # If the location was found, use pop(int) to remove it from list
    if location_index >= 0:
        LOCATIONS.pop(location_index)


def update_location(id, new_location):
    # Iterate the LOCATIONS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Update the value.
            LOCATIONS[index] = new_location
            break
