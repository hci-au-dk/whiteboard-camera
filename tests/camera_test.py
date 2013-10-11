import unittest
from flask import Flask
import camera
from PIL import Image
from stubs import picam_stub
import StringIO
import json

class CameraTest(unittest.TestCase):
    
    def setUp(self):
        camera.app.config['TESTING'] = True
        camera.camera_module = picam_stub
        self.app = camera.app.test_client()
        
    def tearDown(self):
        camera.clear_config()
        
    def test_front_page_get_success(self):
        rv = self.app.get('/')
        assert 'I am a whiteboard camera.' in rv.data
        
    def test_set_correct_configuration(self):
        configuration = {'x0': 530, 'y0': 200, 'x1': 480, 'y1': 1240, 'x2': 1610, 'y2': 1512, 'x3': 1682, 'y3': 22}
        json_data = json.dumps(configuration)
        response = self.app.post('/configuration', data = json_data, content_type='application/json')
        assert response.status_code == 200
        
    def test_snapshot(self):
        configuration = {'x0': 530, 'y0': 200, 'x1': 480, 'y1': 1240, 'x2': 1610, 'y2': 1512, 'x3': 1682, 'y3': 22}
        json_data = json.dumps(configuration)
        response = self.app.post('/configuration', data = json_data, content_type='application/json')
        
        rv = self.app.get('/snapshot')
        result_image = Image.open('tests/test_data/wb_transformed_scaled.jpg')
        img = Image.open(StringIO.StringIO(rv.data))
        assert img.mode == result_image.mode
        assert img.size == result_image.size
        
    def test_rawimage(self):
        rv = self.app.get('/rawimage')
        result_image = Image.open('tests/test_data/wb.jpg')
        img = Image.open(StringIO.StringIO(rv.data))
        assert img.mode == result_image.mode
        assert img.size == result_image.size
        
    def test_set_wrongly_typed_configuration(self):
        configuration = ['foo', 'bar']
        json_data = json.dumps(configuration)
        response = self.app.post('/configuration', data = json_data, content_type='application/json')
        assert response.status_code == 400
        
    def test_set_configuration_with_wrong_length(self):
        configuration = {'x0': 530, 'y0': 200, 'x1': 480, 'y1': 1240, 'x2': 1610, 'y2': 1512, 'x3': 1682}
        json_data = json.dumps(configuration)
        response = self.app.post('/configuration', data = json_data, content_type='application/json')
        assert response.status_code == 400
        
    def test_set_configuration_with_wrong_key(self):
        configuration = {'x0': 530, 'y0': 200, 'x1': 480, 'y1': 1240, 'x2': 1610, 'y2': 1512, 'z3': 1682}
        json_data = json.dumps(configuration)
        response = self.app.post('/configuration', data = json_data, content_type='application/json')
        assert response.status_code == 400
        
    def test_get_configuration_where_undefined(self):
        response = self.app.get('/configuration')
        assert response.status_code == 404
    
    def test_get_configuration(self):
        configuration = {'x0': 530, 'y0': 200, 'x1': 480, 'y1': 1240, 'x2': 1610, 'y2': 1512, 'x3': 1682, 'y3': 22}
        json_data = json.dumps(configuration)
        response = self.app.post('/configuration', data = json_data, content_type='application/json')
        
        response = self.app.get('/configuration')
        response_json_str = json.dumps(json.loads(response.data))
        assert len(response_json_str) == len(json_data)
        assert response.status_code == 200
        