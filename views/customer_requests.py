CUSTOMERS = [
  {
        "id": 1,
        "name": "Randy Marsh"
    },
  {
        "id": 2,
        "name": "Stan Marsh"
    }
]

def get_all_customers():
  """Return all customers."""
  return CUSTOMERS

def get_single_customer(id):
  """Return a single customer."""
  requested_customer = None
  for customer in CUSTOMERS:
    if customer["id"] == id:
      requested_customer = customer
  return requested_customer


def create_customer(customer):
    # Get the id value of the last animal in the list
    max_id = CUSTOMERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    customer["id"] = new_id

    # Add the animal dictionary to the list
    CUSTOMERS.append(customer)

    # Return the dictionary with `id` property added
    return customer

  