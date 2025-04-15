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
