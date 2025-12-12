import requests
from dataclasses import dataclass
 
@dataclass
class Name:
    first: str
    last: str
 
@dataclass
class User:
    name: Name
    email: str
 
response = requests.get('https://randomuser.me/api/')
data = response.json()
# print(data)
user_data = data['results'][0]
name = Name(first=user_data['name']['first'], last=user_data['name']['last'])
user = User(name=name, email=user_data['email'])
print(f"Name: {user.name.first} {user.name.last}, Email: {user.email}")
 