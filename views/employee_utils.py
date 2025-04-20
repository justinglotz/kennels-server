def is_valid_employee(employee):
    if not isinstance(employee, dict):
        return False
    if "id" not in employee or "name" not in employee:
        return False
    if not isinstance(employee["id"], int):
        return False
    if not isinstance(employee["name"], str) or not employee["name"].strip():
        return False
    return True
