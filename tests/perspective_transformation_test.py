import unittest
from PIL import Image
from util.perspective_transformation import transform_perspective
import math
import operator
import os

class PerspectiveTransformationTest(unittest.TestCase):
    """Testing the perspective transformation utility function"""
    
    def setUp(self):
        self.img = Image.open('tests/test_data/wb.jpg')
        # Upper left
        self.x0 = 530
        self.y0 = 200
        # Lower left
        self.x1 = 480
        self.y1 = 1240
        # Lower right
        self.x2 = 1610
        self.y2 = 1512
        # Upper right
        self.x3 = 1682
        self.y3 = 22
        
        width = int(math.sqrt((abs(self.x0 - self.x3) * abs(self.x0 - self.x3)) + (abs(self.y0 - self.y3) + abs(self.y0 - self.y3))))
        
        height = int(math.sqrt((abs(self.x1 - self.x2) * abs(self.x1 - self.x2)) + (abs(self.y1 - self.y2) * abs(self.y1 - self.y2))))
        
        self.size = (width, height)
        
    def test_correct_dimensions(self):
        self.img = transform_perspective(self.img, self.x0, self.y0, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
        (new_width, new_height) = self.img.size
        self.img.save('tests/test_data/wb_test_temp.jpg')
        assert self.img.size == self.size, "New image size is the same as computed whiteboard size in pixels"
        

    def test_correct_image_result(self):
        self.img = transform_perspective(self.img, self.x0, self.y0, self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
        self.img.save('tests/test_data/wb_test_temp.jpg') #Hack given that the histogram of an image changes when saved and opened as jpg probably due to compression
        self.img = Image.open('tests/test_data/wb_test_temp.jpg')
        os.remove('tests/test_data/wb_test_temp.jpg')
        img_comparison = Image.open('tests/test_data/wb_transformed_scaled.jpg')
        histogram1 = self.img.histogram()
        histogram2 = img_comparison.histogram()
        
        #from http://stackoverflow.com/questions/1927660/compare-two-images-the-python-linux-way
        root_mean_square = math.sqrt(reduce(operator.add,
            map(lambda a,b: (a-b)**2, histogram1, histogram2))/len(histogram1))     
        
        assert root_mean_square == 0
        