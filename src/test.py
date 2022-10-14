from Database import Database

db = Database('./record.db', False)
print(db.getByAttribute(record_type='sickness', patient_id='usr1'))