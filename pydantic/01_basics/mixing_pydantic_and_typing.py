from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Dict, List, Optional

class Cart(BaseModel):
    user_id: int
    items: List[str]
    quantities: Dict[str, int]

class BlogPost(BaseModel):
    title: str
    content: str
    image_url: Optional[str] = None

class User(BaseModel):
    id: int
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Employee Name",
        examples="Pratik"
    )
    # email: str = Field(..., regex=r'')
    username: str
    username2: str
    password: str
    confirm_password: str

    @field_validator('username','username2')
    def username_length(cls, v):
        if(len(v) < 4):
            raise ValueError("Username must be at least 4 characters")
        return v
    
    # model validator have access to all values
    @model_validator(mode="after") # mode= allows you to set when this should run before or after field validation
    def password_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password does not match")
        return self


input = {"id":1, "name":"prat"}

# user = User(**input)
# print(user)

class Product(BaseModel):
    price: float
    quantity: int

    @computed_field
    @property
    def total_price(self) -> float:
        return self.price * self.quantity

product_input = {"price": 20, "quantity":3}
product_1 = Product(**product_input)

print(product_1)