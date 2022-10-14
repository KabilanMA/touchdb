import os
import sys
import signal
import json
import uuid
from threading import Thread
from .Exceptions import NoValueError


class Connector(object):
    
    key_string_error = TypeError('Custom type error occured')
    invalid_input_value = NoValueError('No value/Invalid is provided to insert')
    
    def __init__(self, location, auto_dump, sig=True):
        '''
        :params:location: Directory location of the database file.
        :params:auto_dump: Whether to automatically dump the data or wait for manual dump action.
        '''
        self.load(location, auto_dump)
        self.dthread = None
        if sig:
            self.set_sigterm_handler()
    
    def __getitem__(self, item):
        return self.get(item)
    
    def __setitem__(self, key, value):
        return self.set(key, value)
    
    def __delitem__(self, key):
        return self.rem(key)
    
    def set_sigterm_handler(self):
        def sigterm_handler():
            if self.dthread is not None:
                self.dthread.join()
            sys.exit(0)
        signal.signal(signal.SIGTERM, sigterm_handler)
        
    def load(self, location, auto_dump):
        '''Force the database to read the data from the database file into the memory
        :params: location: Location to the .db database file.
        :params: auto_dump: boolean value, if set to True automatically dump the data after each update or insertion. If set to False have to dump the data after each update or insertion manually.'''
        
        location = os.path.expanduser(location)
        self.loco = location
        self.auto_dump = auto_dump
        if os.path.exists(location):
            self._loaddb()
        else:
            self.db = {}
        return True
    
    def dump(self):
        '''dump the data in the memory into the database file'''
        
        self.dthread = Thread(target=json.dump, args=(self.db, open(self.loco, 'w')), kwargs={'indent':4})
        self.dthread.start()
        self.dthread.join()
        return True
    
    def _loaddb(self):
        try:
            with open(self.loco, 'r') as dataRecord:
                self.db = json.load(dataRecord)
        except ValueError:
            if os.stat(self.loco).st_size == 0:
                self.db = {}
            else:
                raise # File is not empty, avoid overwriting it
    
    def _autodumpdb(self):
        if self.auto_dump:
            self.dump()
            
    
    def insert(self, **kwargs):
        '''
        Insert the python dictionary data into the database.
        :params: key - optional: Key of the value to be stored in the database. If not provided a random value will be assigned.
        :params: value: dict: A python dictionary to be inserted into the database.
        '''
        
        try:
            key = kwargs['key']
        except KeyError:
            key = uuid.uuid1()
        
        try:
            value = kwargs['value']
            if not isinstance(value, dict):
                raise self.invalid_input_value
        except KeyError:
            raise self.invalid_input_value
        except NoValueError:
            return False
        
        self._append(key, value)
        return key
        
    def get(self, key):
        '''Get the data from the database using the key'''
        try:
            return self.db[key]
        except KeyError:
            return False
    
    def getAll(self):
        '''Get all the data in the database as JSON format(python dictionary)'''
        return self.db
    
    def getByAttribute(self, **kwargs):
        '''Attribute of the record will be checked with the provided values and return the list of mapping data in the database'''
        
        keys = list(kwargs.keys())
        result = []
        for keyi in self.db:
            IN = False
            for keyj in self.db[keyi]:
                if keyj in keys:
                    if kwargs[keyj] == self.db[keyi][keyj]:
                        IN = True
                    else:
                        IN = False
                        break
            if IN:
                result.append(self.db[keyi])
                
        return result
        
    def exists(self, key):
        '''Check if a key exists in the database'''
        return key in self.db
    
    def remove(self, key):
        '''Remove a particular data mapping to the key in the database'''
        if not key in self.db:
            return False
        del self.db[key]
        self._autodumpdb()
        return True
    
    def removeByAttribute(self, **kwargs):
        '''remove all data records in the database which correlate to the attribute value'''
        
        keys = list(kwargs.keys())
        for keyi in self.db:
            IN = False
            for keyj in self.db[keyi]:
                if keyj in keys:
                    if kwargs[keyj] == self.db[keyi][keyj]:
                        IN = True
                    else:
                        IN = False
                        break
            if IN:
                del self.db[keyi]
        self._autodumpdb()
        return True    
        
    
    def totalkeys(self, key=None):
        '''If the parameter key is not provided return the total number of keys in the database, but if the key is provided return the number of data records inside that particular dictionary'''
        
        if key is None:
            total = len(self.db)
            return total
        else:
            total = len(self.db[key])
            return total
    
    def _append(self, key, value:dict):
        self.db[key] = value
        self._autodumpdb()
        return True
        
    def add(self, key, value:dict):
        '''Add a new key-value pair to the existing data record with key as provided'''
        
        key_list = []
        try:
            for key_val in value:
                self.db[key][key_val] = value[key_val]
                key_list.append(key_val)
            self._autodumpdb()
            return True
        except KeyError:
            for key_val in key_list:
                del self.db[key][key_val]
            return False
        
        
    def extend(self, datas:dict):
        '''Extend the database with the provided dictionary data'''
        success = False
        for key in datas:
            if isinstance(datas[key], dict):
                self.db[key] = datas[key]
                success = True
            else:
                success = False
                break
        if success:
            self._autodumpdb()
            return True
        else:
            allKeysToBeRemoved = list(datas.keys())
            for key in allKeysToBeRemoved:
                try:
                    del self.db[key]
                except KeyError:
                    continue
            return False

    def deldb(self):
        '''Delete the database from both memory and file.'''
        
        self.db = {}
        self._autodumpdb()
        return True             