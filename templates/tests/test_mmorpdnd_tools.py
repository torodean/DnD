#!/bin/python3
import os
import tempfile
import pytest
import sys
sys.path.append('../')
from mmorpdnd_tools import is_image_file

def test_is_image_file_with_image_extensions():
    """
    Test if the function correctly identifies file names with image extensions.
    """
    assert is_image_file('photo.jpg') == True
    assert is_image_file('image.jpeg') == True
    assert is_image_file('picture.png') == True
    assert is_image_file('logo.gif') == True
    assert is_image_file('pic.bmp') == True


def test_is_image_file_without_image_extensions():
    """
    Test if the function correctly identifies file names without image extensions.
    """
    assert is_image_file('document.pdf') == False
    assert is_image_file('presentation.pptx') == False
    assert is_image_file('spreadsheet.xlsx') == False
    assert is_image_file('text.txt') == False


def test_is_image_file_with_mixed_case_extensions():
    """
    Test if the function correctly handles file names with mixed case extensions.
    """
    assert is_image_file('photo.JPG') == True
    assert is_image_file('image.PnG') == True
    assert is_image_file('picture.GIF') == True
    

def test_is_image_file_with_edge_cases():
    """
    Test if the function correctly handles edge cases and boundary conditions.
    """
    #assert is_image_file('.jpg') == False   # File name consists only of the extension
    assert is_image_file('image') == False  # File name has no extension
    assert is_image_file('') == False       # Empty file name
