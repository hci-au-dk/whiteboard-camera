from flask import Flask, send_file, request, jsonify
app = Flask(__name__)
import datetime
import time
import tempfile
import requests
import requests.exceptions
import StringIO
import json
import os
from shutil import copyfileobj
from os import remove
from PIL import Image
from util.perspective_transformation import transform_perspective

camera_module = None
config = None
server_config = None

def clear_config():
    global config
    config = None

@app.route('/register-server', methods=['POST', 'DELETE'])
def register_server():
    if request.method == 'POST':
        if not isinstance(request.json, dict):
            return 'Malformed registration data', 400
        if len(request.json) != 1:
            return 'Configuration must have 1 entries', 400
        if (not 'server' in request.json):
            return 'Configuration must have key server', 400
        global server_config
        server_config = request.json
        with open('server.json', 'w') as outfile:
            json.dump(server_config, outfile)
        return 'Server saved'
    if request.method == 'DELETE':
        os.remove('server.json')
        return 'Deleted server config file', 200

@app.route('/configuration', methods=['GET', 'POST', 'DELETE'])
def configuration():
    if request.method == 'POST':
        if not isinstance(request.json, dict):
            return 'Malformed configuration data', 400
        if len(request.json) != 8:
            return 'Configuration must have 8 entries', 400
        if (not 'x0' in request.json) or (not 'y0' in request.data) or (not 'x1' in request.json) or (not 'y1' in request.data) or (not 'x2' in request.json) or (not 'y2' in request.data) or (not 'x3' in request.json) or (not 'y3' in request.data):
            return 'Configuration must have keys x0, y0, x1, y1, x2, y2, x3, y3', 400
        global config
        config = request.json
        with open('config.json', 'w') as outfile:
          json.dump(config, outfile)
        return "Configuration saved"
    if request.method == 'GET':
        global config
        if config is None:
            return "Camera has no configuration", 404
        return jsonify(config)
    if request.method == 'DELETE':
        os.remove('config.json')
        return "Deleted configuration file", 200    
    

@app.route("/")
def hello():
    return "I am a whiteboard camera."
    
@app.route("/snapshot")
def snapshot():
    global config
    img = camera_module.takePhoto()
    if config is not None:
        img = transform_perspective(img, int(config['x0']), int(config['y0']), int(config['x1']), int(config['y1']), int(config['x2']), int(config['y2']), int(config['x3']), int(config['y3']))
        
    imageBuffer = StringIO.StringIO() 
    img.save(imageBuffer, format="JPEG")
    imageBuffer.seek(0)
    return send_file(imageBuffer, mimetype='image/jpeg')

@app.route("/rawimage")
def rawimage():
    img = camera_module.takePhoto()
    imageBuffer = StringIO.StringIO() 
    img.save(imageBuffer, format="JPEG")
    imageBuffer.seek(0)
    return send_file(imageBuffer, mimetype='image/jpeg')

@app.route("/button-snapshot")
def button_snapshot():
    global config
    img = camera_module.takePhoto()
    if config is not None:
        img = transform_perspective(img, int(config['x0']), int(config['y0']), int(config['x1']), int(config['y1']), int(config['x2']), int(config['y2']), int(config['x3']), int(config['y3']))
        
    imageBuffer = StringIO.StringIO() 
    img.save(imageBuffer, format="JPEG")
    imageBuffer.seek(0)

    # send image to the server
    global server_config
    if server_config is None:
        s = 'Server configuration file not found. Perhaps you have not registered this pi yet?'
        return s

    ip = server_config['server']
    server_location = 'http://' + server_config['server'] + '/pi-upload/'

    now = datetime.datetime.now()
    filename = 'button_%i%i%i_%i%i%i' % (now.year,
                                         now.month,
                                         now.day,
                                         now.hour,
                                         now.minute,
                                         now.second)
    filename = filename + ".jpg"
    files = {'file': (filename, imageBuffer.getvalue())}
    try:
        r = requests.post(server_location, files=files)
    except:
        requests.exceptions.ConnectionError
        s = 'Connection to ' + server_location + ' timed out. Check to see that this address is accepting connections.'
        s = s + 'If this is the incorrect location, please register your pi again. This will require deleting the'
        s = s + 'previous configuration, as all pi ip addresses must be unique.'
        return s

    response = make_response(r.json(), 200)
    response.headers['Content-type'] = 'application/json'
    return response

    
if __name__ == "__main__":
    import picam
    camera_module = picam
    try:
        f = open('config.json', 'r')
        json_string = f.read()
        config = json.loads(json_string)
    except IOError:
        print "No configuration file to load..."
    try:
        f = open('server.json', 'r')
        json_string = f.read()
        server_config = json.loads(json_string)
    except IOError:
        print "No server configuration file to load..."
    app.run(debug = True, host='0.0.0.0', port=80)
