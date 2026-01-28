from pydantic import BaseModel, ConfigDict
import datetime
class Address(BaseModel):
    street: str
    city: str
    postal_code: str

class User(BaseModel):
    id: int
    name: str
    address: Address
    created_at: datetime

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={datetime: lambda v: v.strftime('%d-%m-%y %H:%M:%S')}
    )

address = Address(
    street="pashan road",
    city="Pune",
    postal_code="102"
)

user_1 = User(
    id=1,
    name="pratik",
    created_at=datetime.datetime(2026, 1, 28, 20, 30),
    address=address
)

print(user_1.model_dump())

input_data = {
     "id":2,
    "name":"Aakash",
    "created_at": datetime.datetime(2026, 1, 28),
    "address":{
        "street":"pashan road",
        "city":"Pune",
        "postal_code":"102"
    }
}

user_2 = User(**input_data)

print(user_2.model_dump())
print(user_2.model_dump_json())