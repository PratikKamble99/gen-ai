from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    is_active: bool = True # giving default value to field

input_1 = { "id": 1, "name": "pratik", "is_active": True}
input_2 = { "id": 1, "name": "pratik", "is_active": 21}

user_1 = User(**input_1)
# user_2 = User(**input_2) # This will throw validation error

print(user_1)