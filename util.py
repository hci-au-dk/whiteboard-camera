import math
from PIL import Image

def transform_perspective(img, x0, y0, x1, y1, x2, y2, x3, y3):
    '''
    Transforms and resizes and image to the content of the given four points
    '''
    width = int(math.sqrt((abs(x0 - x3) * abs(x0 - x3)) + (abs(y0 - y3) + abs(y0 - y3))))
    height = int(math.sqrt((abs(x1 - x2) * abs(x1 - x2)) + (abs(y1 - y2) * abs(y1 - y2))))
    size = (width, height)
        
    img = img.transform(size, Image.QUAD, (x0, y0, x1, y1, x2, y2, x3, y3), Image.BICUBIC)
    
    return img