from flask import Flask, send_file, request, jsonify
app = Flask(__name__)
import time
import tempfile
import StringIO
import json
from shutil import copyfileobj
from os import remove
from PIL import Image
from util.perspective_transformation import transform_perspective

camera_module = None
config = None

@app.route('/configuration', methods=['GET', 'POST'])
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
        return jsonify(config)

@app.route("/")
def hello():
    return "I am a whiteboard camera."
    
@app.route("/snapshot")
def snapshot():
    global config
    img = camera_module.takePhoto()
    if config is not None:
        img = transform_perspective(img, config['x0'], config['y0'], config['x1'], config['y1'], config['x2'], config['y2'], config['x3'], config['y3'])
        
    imageBuffer = StringIO.StringIO() 
    img.save(imageBuffer, format="JPEG")
    imageBuffer.seek(0)
    return send_file(imageBuffer, mimetype='image/jpeg')

    
if __name__ == "__main__":
    import picam
    camera_module = picam
    try:
        f = open('config.json', 'r')
        json_string = f.read()
        config = json.loads(json_string)
    except IOError:
        print "No configuration file to load..."
    app.run(debug = True, host='0.0.0.0', port=80)