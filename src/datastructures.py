
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        # example list of members
        self._members = [
            {
                "id": self._generateId(),
                "first_name": "John",
                "last_name": last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": self._generateId(),
                "first_name": "Jane",
                "last_name": last_name,
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": self._generateId(),
                "first_name": "Jimmy",
                "last_name": last_name,
                "age": 5,
                "lucky_numbers": [1]
            }
        ]

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        # fill this method and update the return
        #pass
        if 'id' not in member:
            member['id'] = self._generateId()
        member['last_name'] = self.last_name  # apellido siempre 'Jackson'

        # Validaciones 
        required_fields = ["first_name", "age", "lucky_numbers"]
        for field in required_fields:
            if field not in member:
                raise ValueError(f"Missing field: {field}")
        
        if not isinstance(member['age'], int) or member['age'] <= 0:
            raise ValueError("Age must be a positive integer.")
        
        if not isinstance(member['lucky_numbers'], list) or not all(isinstance(num, int) for num in member['lucky_numbers']):
            raise ValueError("Lucky numbers must be a list of integers.")

        self._members.append(member)
        return member


    def delete_member(self, id):
        # fill this method and update the return
        #pass
        initial_length = len(self._members)
        self._members = [member for member in self._members if member["id"] != id]
        if len(self._members) < initial_length:
            return {"done": True}
        return {"done": False}
    
    def get_member(self, id):
        # fill this method and update the return
       #pass
        for member in self._members:
            if member['id'] == id:
                return member
        return None

    def update_member(self, id, updated_member):
        for index, member in enumerate(self._members):
            if member['id'] == id:
                updated_member['last_name'] = self.last_name
                self._members[index].update(updated_member)
                return self._members[index]
        return None
    
    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
