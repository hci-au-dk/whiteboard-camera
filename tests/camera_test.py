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
        
        try:
            f = open('config.json', 'r')
            json_string = f.read()
            loaded_config = json.loads(json_string)
        except IOError:
            assert False, "No configuration loaded"
            return
        assert loaded_config is not None
        assert loaded_config['x0'] == configuration['x0']
        assert loaded_config['y0'] == configuration['y0']
        assert loaded_config['x1'] == configuration['x1']
        assert loaded_config['y1'] == configuration['y1']
        assert loaded_config['x2'] == configuration['x2']
        assert loaded_config['y2'] == configuration['y2']
        assert loaded_config['x3'] == configuration['x3']
        assert loaded_config['y3'] == configuration['y3']
        
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
        
    def test_delete_configuration(self):
        configuration = {'x0': 530, 'y0': 200, 'x1': 480, 'y1': 1240, 'x2': 1610, 'y2': 1512, 'x3': 1682, 'y3': 22}
        json_data = json.dumps(configuration)
        response = self.app.post('/configuration', data = json_data, content_type='application/json')
        
        response2 = self.app.delete('/configuration')
        try:
            f = open('config.json', 'r')
            json_string = f.read()
            assert False, "Configuration still there"
        except IOError:
            assert True, "No configuration file"
            return
        