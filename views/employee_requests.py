EMPLOYEES = [
  {
        "id": 1,
        "name": "Jenna Solis"
    },
  {
        "id": 2,
        "name": "Jenna Fischer"
    }
]

def get_all_employees():
  """Return all employees."""
  return EMPLOYEES

def get_single_employee(id):
  """Return a single employee."""
  requested_employee = None
  for employee in EMPLOYEES:
    if employee["id"] == id:
      requested_employee = employee
  return requested_employee
