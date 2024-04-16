#!/bin/python3
import os
import tempfile
import pytest
import sys
sys.path.append('../../')
from mmorpdnd import is_image_file
from mmorpdnd import get_relative_path
from mmorpdnd import alphabetize_links
from mmorpdnd import MMORPDND

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


def test_get_relative_path():
    """
    Test cases for get_relative_path function.
    """
    # Test case 1: Relative path within the same directory
    from_file = '/path/to/source/file.html'
    to_file = '/path/to/source/otherfile.txt'
    expected_result = 'otherfile.txt'
    assert get_relative_path(from_file, to_file) == expected_result

    # Test case 2: Relative path within a subdirectory
    from_file = '/path/to/source/file.html'
    to_file = '/path/to/source/subdirectory/anotherfile.txt'
    expected_result = 'subdirectory/anotherfile.txt'
    assert get_relative_path(from_file, to_file) == expected_result

    # Test case 3: Relative path to a parent directory
    from_file = '/path/to/source/subdirectory/file.html'
    to_file = '/path/to/source/otherfile.txt'
    expected_result = '../otherfile.txt'
    assert get_relative_path(from_file, to_file) == expected_result

    # Test case 4: Relative path to a sibling directory
    from_file = '/path/to/source/subdirectory/file.html'
    to_file = '/path/to/source/otherdirectory/otherfile.txt'
    expected_result = '../otherdirectory/otherfile.txt'
    assert get_relative_path(from_file, to_file) == expected_result


def test_alphabetize_links_with_links():
    """
    Test case to verify alphabetizing links.
    """
    input_links = '''<li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
                   <li><a href="kaelar_stormcaller.html">kaelar_stormcaller</a></li>
                   <li><a href="thorne_ironfist.html">thorne_ironfist</a></li>
                   <li><a href="foobar.html">foobar</a></li>
                   <li><a href="aria_thistlewood.html">aria_thistlewood</a></li>
                   <li><a href="stoneshaper_golem.html">stoneshaper_golem</a></li>
                   <li><a href="elara_nightshade.html">elara_nightshade</a></li>'''
    expected_output = '''<li><a href="aria_thistlewood.html">aria_thistlewood</a></li>
<li><a href="elara_nightshade.html">elara_nightshade</a></li>
<li><a href="foobar.html">foobar</a></li>
<li><a href="kaelar_stormcaller.html">kaelar_stormcaller</a></li>
<li><a href="stoneshaper_golem.html">stoneshaper_golem</a></li>
<li><a href="thorne_ironfist.html">thorne_ironfist</a></li>
<li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
'''

    assert alphabetize_links(input_links) == expected_output
    

def test_alphabetize_links_empty_input():
    """
    Test case to verify behavior with empty input.
    """
    input_links = ""
    assert alphabetize_links(input_links) == ""
    

def test_alphabetize_links_with_single_link():
    """
    Test case to verify behavior with a single link.
    """
    input_links = '<li><a href="test.html">Test</a></li>'
    expected_output = '<li><a href="test.html">Test</a></li>'
    assert alphabetize_links(input_links).strip() == expected_output.strip()


@pytest.fixture
def mmorpdnd_instance():
    """
    Fixture to provide an instance of the MMORPDND class for testing.
    """
    return MMORPDND()
    

def test_create_directories(tmp_path, mmorpdnd_instance):
    """
    Test case to verify the creation of directories based on the specified structure.
    """
    # Define the directory structure
    directory_structure = {
        "folder1": {
            "subfolder1": {},
            "subfolder2": {
                "subsubfolder1": {}
            }
        },
        "folder2": {}
    }

    # Define the root path
    root_path = tmp_path / "test_directory"

    # Call the create_directories method
    mmorpdnd_instance.create_directories(root_path, directory_structure)

    # Verify that the directories are created as expected
    assert os.path.exists(root_path)

    # Check the created directory structure
    assert os.path.exists(root_path / "folder1")
    assert os.path.exists(root_path / "folder1" / "subfolder1")
    assert os.path.exists(root_path / "folder1" / "subfolder2")
    assert os.path.exists(root_path / "folder1" / "subfolder2" / "subsubfolder1")
    assert os.path.exists(root_path / "folder2")


def test_create_index_files(tmp_path, mmorpdnd_instance):
    """
    Test case to verify the creation of index files in directories.
    """
    # Define a directory structure
    directory_structure = {
        "dir1": {
            "subdir1": {
                "file1.txt": {}
            },
            "subdir2": {}
        },
        "dir2": {}
    }

    # Create the directory structure
    create_directory_structure(tmp_path, directory_structure)
        
    # Print contents of the source directory before moving
    print(f"Contents of {tmp_path} before index file creation:")
    print(os.listdir(tmp_path))

    # Call the create_index_files method
    mmorpdnd_instance.create_index_files(tmp_path)

    # Verify that index files are created where necessary
    assert os.path.exists(tmp_path / "dir1" / "index.html")
    assert os.path.exists(tmp_path / "dir1" / "subdir1" / "index.html")
    assert os.path.exists(tmp_path / "dir1" / "subdir2" / "index.html")
    assert os.path.exists(tmp_path / "dir2" / "index.html")

    # Check the content of index files
    with open(tmp_path / "dir1" / "index.html", 'r') as f:
        content = f.read()
        assert "Index of dir1" in content
    with open(tmp_path / "dir1" / "subdir1" / "index.html", 'r') as f:
        content = f.read()
        assert "Index of subdir1" in content
    with open(tmp_path / "dir1" / "subdir2" / "index.html", 'r') as f:
        content = f.read()
        assert "Index of subdir2" in content
    with open(tmp_path / "dir2" / "index.html", 'r') as f:
        content = f.read()
        assert "Index of dir2" in content
        

def test_create_index_files_with_existing_index_files(tmp_path, mmorpdnd_instance):
    """
    Test case to verify that existing index files are not overwritten.
    """
    # Create an index file in a directory
    index_file_path = tmp_path / "existing_index" / "index.html"
    os.makedirs(tmp_path / "existing_index")
    with open(index_file_path, 'w') as f:
        f.write("Existing index file content")

    # Call the create_index_files method
    mmorpdnd_instance.create_index_files(tmp_path)

    # Verify that the existing index file is not overwritten
    assert os.path.exists(index_file_path)
    with open(index_file_path, 'r') as f:
        content = f.read()
        assert content == "Existing index file content"


def test_create_index_files_with_excluded_directories(tmp_path, mmorpdnd_instance):
    """
    Test case to verify that directories specified in global_vars.directories_to_exclude are skipped.
    """
    # Define excluded directories
    excluded_directories = ["templates"]

    # Define directory structure with an excluded directory
    directory_structure = {
        "templates": {
            "file.txt": {}
        },
        "included_dir": {}
    }

    # Create the directory structure
    create_directory_structure(tmp_path, directory_structure)

    # Call the create_index_files method
    mmorpdnd_instance.create_index_files(tmp_path)

    # Verify that index files are not created in excluded directories
    assert not os.path.exists(tmp_path / "templates" / "index.html")
    assert os.path.exists(tmp_path / "included_dir" / "index.html")


def create_directory_structure(root_dir: str, structure: dict) -> None:
    """
    Helper function to create a directory structure for testing.

    Args:
        root_dir (str): The root directory where the structure will be created.
        structure (dict): A dictionary representing the structure of directories and files.

    Returns:
        None.
    """
    for key in structure:
        subpath = os.path.join(root_dir, key)
        if not os.path.exists(subpath):
            os.makedirs(subpath)
            print(f"Created directory: {subpath}")
        if structure[key]:
            create_directory_structure(os.path.join(root_dir, key), structure[key])


def test_move_dir_items_to_end_no_dir_items(mmorpdnd_instance):
    """
    Test case to verify behavior when there are no directory items in the input string.
    """
    input_string = "Line 1\nLine 2\nLine 3"
    assert mmorpdnd_instance.move_dir_items_to_end(input_string) == input_string
    

def test_move_dir_items_to_end_single_dir_item(mmorpdnd_instance):
    """
    Test case to verify behavior when there is only one directory item in the input string.
    """
    input_string = "Line 1\n/index.html\nLine 2\nLine 3"
    expected_result = "Line 1\nLine 2\nLine 3\n/index.html"
    assert mmorpdnd_instance.move_dir_items_to_end(input_string) == expected_result
    

def test_move_dir_items_to_end_multiple_dir_items(mmorpdnd_instance):
    """
    Test case to verify behavior when there are multiple directory items in the input string.
    """
    input_string = "Line 1\n/index.html\nLine 2\nLine 3\n/index.html"
    expected_result = "Line 1\nLine 2\nLine 3\n/index.html\n/index.html"
    assert mmorpdnd_instance.move_dir_items_to_end(input_string) == expected_result
    

def test_move_dir_items_to_end_mixed_items_order_preserved(mmorpdnd_instance):
    """
    Test case to verify behavior when there are mixed directory and non-directory items, and their order is preserved.
    """
    input_string = "Line 1\n/index.html\nLine 2\nLine 3\n/index.html\nLine 4\n/index.html"
    expected_result = "Line 1\nLine 2\nLine 3\nLine 4\n/index.html\n/index.html\n/index.html"
    assert mmorpdnd_instance.move_dir_items_to_end(input_string) == expected_result
    

def test_move_dir_items_to_end_empty_string(mmorpdnd_instance):
    """
    Test case to verify behavior when the input string is empty.
    """
    input_string = ""
    assert mmorpdnd_instance.move_dir_items_to_end(input_string) == ""


def test_move_img_items_to_end_no_img_items(mmorpdnd_instance):
    """
    Test case to verify behavior when there are no items containing "img/" in the input string.
    """
    input_string = '''<li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
                      <li><a href="kaelar_stormcaller.html">kaelar_stormcaller</a></li>
                      <li><a href="thorne_ironfist.html">thorne_ironfist</a></li>'''
    assert mmorpdnd_instance.move_img_items_to_end(input_string) == input_string


def test_move_img_items_to_end_single_img_item(mmorpdnd_instance):
    """
    Test case to verify behavior when there is only one item containing "img/" in the input string.
    """
    input_string = '''<li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
                      <li><a href="kaelar_stormcaller.html">kaelar_stormcaller</a></li>
                      <li><a href="img/foobar.html">img/foobar</a></li>
                      <li><a href="thorne_ironfist.html">thorne_ironfist</a></li>'''
    expected_result = '''<li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
                      <li><a href="kaelar_stormcaller.html">kaelar_stormcaller</a></li>
                      <li><a href="thorne_ironfist.html">thorne_ironfist</a></li>
                      <li><a href="img/foobar.html">img/foobar</a></li>'''
    assert mmorpdnd_instance.move_img_items_to_end(input_string) == expected_result


def test_move_img_items_to_end_multiple_img_items(mmorpdnd_instance):
    """
    Test case to verify behavior when there are multiple items containing "img/" in the input string.
    """
    input_string = '''<li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
                      <li><a href="img/aria_thistlewood.html">img/aria_thistlewood</a></li>
                      <li><a href="stoneshaper_golem.html">stoneshaper_golem</a></li>
                      <li><a href="img/foobar.html">img/foobar</a></li>
                      <li><a href="elara_nightshade.html">elara_nightshade</a></li>'''
    expected_result = '''<li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
                      <li><a href="stoneshaper_golem.html">stoneshaper_golem</a></li>
                      <li><a href="elara_nightshade.html">elara_nightshade</a></li>
                      <li><a href="img/aria_thistlewood.html">img/aria_thistlewood</a></li>
                      <li><a href="img/foobar.html">img/foobar</a></li>'''
    assert mmorpdnd_instance.move_img_items_to_end(input_string) == expected_result


def test_move_img_items_to_end_mixed_order_preserved(mmorpdnd_instance):
    """
    Test case to verify behavior when there are mixed items and their order is preserved.
    """
    input_string = '''<li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
                      <li><a href="kaelar_stormcaller.html">kaelar_stormcaller</a></li>
                      <li><a href="img/aria_thistlewood.html">img/aria_thistlewood</a></li>
                      <li><a href="stoneshaper_golem.html">stoneshaper_golem</a></li>
                      <li><a href="thorne_ironfist.html">thorne_ironfist</a></li>
                      <li><a href="img/foobar.html">img/foobar</a></li>
                      <li><a href="elara_nightshade.html">elara_nightshade</a></li>'''
    expected_result = '''<li><a href="valen_shadowborn.html">valen_shadowborn</a></li>
                      <li><a href="kaelar_stormcaller.html">kaelar_stormcaller</a></li>
                      <li><a href="stoneshaper_golem.html">stoneshaper_golem</a></li>
                      <li><a href="thorne_ironfist.html">thorne_ironfist</a></li>
                      <li><a href="elara_nightshade.html">elara_nightshade</a></li>
                      <li><a href="img/aria_thistlewood.html">img/aria_thistlewood</a></li>
                      <li><a href="img/foobar.html">img/foobar</a></li>'''
    assert mmorpdnd_instance.move_img_items_to_end(input_string) == expected_result


def test_find_all_html_files_no_html_files(mmorpdnd_instance, tmp_path):
    """
    Test case to verify behavior when no HTML files are present.
    """
    assert mmorpdnd_instance.find_all_html_files(tmp_path) == []


def test_find_all_html_files_single_html_file(mmorpdnd_instance, tmp_path):
    """
    Test case to verify behavior when only one HTML file is present.
    """
    # Create a single HTML file
    test_file_path = tmp_path / "test.html"
    test_file_path.touch()

    expected_result = [{
        'name_no_ext': 'test',
        'name_with_ext': 'test.html',
        'full_path': str(test_file_path)
    }]
    assert mmorpdnd_instance.find_all_html_files(tmp_path) == expected_result


def test_find_all_html_files_multiple_html_files(mmorpdnd_instance, tmp_path):
    """
    Test case to verify behavior when multiple HTML files are present.
    """
    # Create multiple HTML files
    html_files = ["file1.html", "file2.html", "file3.html"]
    for filename in html_files:
        (tmp_path / filename).touch()

    expected_result = [
        {'name_no_ext': 'file1', 'name_with_ext': 'file1.html', 'full_path': str(tmp_path / "file1.html")},
        {'name_no_ext': 'file2', 'name_with_ext': 'file2.html', 'full_path': str(tmp_path / "file2.html")},
        {'name_no_ext': 'file3', 'name_with_ext': 'file3.html', 'full_path': str(tmp_path / "file3.html")}
    ]
    
    # Add some sorting since they could be read in a different order.
    sorted_list1 = sorted(mmorpdnd_instance.find_all_html_files(tmp_path), key=lambda x: x['name_no_ext'])
    sorted_list2 = sorted(expected_result, key=lambda x: x['name_no_ext'])
    assert sorted_list1 == sorted_list2
    
    
def test_find_all_html_files_multiple_html_files_and_directories(mmorpdnd_instance, tmp_path):
    """
    Test case to verify behavior when multiple HTML files are present in multiple directories.
    """
    # Create multiple HTML files
    html_files = ["file1.html", "file2.html", "file3.html"]
    for filename in html_files:
        (tmp_path / filename).touch()
    (tmp_path / "dir").mkdir()
    (tmp_path / "dir" / "file4.html").touch()

    expected_result = [
        {'name_no_ext': 'file1', 'name_with_ext': 'file1.html', 'full_path': str(tmp_path / "file1.html")},
        {'name_no_ext': 'file2', 'name_with_ext': 'file2.html', 'full_path': str(tmp_path / "file2.html")},
        {'name_no_ext': 'file3', 'name_with_ext': 'file3.html', 'full_path': str(tmp_path / "file3.html")},
        {'name_no_ext': 'file4', 'name_with_ext': 'file4.html', 'full_path': str(tmp_path / "dir" / "file4.html")}
    ]
    
    # Add some sorting since they could be read in a different order.
    sorted_list1 = sorted(mmorpdnd_instance.find_all_html_files(tmp_path), key=lambda x: x['name_no_ext'])
    sorted_list2 = sorted(expected_result, key=lambda x: x['name_no_ext'])
    assert sorted_list1 == sorted_list2


def test_find_all_html_files_with_index_html_file(mmorpdnd_instance, tmp_path):
    """
    Test case to verify behavior when an index.html file is present.
    """
    # Create an index.html file
    index_file_path = tmp_path / "index.html"
    index_file_path.touch()

    # Create other HTML files
    (tmp_path / "file1.html").touch()
    (tmp_path / "file2.html").touch()

    expected_result = [
        {'name_no_ext': 'file1', 'name_with_ext': 'file1.html', 'full_path': str(tmp_path / "file1.html")},
        {'name_no_ext': 'file2', 'name_with_ext': 'file2.html', 'full_path': str(tmp_path / "file2.html")}
    ]

    # Add some sorting since they could be read in a different order.
    sorted_list1 = sorted(mmorpdnd_instance.find_all_html_files(tmp_path), key=lambda x: x['name_no_ext'])
    sorted_list2 = sorted(expected_result, key=lambda x: x['name_no_ext'])
    assert sorted_list1 == sorted_list2

