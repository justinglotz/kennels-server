import sqlite3
import json
from models import Animal

ANIMALS = [
    {
        "id": 1,
        "name": "Snickers",
        "species": "Dog",
        "locationId": 1,
        "animalId": 4,
        "status": "Admitted"
    },
    {
        "id": 2,
        "name": "Roman",
        "species": "Dog",
        "locationId": 1,
        "animalId": 2,
        "status": "Admitted"
    },
    {
        "id": 3,
        "species": "Cat",
        "locationId": 2,
        "animalId": 1,
        "status": "Admitted"
    }
]


def get_all_animals():
    # Open a connection to the rowbase
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.animal_id
        FROM animal a
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of row into a Python list
        rowset = db_cursor.fetchall()

        # Iterate list of row returned from rowbase
        for row in rowset:

            # Create an animal instance from the current row.
            # Note that the rowbase fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['animal_id'])

            # see the notes below for an explanation on this line of code.
            animals.append(animal.__dict__)

    return animals

# Function with a single parameter


def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.animal_id
        FROM animal a
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        row = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(row['id'], row['name'], row['breed'],
                        row['status'], row['location_id'],
                        row['animal_id'])

        return animal.__dict__


def create_animal(animal):
    # Get the id value of the last animal in the list
    max_id = ANIMALS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    animal["id"] = new_id

    # Add the animal dictionary to the list
    ANIMALS.append(animal)

    # Return the dictionary with `id` property added
    return animal


def delete_animal(id):
    """Deletes an animal

    Args:
        id (integer): The id being accessed
    """
    # Initial -1 value for animal index, in case one isn't found
    animal_index = -1

# Iterate the ANIMALS list, but use enumerate() so that you
# can access the index value of each item
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            # Found the animal. Store the current index.
            animal_index = index

    # If the animal was found, use pop(int) to remove it from list
    if animal_index >= 0:
        ANIMALS.pop(animal_index)


def update_animal(id, new_animal):
    """Updates an animal object

    Args:
        id (integer): Id of the animal to update
        new_animal (object): The object to pass in to the udpate
    """
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            # Found the animal. Update the value.
            ANIMALS[index] = new_animal
            break


def get_animal_by_location(location_id):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.status,
            c.breed,
            c.customer_id,
            c.location_id
        from Animal c
        WHERE c.location_id = ?
        """, (location_id, ))

        animals = []
        rowset = db_cursor.fetchall()

        for row in rowset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)

    return animals


def get_animal_by_status(status):

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.status,
            c.breed,
            c.customer_id,
            c.location_id
        from Animal c
        WHERE c.status = ?
        """, (status, ))

        animals = []
        rowset = db_cursor.fetchall()

        for row in rowset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)

    return animals
