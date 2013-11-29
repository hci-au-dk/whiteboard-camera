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
from util import printer

camera_module = None
config = None
server_config = None
tp = None

def clear_config():
    global config
    config = None

@app.route('/register-server', methods=['GET', 'DELETE'])
def register_server():
    if request.method == 'GET':
        ip = request.remote_addr
        pi_id = request.args.get('id')
        global server_config
        server_config = {'server': ip, 'id': pi_id}
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

@app.route("/thermal-hello")
def thermal_hello():
    global tp
    tp.print_text("hello")
    tp.linefeed(3)

    return 'See thermal printer for message!', 200

@app.route("/button-snapshot")
def button_snapshot():
    global tp
    now = datetime.datetime.now()

    tp.print_text('Time submitted: ')
    tp.print_text(str(now))
    tp.linefeed(2)

    # send image to the server
    global server_config
    if server_config is None:
        s = 'Server configuration file not found. Perhaps you have not registered this pi yet?'

    ip = server_config['server']
    server_location = 'http://' + server_config['server']

    # generate the access code
    r = requests.get(server_location + '/generate-access-code/')
    code = r.json()['code']

    tp.print_text('You have 2 days to process this snapshot before it is ')
    tp.print_text('automatically deleted.')
    tp.linefeed(2)

    tp.print_text('Access code: \n')
    tp.justify("C")
    tp.double_width(True)
    tp.double_height(True)
    tp.print_text(code)
    tp.double_width(False)
    tp.double_height(False)
    tp.justify("L")
    tp.linefeed(2)

    tp.print_text('Your photo will be available at: \n')
    tp.print_text('http://' + server_config['server'] + '/')
    tp.linefeed(5)

    global config
    img = camera_module.takePhoto()
    if config is not None:
        img = transform_perspective(img, int(config['x0']), int(config['y0']), int(config['x1']), int(config['y1']), int(config['x2']), int(config['y2']), int(config['x3']), int(config['y3']))
        
    imageBuffer = StringIO.StringIO() 
    img.save(imageBuffer, format="JPEG")
    imageBuffer.seek(0)

    filename = 'button_%i%i%i_%i%i%i' % (now.year,
                                         now.month,
                                         now.day,
                                         now.hour,
                                         now.minute,
                                         now.second)
    filename = filename + ".jpg"
    files = {'file': (filename, imageBuffer.getvalue())}
    data = {'id': server_config['id'], 'code': code}
    r = requests.post(server_location + '/pi-upload/', files=files, data=data)
    if r.status_code != 200:
        tp.print_text('There was an error with the photo:\n')
        tp.print_text(str(r.status_code))
        tp.linefeed()
        tp.print_text(r.text)
    elif r.json()['code'] != code:
        tp.print_text('There was a code mismatch error.\n')
        tp.print_text(code + ' vs ' + r.json()['code'])

    return 'Success', 200


    
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

    # Now be listening on the terminal for a take-photo command    
    tp = printer.ThermalPrinter()

    app.run(debug = True, host='0.0.0.0', port=80)


