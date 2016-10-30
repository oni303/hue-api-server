import socket
import json
import time
from tzlocal import get_localzone
import datetime
from copy import deepcopy

class Config(object):
    def __init__(self):
        self.file ='hueConfig.json' 
        with open(self.file) as config_file:  
            self.allConfig = json.load(config_file)
            config_file.close()
        self.config = self.allConfig['config']
        self.config["ipaddress"] = str(socket.gethostbyname(socket.gethostname()))
        self.config["timezone"] = get_localzone().zone 
        self.config["localtime"] = str(datetime.datetime.now().isoformat())
        self.config["UTC"] = str(datetime.datetime.utcnow().isoformat())

        self.lights = self.allConfig['lights']
        self.groups = self.allConfig['groups']
        
        
    def set(self, key, value):
        self.config[key] = value
    def get(self, key):
        return self.config[key] 
    def save(self):
        with open(self.file, 'w') as config_file:  
            json.dump(self.config, config_file, indent=4, sort_keys=True)
            config_file.close()
    def get_bridge_config(self, user):
        #it is request used to connect an app to this bridge so we do not offer all details
        conf = False
        if user == 'nouser': 
            conf = deepcopy(self.config)
            conf['whitelist'] = None
        else:
            # if the user is kown we only return its one whitelist entry
            if user in self.config['whitelist'].keys(): 
                conf = deepcopy(self.config)
                conf['whitelist'] = {user : self.config['whitelist'][user]} 
        return conf
        

if __name__ == '__main__':
    config = Config()
    print(json.dumps(config.config))
