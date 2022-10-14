import os
import sys
import signal
import json
import uuid
from threading import Thread
from Exceptions import NoValueError


class Database(object):
    
    key_string_error = TypeError('Custom type error occured')
    invalid_input_value = NoValueError('No value/Invalid is provided to insert')
    
    def __init__(self, location, auto_dump, sig=True):
        
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
        location = os.path.expanduser(location)
        self.loco = location
        self.auto_dump = auto_dump
        if os.path.exists(location):
            self._loaddb()
        else:
            self.db = {}
        return True
    
    def dump(self):
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
        try:
            return self.db[key]
        except KeyError:
            return False
    
    def getAll(self):
        return self.db
    
    def getByAttribute(self, **kwargs):
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
        return key in self.db
    
    def remove(self, key):
        if not key in self.db:
            return False
        del self.db[key]
        self._autodumpdb()
        return True
    
    def removeByAttribute(self, **kwargs):
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
        self.db = {}
        self._autodumpdb()
        return True             