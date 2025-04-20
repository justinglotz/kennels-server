import unittest
from employee_requests import EMPLOYEES, update_employee
from employee_utils import is_valid_employee


class TestUpdateEmployee(unittest.TestCase):

    def setUp(self):
        EMPLOYEES.clear()
        EMPLOYEES.extend([
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
        ])

# Functional Tests
    def test_update_existing_employee(self):
        update_employee(2, {"id": 2, "name": "Robert"})
        self.assertEqual(EMPLOYEES[1]["name"], "Robert")

    def test_update_nonexistent_employee(self):
        update_employee(3, {"id": 3, "name": "Charlie"})
        self.assertEqual(len(EMPLOYEES), 2)  # No change

    def test_update_with_invalid_employee_data(self):
        with self.assertRaises(ValueError):
            update_employee(2, {"name": "No ID"})

# Validation Tests

    def test_valid_employee_passes(self):
        self.assertTrue(is_valid_employee({"id": 1, "name": "Test"}))

    def test_invalid_employee_missing_id(self):
        self.assertFalse(is_valid_employee({"name": "No ID"}))

    def test_invalid_employee_wrong_types(self):
        self.assertFalse(is_valid_employee({"id": "not an int", "name": 123}))


if __name__ == '__main__':
    unittest.main()
