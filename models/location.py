class Location():
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address
        self.employees = []
        self.animals = []

    def to_dict(self):
        return {
            "name": self.name,
            "address": self.address
        }
