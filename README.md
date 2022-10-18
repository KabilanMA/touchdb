[![Downloads](https://static.pepy.tech/personalized-badge/touchdb?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Reached)](https://pepy.tech/project/touchdb)

touchdb is a simple document based nosql database built entirely on python. This save the data input which is in python dictionary into a JSON data in a .db file.
There are only limited number of functionalities that are implemented in the engine but they are more than sufficient to handle normal database queries.
<br>
## Find Me

<ul>
    <li><a href="https://github.com/KabilanMA/touchdb">GitHub</a></li>
    <li><a href="https://pypi.org/manage/project/touchdb">PyPI</a></li>
    <li><a href="https://kabilanma.github.io/touchdb/">Website</a></li>
</ul>

## Installation
Easy to install in your projects using pip.<br>
`pip install touchdb`
<br>
## Usage

```python
>>> from touchdb import Database
>>> db = Database.Connector('./record.db', True)
>>> print(db.getByAttribute(record_type='sickness', patient_id='usr1'))

```
## List of functions

1. `load(location, auto_dump)` : Force the database to load the database from the database file into the memory.<br>
2. `dump()` : Dump the data in the memory into the database file.<br>
3. `insert(**kwargs)` : Insert the python dictionary data into the database. `key - optional` parameter which provide the key for the value to be inserted. `value` is python `dict` to be inserted into the database.<br>
4. `get(key)` : Get the data from the database using the key.<br>
5. `getAll()` : Get all the data in the database as JSON format(python dictionary).<br>
6. `getByAttribute(**kwargs)` : Attribute of the record will be checked with the provided values and return the list of mapping data in the database.<br>
7. `exists(key)` : Check if a key exists in the database.<br>
8. `remove(key)` : Remove a particular data mapping to the key in the database.<br>
9. `removeByAttribute(**kwargs)` : Remove all data records in the database which correlate to the attribute value.<br>
10. `totalkeys(key=None)` : If the parameter key is not provided return the total number of keys in the database, but if the key is provided return the number of data records 11. inside that particular dictionary.<br>
12. `add(key, value:dict)` : Add a new key-value pair to the existing data record with key as provided.<br>
13. `extend(datas: dict)` : Extend the database with the provided dictionary data.<br>
14. `deldb()` : Delete the database from both memory and file.<br>
<br>
<br>

## Sample Data
A sample data record file is given below for testing purpose.

```json
{
    "894a9a5d-46e8-11ed-b600-b526d12bcc50": {
        "patient_id": "usr1",
        "patient_name": "James",
        "record_type": "sickness",
        "sens_level": 4,
        "data": "<THIS IS THE ACTUAL DATA TO BE STORED IN THE DATABASE>"
    },
    "69840102-479e-11ed-97ec-b526d12bcc50": {
        "patient_id": "usr6",
        "patient_name": "Kabilan",
        "record_type": "sickness",
        "sens_level": 3,
        "data": "THIS IS A DUMMY SICKNESS DATA FOR NEW USER"
    },
    "4e4f3d76-47b0-11ed-8752-b526d12bcc50": {
        "patient_id": "usr7",
        "patient_name": "Levi Ackerman",
        "record_type": "drug_prescription",
        "sens_level": 3,
        "data": "THIS IS A DUMMY DRUG PRESCRIPTION DATA RECORD FOR TESTING"
    }
}
```

<br>

## A few example code

```python
from touchdb import Database

db = Database.Connector('./record.db', True)
db.insert(value={'test_id':"test123"})
print(db.get(key='cf9a67ed-4bf6-11ed-9284-b72b6fa7f086'))
print(db.getAll())
print(db.getByAttribute(record_type='sickness'))
print(db.exists(key='cf9a67ed-4bf6-11ed-9284-b72b6fa7f086'))
print(db.remove(key='cf9a67ed-4bf6-11ed-9284-b72b6fa7f086'))
print(db.removeByAttribute(record_type='sickness'))
print(db.totalkeys())
print(db.totalkeys(key='69840102-479e-11ed-97ec-b526d12bcc50'))
print(db.add('4e4f3d76-47b0-11ed-8752-b526d12bcc50', {'address':'Eldian Kingdom', 'Kill count':'inf+'}))

```
