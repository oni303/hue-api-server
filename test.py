#!/usr/bin/python3

from flask import Flask , request, jsonify
from upnp import UpnpServer
from config import Config
import json
import datetime
import random
import string  
import socket

class PermissionDenied(Exception):
    status_code = 503

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

app = Flask(__name__)

@app.errorhandler(PermissionDenied)
def handlePermissionDenied(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.route('/<filename>')
def index(filename):
      if filename == "description.xml":
            ip = socket.gethostbyname(socket.gethostname())
            msg =  """<?xml version=\"1.0\" encoding=\"UTF-8\" ?>
                    <root xmlns=\"urn:schemas-upnp-org:device-1-0\">
                        <specVersion>
                            <major>1</major>
                            <minor>0</minor>
                        </specVersion>
                        <URLBase>http://"""+str(ip)+"""</URLBase>
                        <device>
                            <deviceType>urn:schemas-upnp-org:device:Basic:1</deviceType>
                            <friendlyName>Philips hue ("""+str(ip)+""")</friendlyName>
                            <manufacturer>Royal Philips Electronics</manufacturer>
                            <manufacturerURL>http://www.philips.com</manufacturerURL>
                            <modelDescription>Philips hue Personal Wireless Lighting
                            </modelDescription>
                            <modelName>Philips hue bridge 2015</modelName>
                            <modelNumber>929000226503</modelNumber>
                            <modelURL>http://www.meethue.com</modelURL>
                            <serialNumber>0017880ae670</serialNumber>
                            <UDN>uuid:2f402f80-da50-11e1-9b23-0017880ae670</UDN>
                            <presentationURL>index.html</presentationURL>
                            <iconList>
                                <icon>
                                    <mimetype>image/png</mimetype>
                                    <height>48</height>
                                    <width>48</width>
                                    <depth>24</depth>
                                    <url>hue_logo_0.png</url>
                                </icon>
                                <icon>
                                    <mimetype>image/png</mimetype>
                                    <height>120</height>
                                    <width>120</width>
                                    <depth>24</depth>
                                    <url>hue_logo_3.png</url>
                                </icon>
                            </iconList>
                        </device>
                    </root>"""
      else:
            msg = filename
                 
      return msg

@app.route('/api/<username>/config')
def config(username):
    conf = Config()
    retVal = conf.get_bridge_config(username)
    if retVal:
        return json.dumps(retVal)
    else:
        raise PermissionDenied('wrong user', status_code=503)

@app.route('/api/', methods=['POST'])
def api():
    try:
        body = json.loads(request.data.decode())
        devType = body['devicetype']
        username = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(30))
        config = Config()
        whitelist = config.get("whitelist")
        whitelist[username] = {"name":devType, "create date":str(datetime.datetime.utcnow().isoformat()), "last use date":str(datetime.datetime.utcnow().isoformat())}
        config.save()
        retValue = [{"success":{"username": username}}]
        return json.dumps(retValue)
    except Exception as e:
        print(e)
        raise PermissionDenied('No data', status_code=503)

@app.route('/api/<username>/')
def fullState(username):
    conf = Config()
    retVal = conf.get_bridge_config(username)
    if retVal:
        return json.dumps(conf.allConfig)
    else:
        raise PermissionDenied('wrong user', status_code=503)


if __name__ == '__main__':
    upnpServ = UpnpServer()
    upnpServ.start()
    app.run(host='0.0.0.0', port=80)
    upnpServ.join()
      
