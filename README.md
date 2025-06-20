# TODO-API
A simple API that allows authenticated users to create, update, delete TODO items.  

## Tech Stack Used
- Python
- Django
- Django Rest Framework
- Sqlite3 (Database)

## Features
- Register a new user
- Login the user
- Create a TODO item
- Update a TODO item
- Delete a TODO item
- Fetch TODO items using pagination

## Installation
1. Clone this repository
```
git clone https://github.com/apigituser/todo-api
```
2. Install the requirements
```
pip install -r requirements.txt
```
3. Run migrations to create the tables
```
python manage.py migrate
```
4. Run the API
```
python manage.py runserver
```

## Recommended API software
Install an API development software like Postman or Insomnia to interact with the API  

## Using the Token
Add the Token received in the Authorization header. For example  
```
Authorization: Token <token>
```

## Roadmap.sh Project URL
Project link is available [here](https://roadmap.sh/projects/todo-list-api)
