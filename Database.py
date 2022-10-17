import os
import sys
import signal
import json
import uuid
from threading import Thread
from .Exceptions import NoValueError
from .Exceptions import NotImplementedError
from ast import literal_eval

class Connector(object):
    
    key_string_error = TypeError('Custom type error occured')
    invalid_input_value = NoValueError('No value/Invalid is provided to insert')
    not_implemented = NotImplementedError('Not implemented')
    
    def __init__(self, location, auto_dump, sig=True):
        '''
        :params:location: Directory location of the database file.
        :params:auto_dump: Whether to automatically dump the data or wait for manual dump action.
        '''
        self.load(location, auto_dump)
        self.dthread = None
        self.temp_data = {}
        
        if sig:
            self.set_sigterm_handler()
    
    def __getitem__(self, item):
        raise self.not_implemented
    
    def __setitem__(self, key, value):
        raise self.not_implemented
    
    def __delitem__(self, key):
        raise self.not_implemented
    
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
            self.keys = []
            with open(self.loco, 'w') as file:
                file.write('{\n}')
        return True
    
    def _loaddb(self):
        try:
            with open(self.loco, 'r') as dataRecord:
                self.keys = list(json.load(dataRecord).keys())
        except ValueError:
            if os.stat(self.loco).st_size == 0:
                with open(self.loco, 'w') as file:
                    file.write('{\n}')
                self.keys = []
            else:
                raise # File is not empty, avoid overwriting it
        
    def _dump(self):
        with open(self.loco, 'r+') as dataFile:
            recordData = literal_eval(dataFile.read())
            for key in self.temp_data:
                dataFile.seek(0,2)
                dataFile.seek(dataFile.tell() - 3)
                
                if len(recordData) ==0:
                    dataFile.write('\n    "{}": '.format(key))
                else:
                    dataFile.write(',\n    "{}": '.format(key))
                    
                json.dump(self.temp_data[key], dataFile, indent=8)
                dataFile.seek(dataFile.tell() - 1)
                dataFile.write('    }\n}')
        self.temp_data = {}
            
    def dump(self):
        '''dump the data in the memory into the database file'''
        
        self.dthread = Thread(target=self._dump)
        self.dthread.start()
        self.dthread.join()
        return True
    
    def _autodumpdb(self):
        if self.auto_dump:
            self.dump()
             
    def insert(self, value=None, **kwargs):
        '''
        Insert the python dictionary data into the database.
        :params: key - optional: Key of the value to be stored in the database. If not provided a random value will be assigned.
        :params: value: dict: A python dictionary to be inserted into the database.
        '''
        
        try:
            key = kwargs['key']
        except KeyError:
            key = str(uuid.uuid1())
        
        try:
            if not value:
                value = kwargs['value']
            if not isinstance(value, dict):
                raise self.invalid_input_value
        except KeyError:
            raise self.invalid_input_value
        except NoValueError:
            return False
        
        self._append(key, value)
        return key
    
    def _append(self, key, value:dict):
        if key in self.keys:
            raise KeyError
        else:
            self.keys.append(key)
            self.temp_data[key] = value
            self._autodumpdb()
            return True
    
       
    def get(self, key):
        '''Get the data from the database using the key'''
        try:
            if not key in self.keys:
                raise KeyError
            else:
                with open(self.loco, 'r') as file:
                    readData = literal_eval(file.read())
                return readData[key]
        except KeyError:
            return False
    
    def getAll(self):
        '''Get all the data in the database as JSON format(python dictionary)'''
        try:
            with open(self.loco, 'r') as file:
                readData = literal_eval(file.read())
            return readData
        except ValueError:
            return False
    
    def getByAttribute(self, **kwargs):
        '''Attribute of the record will be checked with the provided values and return the list of mapping data in the database'''
        
        keys = list(kwargs.keys())
        result = []
        temp_data = {}
        with open(self.loco, 'r') as file:
            temp_data = literal_eval(file.read())
            
        for keyi in temp_data:
            IN = False
            singleRecordKeys = list(temp_data[keyi].keys())
            for keyj in keys:
                if not keyj in singleRecordKeys:
                    IN = False
                    break
                else:
                    if kwargs[keyj] == temp_data[keyi][keyj]:
                        IN = True
                    else:
                        IN = False
                        break
            if IN:
                result.append(temp_data[keyi])
                
        return result
        
    def exists(self, key):
        '''Check if a key exists in the database'''
        return key in self.keys
    
    def remove(self, key):
        '''Remove a particular data mapping to the key in the database'''
        if not key in self.keys:
            return False, 'No matching in the database'
        
        temp_data = {}
        with open(self.loco, 'r') as file:
            temp_data = literal_eval(file.read())
        try:
            del temp_data[key]
            self.temp_data = temp_data
            self.keys = list(self.temp_data.keys())
            
            with open(self.loco, 'w') as file:
                file.write('{\n}')
        except KeyError:
            return False, 'Something wrong with the database, please reload the database.'  
                 
        self._autodumpdb()
        return True, "Removed, Removing a record is very costly"
    
    def removeByAttribute(self, **kwargs):
        '''remove all data records in the database which correlate to the attribute value'''
        
        keys = list(kwargs.keys())
        result = {}
        temp_data = {}
        with open(self.loco, 'r') as file:
            temp_data = literal_eval(file.read())
            
        for keyi in temp_data:
            IN = False
            singleRecordKeys = list(temp_data[keyi].keys())
            for keyj in keys:
                if not keyj in singleRecordKeys:
                    IN = False
                    break
                else:
                    if kwargs[keyj] == temp_data[keyi][keyj]:
                        IN = True
                    else:
                        IN = False
                        break
            if not IN:
                result[keyi] = temp_data[keyi]
        
        if len(result) == len(self.keys):
            return False, 'No matching data records found'
        else:
            self.temp_data = result
            self.keys = list(self.temp_data.keys())
            with open(self.loco, 'w') as file:
                file.write('{\n}')
                            
            self._autodumpdb()

            return True, 'Removed, Removing a record is very costly'
    
    def totalKeys(self, key=None):
        '''If the parameter key is not provided return the total number of keys in the database, but if the key is provided return the number of data records inside that particular dictionary'''
        pass    
    
    def getAllKeys(self, key=None):
        '''If the parameter key is not provided return all of the keys in the database, but if the key is provided return all the inner keys of the specific data record'''
        
        if key is None:
            return self.keys
        else:
            result = []
            if not key in self.keys:
                return None
            else:
                with open(self.loco, 'r') as file:
                    dataRecord = literal_eval(file.read())
                
                result.append(keyi for keyi in dataRecord[key])
                return result
    
        
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
