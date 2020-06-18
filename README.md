# TREE APP
This app is written in Python with Flask and SQLAlchemy, as a capstone project of the Udacity's Full Stack Web Developer Nanodegree program.

## Motivation for the project.
This project was inspired by my recent volunteering for a local charity Tree planting initiative. Native tree saplings are given away to anyone in the community, and the tree data is tracked for mapping and analysis.

## A. Dependency
In order to run this app, the following dependencies must have been already installed:
1. Postgres. 
 * Start manually: `pg_ctl -D /usr/local/var/postgres start`
 * Stop manually: `pg_ctl -D /usr/local/var/postgres stop -s -m fast`
 
2. Flask

## B. Database 
The database relations `todos(id, description, complete, list_id)` and `todolists(id, name)` must have been already created in Postgres. We have assumed that the Postgres is running on default port 5432.

* `dropdb todoapp -p 5432 && createdb todoapp -p 5432` 
* Open the database prompt - `psql -p 5432`
* Connect to the database - `\c todoapp` 
* Displays the tables in the database `\dt` 
* Displays the schema of the 'todos' table `\d todos` 
* Displays the schema of the 'todolists' table `\d todolists` 

You can insert a few rows in both the tables. Insert first in the `todolists` relation. 


## C. Steps to Run the App: 
* `python3 -m venv env` set the virtual environment for Pyhton 
* `source env/bin/activate` activate the venv
* `python -m pip install -r requirements.txt` to install dependencies. For Mac users, if you face difficulty in installing the `psycopg2`, you may consider intalling the `sudo brew install libpq` before running the `requirement.txt`. 
* `python3 app.py` to run the app (http://127.0.0.1:5000/ or http://localhost:5000)
* `deactivate` de-activate the virtual environment

##	Roles:
*	Assistant
*	Can view trees and owners
*	Admin user
*	All permissions a Asistant has and…
*	Add or delete an owner and tree from the database
*	Modify trees and owners


##API Reference for Tree APP
```sh
GET /trees
•	General:
    Returns a list of category trees, success value, and total number of trees.
        
•	Sample: curl http://127.0.0.1:5000/trees
{
  "success": true, 
  "total_trees": 6, 
  "trees": [
    {
      "id": 1, 
      "lat": 27.63864, 
      "long": -80.39727, 
      "owner_id": 1, 
      "planted_date": "Sun, 14 Jun 2020 00:00:00 GMT", 
      "type": "elm"
    }, 
    {
      "id": 3, 
      "lat": 25.5, 
      "long": -80.5, 
      "owner_id": 2, 
      "planted_date": "Tue, 16 Jun 2020 00:00:00 GMT", 
      "type": "elm"
    }, 
    {
      "id": 4, 
      "lat": null, 
      "long": null, 
      "owner_id": 1, 
      "planted_date": null, 
      "type": "maple"
    }, 
    {
      "id": 5, 
      "lat": 1.0, 
      "long": 4.5, 
      "owner_id": 1, 
      "planted_date": "Tue, 16 Jun 2020 00:00:00 GMT", 
      "type": "maple"
    }, 
    {
      "id": 8, 
      "lat": 33.749, 
      "long": 84.388, 
      "owner_id": 1, 
      "planted_date": "Tue, 16 Jun 2020 00:00:00 GMT", 
      "type": "mahogany"
    }, 
    {
      "id": 9, 
      "lat": 33.749, 
      "long": 84.388, 
      "owner_id": 1, 
      "planted_date": "Tue, 16 Jun 2020 00:00:00 GMT", 
      "type": "mahogany"
    }
  ]
}
GET /owners
•	General:
    Returns a list of owner objects, success value, and total number of owners
    
•	Sample: curl http://127.0.0.1:5000/owners
{
  "owners": [
    {
      "address": "Vero Beach, FL", 
      "first_name": "Bonnie", 
      "id": 1, 
      "last_name": "Shwartz", 
      "mail": "bonnie@me.com", 
      "phone": "772-222-3333"
    }, 
    {
      "address": "Sebastian, FL", 
      "first_name": "Ben", 
      "id": 2, 
      "last_name": "Tuts", 
      "mail": "ben@me.com", 
      "phone": "772-333-7777"
    }
  ], 
  "success": true, 
  "total_owners": 2
}

GET /owners/{owner_id}/trees
    General:
    Returns a list of trees which are owned by owner with the id = owner_id.
    
    Example:
$ curl http://127.0.0.1:5000/owners/2/trees
{
  "success": true, 
  "total_trees": 1, 
  "trees": [
    {
      "id": 3, 
      "lat": 25.5, 
      "long": -80.5, 
      "owner_id": 2, 
      "planted_date": "Tue, 16 Jun 2020 00:00:00 GMT", 
      "type": "elm"
    }
  ]
}

POST /trees
•	General:
    Creates a new tree using the submitted type, owner_id, lat, long and planted date. Tree type is Enum type with the following values: 
    live_oak,
    mahogany,
    bald_cypress,  
    maple,
    elm,
    other.
 Returns the id of the created tree, success value, total trees, and tree list.
 Example:
•	 curl -X POST http://127.0.0.1:5000/trees -H "Content-Type: application/json" --data '{"type":"maple","owner_id": "1","latitude": "33.7490", "longitude": "84.3880","plantedDate": "6-16-2020"}'
  {
  "created": 7,
  "success": true,
  "total_trees": 6,
  "trees": [
    {
      "id": 1,
      "lat": 27.63864,
      "long": -80.39727,
      "owner_id": 1,
      "planted_date": "Sun, 14 Jun 2020 00:00:00 GMT",
      "type": "live_oak"
    },
    {
      "id": 3,
      "lat": 25.5,
      "long": -80.5,
      "owner_id": 2,
      "planted_date": "Mon, 15 Jun 2020 00:00:00 GMT",
      "type": "elm"
    },
    {
      "id": 4,
      "lat": null,
      "long": null,
      "owner_id": 1,
      "planted_date": null,
      "type": "maple"
    },
    {
      "id": 5,
      "lat": 1.0,
      "long": 4.5,
      "owner_id": 1,
      "planted_date": "Tue, 16 Jun 2020 00:00:00 GMT",
      "type": "maple"
    },
    {
      "id": 6,
      "lat": 1.0,
      "long": 4.5,
      "owner_id": 1,
      "planted_date": "Tue, 16 Jun 2020 00:00:00 GMT",
      "type": "maple"
    },
    {
      "id": 7,
      "lat": 33.749,
      "long": 84.388,
      "owner_id": 1,
      "planted_date": "Tue, 16 Jun 2020 00:00:00 GMT",
      "type": "maple"
    }
  ]
}
DELETE /trees/{tree_id}
•	General:
    Deletes the tree of the given ID if it exists. Returns the id of the deleted tree, success value, total trees, and tree list 
•	curl -X DELETE http://127.0.0.1:5000/trees/6
{
  "deleted": "6",
  "success": true,
  "total_trees": 4,
  "trees": [
    {
      "id": 1,
      "lat": 27.63864,
      "long": -80.39727,
      "owner_id": 1,
      "planted_date": "Sun, 14 Jun 2020 00:00:00 GMT",
      "type": "live_oak"
    },
    {
      "id": 3,
      "lat": 25.5,
      "long": -80.5,
      "owner_id": 2,
      "planted_date": "Mon, 15 Jun 2020 00:00:00 GMT",
      "type": "elm"
    },
    {
      "id": 4,
      "lat": null,
      "long": null,
      "owner_id": 1,
      "planted_date": null,
      "type": "maple"
    },
    {
      "id": 5,
      "lat": 1.0,
      "long": 4.5,
      "owner_id": 1,
      "planted_date": "Tue, 16 Jun 2020 00:00:00 GMT",
      "type": "maple"
    }
  ]
}

PATCH /trees/{tree_id}
Updates the tree object with id= tree_id with specified values. Only values for type and platedDate are modifiable.
 curl -X PATCH http://127.0.0.1:5000/trees/3 -H "Content-Type: application/json" --data '{"plantedDate": "6-16-2020"}'
  {
  "success": true,
  "trees": [
    {
      "id": 1,
      "lat": 27.63864,
      "long": -80.39727,
      "owner_id": 1,
      "planted_date": "Sun, 14 Jun 2020 00:00:00 GMT",
      "type": "live_oak"
    },
    {
      "id": 4,
      "lat": null,
      "long": null,
      "owner_id": 1,
      "planted_date": null,
      "type": "maple"
    },
    {
      "id": 5,
      "lat": 1.0,
      "long": 4.5,
      "owner_id": 1,
      "planted_date": "Tue, 16 Jun 2020 00:00:00 GMT",
      "type": "maple"
    },
    {
      "id": 3,
      "lat": 25.5,
      "long": -80.5,
      "owner_id": 2,
      "planted_date": "Tue, 16 Jun 2020 00:00:00 GMT",
      "type": "elm"
    }
  ]
}
```
##Error Handling
```sh
Errors are returned as JSON objects in the following format:
{
            'success': False,
            'error':404,
            'message': 'resource not found'

}
The API will return these type of errors:
- 400 : 'Bad Request'
- 404 : 'resource not found'
- 422 : 'unprocessable'
- 405 : 'method not allowed'
- 500 : 'Internal Server Error'
```

## Testing
```sh
To run the tests, run :
	python test_app.py

```

