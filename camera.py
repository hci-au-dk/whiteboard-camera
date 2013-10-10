from flask import Flask, send_file
app = Flask(__name__)
import picam
import time
import tempfile
import StringIO
from shutil import copyfileobj
from os import remove
from PIL import Image

@app.route("/")
def hello():
    return "I am a whiteboard camera."
    
@app.route("/snapshot")
def snapshot():
    i = picam.takePhoto()
    #i = Image.open('/Users/clemens/Programming/Whiteboards/discontinuityboard/tests/test_data/wb.jpg')
    imageBuffer = StringIO.StringIO() 
    i.save(imageBuffer, format="JPEG")
    imageBuffer.seek(0)
    return send_file(imageBuffer, mimetype='image/jpeg')
    
if __name__ == "__main__":
    app.run(debug = True)