#!/bin/python3
import os
import tempfile
import pytest
import sys
sys.path.append('../../')
from purge_index_files import delete_index_html_files

@pytest.fixture
def temp_directory():
    """
    Fixture to create a temporary directory for testing.

    This fixture creates a temporary directory using tempfile.mkdtemp().
    The temporary directory path is provided to the test functions, and after testing,
    the temporary directory is removed to clean up resources.

    Yields:
        str: Path of the temporary directory.
    """
    # Create a temporary directory for testing
    temp_dir = tempfile.mkdtemp()
    # Provide the temporary directory to the test for its duration.
    yield temp_dir

def test_delete_index_html_files(temp_directory):
    """
    Test case to verify deletion of index.html files.

    This test function creates some index.html files within the temporary directory,
    calls the delete_index_html_files function to delete them, and then checks if
    the index.html files are successfully deleted.

    Args:
        temp_directory (str): Path of the temporary directory.
    """
    # Create some index.html files within the temporary directory
    os.makedirs(os.path.join(temp_directory, 'subdir1'))
    os.makedirs(os.path.join(temp_directory, 'subdir2'))
    with open(os.path.join(temp_directory, 'index.html'), 'w') as f:
        f.write("Sample index.html content")
    with open(os.path.join(temp_directory, 'subdir1', 'index.html'), 'w') as f:
        f.write("Sample index.html content")
    with open(os.path.join(temp_directory, 'subdir2', 'index.html'), 'w') as f:
        f.write("Sample index.html content")

    # Call the function to delete index.html files
    delete_index_html_files(temp_directory)

    # Check if index.html files are deleted
    assert not os.path.exists(os.path.join(temp_directory, 'index.html'))
    assert not os.path.exists(os.path.join(temp_directory, 'subdir1', 'index.html'))
    assert not os.path.exists(os.path.join(temp_directory, 'subdir2', 'index.html'))

def test_delete_index_html_files_no_index_html(temp_directory):
    """
    Test case to verify behavior when no index.html files are present.

    This test function calls the delete_index_html_files function when no index.html
    files are present within the temporary directory and verifies that nothing is deleted.

    Args:
        temp_directory (str): Path of the temporary directory.
    """
    # Call the function to delete index.html files from an empty directory
    delete_index_html_files(temp_directory)

    # Since there are no index.html files, nothing should be deleted
    assert not os.listdir(temp_directory)

def test_delete_index_html_files_with_other_files(temp_directory):
    """
    Test case to verify behavior with other files present.

    This test function creates some files other than index.html within the temporary directory,
    calls the delete_index_html_files function, and verifies that index.html files are not
    deleted but other files remain untouched.

    Args:
        temp_directory (str): Path of the temporary directory.
    """
    # Create some subdirectories
    os.makedirs(os.path.join(temp_directory, 'subdir'))
    
    # Create some files other than index.html
    with open(os.path.join(temp_directory, 'file1.txt'), 'w') as f:
        f.write("Sample text content")
    with open(os.path.join(temp_directory, 'subdir', 'file2.txt'), 'w') as f:
        f.write("Sample text content")

    # Call the function to delete index.html files
    delete_index_html_files(temp_directory)

    # Check if index.html files are not deleted but other files remain untouched
    assert os.path.exists(os.path.join(temp_directory, 'file1.txt'))
    assert os.path.exists(os.path.join(temp_directory, 'subdir', 'file2.txt'))
