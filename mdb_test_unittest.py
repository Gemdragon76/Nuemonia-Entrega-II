import unittest
from detector_neumonia import App

class Testload_img_file(unittest.TestCase):
    def test_1(self):
        testValue = True
        resultado = App.load_img_file
        self.assertTrue(testValue,'mi_imagen.jpg')

    def test_2(self):
        testValue = True
        resultado = App.load_img_file
        self.assertTrue(testValue,'')
        
    def test_3(self):
        testValue = True
        resultado = App.load_img_file
        self.assertTrue(testValue,Null)
        
    def test_4(self):
        testValue = False
        resultado = App.load_img_file
        self.assertTrue(testValue,'')

if __name__ == '__main__':
    unittest.main()