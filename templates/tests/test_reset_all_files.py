#!/bin/python3
import os
import pytest
import tempfile
import sys
sys.path.append('../')
from reset_all_files import copy_images
from reset_all_files import delete_html_files
from reset_all_files import move_input_files

@pytest.fixture
def temp_directory():
    """
    Fixture to create a temporary directory for testing.

    This fixture creates a temporary directory using tempfile.mkdtemp().
    Yields:
        str: Path of the temporary directory.
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    
@pytest.fixture
def temp_directories():
    """
    Fixture to create temporary source and destination directories for testing.

    This fixture creates temporary source and destination directories using tempfile.mkdtemp().
    Yields:
        Tuple[str, str]: Paths of the temporary source and destination directories.
    """
    source_dir = tempfile.mkdtemp()
    dest_dir = tempfile.mkdtemp()
    print(f"Made temporary source directory:      {source_dir}")
    print(f"Made temporary destination directory: {dest_dir}")
    yield source_dir, dest_dir


def test_copy_images(temp_directories):
    """
    Test case to verify copying image files.

    This test function creates some image files within the 'img' folder of the temporary source directory,
    calls the copy_images function, and verifies that the image files are successfully copied to the destination directory.

    Args:
        temp_directories (Tuple[str, str]): Paths of the temporary source and destination directories.
    """
    source_dir, dest_dir = temp_directories

    # Create 'img' folder in the temporary source directory
    img_dir = os.path.join(source_dir, 'img')
    os.makedirs(img_dir)
    print(f"Making temporary img directory:         {img_dir}")

    # Create some image files within the 'img' folder
    with open(os.path.join(img_dir, 'image1.png'), 'w') as f:
        f.write("Sample image content")
    with open(os.path.join(img_dir, 'image2.jpg'), 'w') as f:
        f.write("Sample image content")
    with open(os.path.join(img_dir, 'image3.jpeg'), 'w') as f:
        f.write("Sample image content")
    with open(os.path.join(img_dir, 'image4.gif'), 'w') as f:
        f.write("Sample image content")
    with open(os.path.join(img_dir, 'text_file.txt'), 'w') as f:
        f.write("Sample text content")
        
    # Print contents of the img directory before copying
    print(f"Contents of {img_dir} before copying:")
    print(os.listdir(img_dir))

    # Call the function to copy image files
    copy_images(source_dir, dest_dir)
        
    # Print contents of the destination directory before copying
    print("Contents of destination directory after copying:")
    print(os.listdir(dest_dir))
    
    # Verify that the image files are copied to the destination directory
    assert os.path.exists(os.path.join(dest_dir, 'image1.png'))
    assert os.path.exists(os.path.join(dest_dir, 'image2.jpg'))
    assert os.path.exists(os.path.join(dest_dir, 'image3.jpeg'))
    assert os.path.exists(os.path.join(dest_dir, 'image4.gif'))
    assert not os.path.exists(os.path.join(dest_dir, 'text_file.txt'))


def test_copy_images_no_images(temp_directories):
    """
    Test case to verify behavior when no image files are present.

    This test function calls the copy_images function when no image files are present within the
    'img' folder of the temporary source directory and verifies that nothing is copied.

    Args:
        temp_directories (Tuple[str, str]): Paths of the temporary source and destination directories.
    """
    source_dir, dest_dir = temp_directories
    
    # Create 'img' folder in the temporary source directory
    img_dir = os.path.join(source_dir, 'img')
    os.makedirs(img_dir)
    print(f"Making temporary img directory:         {img_dir}")
        
    # Print contents of the img directory before copying
    print(f"Contents of {img_dir} before copying:")
    print(os.listdir(img_dir))

    # Call the function to copy image files from an empty 'img' folder
    copy_images(source_dir, dest_dir)
        
    # Print contents of the destination directory before copying
    print("Contents of destination directory after copying:")
    print(os.listdir(dest_dir))

    # Verify that no files are copied
    assert not os.listdir(dest_dir)


def test_copy_images_with_non_image_files(temp_directories):
    """
    Test case to verify behavior with non-image files present.

    This test function creates some files other than images within the temporary source directory,
    calls the copy_images function, and verifies that only image files are copied to the destination directory
    while other files remain untouched.

    Args:
        temp_directories (Tuple[str, str]): Paths of the temporary source and destination directories.
    """    
    source_dir, dest_dir = temp_directories
    
    # Create some subdirectories
    sub_dir = os.path.join(source_dir, 'subdir')
    os.makedirs(sub_dir)
    print(f"Making temporary img directory:         {sub_dir}")

    # Create some files other than images
    with open(os.path.join(source_dir, 'file1.txt'), 'w') as f:
        f.write("Sample text content")
    with open(os.path.join(sub_dir, 'file2.txt'), 'w') as f:
        f.write("Sample text content")
        
    # Print contents of the img directory before copying
    print("Contents of img directory before copying:")
    print(os.listdir(source_dir))

    # Call the function to copy images
    copy_images(source_dir, dest_dir)
        
    # Print contents of the destination directory before copying
    print("Contents of destination directory after copying:")
    print(os.listdir(dest_dir))

    # Verify that only image files are copied
    assert not os.path.exists(os.path.join(dest_dir, 'file1.txt'))
    assert not os.path.exists(os.path.join(dest_dir, 'file2.txt'))


def test_delete_html_files(temp_directory):
    """
    Test case to verify deleting HTML files.

    This test function creates some HTML files within the temporary directory and its subdirectories,
    calls the delete_html_files function, and verifies that the HTML files are successfully deleted.

    Args:
        temp_directory (str): Path of the temporary directory.
    """    
    # Create a subdirectory
    sub_dir = os.path.join(temp_directory, 'subdir')
    os.makedirs(sub_dir)
    print(f"Making temporary img directory:         {sub_dir}")
    
    # Create some HTML files within the temporary directory and its subdirectories
    with open(os.path.join(temp_directory, 'file1.html'), 'w') as f:
        f.write("Sample HTML content")
    with open(os.path.join(sub_dir, 'file2.html'), 'w') as f:
        f.write("Sample HTML content")
    with open(os.path.join(sub_dir, 'file3.txt'), 'w') as f:
        f.write("Sample text content")
        
    # Print contents of the temp directory before deleting
    print(f"Contents of {temp_directory} before deleting:")
    print(os.listdir(temp_directory))

    # Call the function to delete HTML files
    delete_html_files(temp_directory)
        
    # Print contents of the temp directory before deleting
    print(f"Contents of {temp_directory} after deleting:")
    print(os.listdir(temp_directory))

    # Verify that the HTML files are deleted while other files remain untouched
    assert not os.path.exists(os.path.join(temp_directory, 'file1.html'))
    assert not os.path.exists(os.path.join(sub_dir, 'file2.html'))
    assert os.path.exists(os.path.join(sub_dir, 'file3.txt'))


def test_delete_html_files_no_html_files(temp_directory):
    """
    Test case to verify behavior when no HTML files are present.

    This test function calls the delete_html_files function when no HTML files
    are present within the temporary directory and verifies that nothing is deleted.

    Args:
        temp_directory (str): Path of the temporary directory.
    """
    # Call the function to delete HTML files from an empty directory
    delete_html_files(temp_directory)

    # Verify that no files are deleted
    assert not os.listdir(temp_directory)


def test_delete_html_files_with_non_html_files(temp_directory):
    """
    Test case to verify behavior with non-HTML files present.

    This test function creates some files other than HTML files within the temporary directory,
    calls the delete_html_files function, and verifies that only HTML files are deleted while
    other files remain untouched.

    Args:
        temp_directory (str): Path of the temporary directory.
    """
    # Create a subdirectory
    sub_dir = os.path.join(temp_directory, 'subdir')
    os.makedirs(sub_dir)
    print(f"Making temporary img directory:         {sub_dir}")
    
    # Create some files other than HTML files
    with open(os.path.join(temp_directory, 'file1.txt'), 'w') as f:
        f.write("Sample text content")
    with open(os.path.join(sub_dir, 'file2.txt'), 'w') as f:
        f.write("Sample text content")

    # Call the function to delete HTML files
    delete_html_files(temp_directory)

    # Verify that only HTML files are deleted
    assert os.path.exists(os.path.join(temp_directory, 'file1.txt'))
    assert os.path.exists(os.path.join(sub_dir, 'file2.txt'))


def test_move_input_files(temp_directories):
    """
    Test case to verify moving .input and .char files.

    This test function creates some .input and .char files within the temporary source directory,
    calls the move_input_files function, and verifies that the files are successfully moved to the destination directory.

    Args:
        temp_directories (Tuple[str, str]): Paths of the temporary source and destination directories.
    """    
    source_dir, dest_dir = temp_directories
    
    # Create some subdirectories
    sub_dir = os.path.join(source_dir, 'subdir')
    os.makedirs(sub_dir)
    print(f"Making temporary img directory:         {sub_dir}")

    # Create some .input and .char files within the temporary source directory
    with open(os.path.join(source_dir, 'file1.input'), 'w') as f:
        f.write("Sample content")
    with open(os.path.join(source_dir, 'file2.char'), 'w') as f:
        f.write("Sample content")
    with open(os.path.join(sub_dir, 'file3.input'), 'w') as f:
        f.write("Sample content")
        
    # Print contents of the source directory before moving
    print(f"Contents of {source_dir} before moving:")
    print(os.listdir(source_dir))
        
    # Print contents of the sub directory before moving
    print(f"Contents of {sub_dir} before moving:")
    print(os.listdir(sub_dir))

    # Call the function to move .input and .char files
    move_input_files(source_dir, dest_dir)

    # Verify that the files are moved to the destination directory
    assert not os.path.exists(os.path.join(source_dir, 'file1.input'))
    assert not os.path.exists(os.path.join(source_dir, 'file2.char'))
    assert not os.path.exists(os.path.join(sub_dir, 'file3.input'))

    assert os.path.exists(os.path.join(dest_dir, 'file1.input'))
    assert os.path.exists(os.path.join(dest_dir, 'file2.char'))
    assert os.path.exists(os.path.join(dest_dir, 'file3.input'))


def test_move_input_files_no_files(temp_directories):
    """
    Test case to verify behavior when no .input or .char files are present.

    This test function calls the move_input_files function when no .input or .char files
    are present within the temporary source directory and verifies that nothing is moved.

    Args:
        temp_directories (Tuple[str, str]): Paths of the temporary source and destination directories.
    """
    source_dir, dest_dir = temp_directories

    # Call the function to move .input and .char files from an empty directory
    move_input_files(source_dir, dest_dir)

    # Verify that no files are moved
    assert not os.listdir(source_dir)
    assert not os.listdir(dest_dir)


def test_move_input_files_with_other_files(temp_directories):
    """
    Test case to verify behavior with other types of files present.

    This test function creates some files other than .input and .char files within the temporary
    source directory, calls the move_input_files function, and verifies that only .input and .char
    files are moved to the destination directory while other files remain untouched.

    Args:
        temp_directories (Tuple[str, str]): Paths of the temporary source and destination directories.
    """    
    source_dir, dest_dir = temp_directories
    
    # Create some subdirectories
    sub_dir = os.path.join(source_dir, 'subdir')
    os.makedirs(sub_dir)
    print(f"Making temporary sub directory:       {sub_dir}")

    # Create some files other than .input and .char
    with open(os.path.join(source_dir, 'file1.txt'), 'w') as f:
        f.write("Sample text content")
    with open(os.path.join(sub_dir, 'file2.txt'), 'w') as f:
        f.write("Sample text content")
        
    # Print contents of the source directory before moving
    print(f"Contents of {source_dir} before moving:")
    print(os.listdir(source_dir))
        
    # Print contents of the sub directory before moving
    print(f"Contents of {sub_dir} before moving:")
    print(os.listdir(sub_dir))

    # Call the function to move .input and .char files
    move_input_files(source_dir, dest_dir)

    # Verify that only .input and .char files are moved
    assert os.path.exists(os.path.join(source_dir, 'file1.txt'))
    assert os.path.exists(os.path.join(sub_dir, 'file2.txt'))

    assert not os.path.exists(os.path.join(dest_dir, 'file1.txt'))
    assert not os.path.exists(os.path.join(dest_dir, 'file2.txt'))
