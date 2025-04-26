import sqlite3
import json
from models import Animal, Location, Customer

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
                a.customer_id,
                l.name location_name,
                l.address location_address,
                c.name customer_name,
                c.address customer_address,
                c.email customer_email
            FROM Animal a
            JOIN Location l
                ON l.id = a.location_id
            JOIN Customer c
                on c.id = a.customer_id
        """)

        # Initialize an empty list to hold all animal representations
        animals = []

        # Convert rows of row into a Python list
        rowset = db_cursor.fetchall()

        # Iterate list of row returned from rowbase
        for row in rowset:

            # Create an animal instance from the current row
            animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                            row['location_id'], row['customer_id'])

            # Create a Location instance from the current row
            location = Location(row['location_id'], row['location_name'],
                                row['location_address'])

            # Create a Customer instance from the current row
            customer = Customer(row['customer_id'], row['customer_name'],
                                row['customer_address'], row['customer_email'])

        # Add the dictionary representation of the location to the animal
            animal.location = location.to_dict()
            animal.customer = customer.to_dict()
        # Add the dictionary representation of the animal to the list
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
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, (id, ))

        # Load the single result into memory
        row = db_cursor.fetchone()

        # Create an animal instance from the current row
        animal = Animal(row['id'], row['name'], row['breed'],
                        row['status'], row['location_id'],
                        row['customer_id'])

        return animal.__dict__


def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['location_id'],
              new_animal['customer_id'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_animal['id'] = id

    return new_animal


def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
            DELETE FROM animal
            WHERE id = ?
            """, (id, ))


def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['locationId'],
              new_animal['customerId'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True


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


def search_for_animals(term):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # This is where we format this term for use in a search SQL query
        search_query = f"%{term}%"

        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.breed,
            c.status,
            c.location_id,
            c.customer_id
        from Animal c
        WHERE c.name LIKE ?
        """, (search_query, ))

        rowset = db_cursor.fetchall()
        animals = []

        for row in rowset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)

    return animals
