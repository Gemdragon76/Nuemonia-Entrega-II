import pytest
import app
import os

import subprocess

def test_predict():
    result=resultado = app.predict_pneumonia(r"C:\Users\MMDDB\Downloads\person1710_bacteria_4526.jpeg")
    assert result  == "No Pneumonia"

def test_predict2():
    result=resultado = app.predict_pneumonia(r"C:\Users\MMDDB\Downloads\person1710_bacteria_4526.jpeg")
    assert result  == "Pneumonia"
