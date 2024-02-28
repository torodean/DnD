#!/bin/python3
import os
import tempfile
import pytest
import sys
sys.path.append('../')
from creator import *


@pytest.fixture
def temp_dir():
    """
    Fixture to create a temporary directory for testing.
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    
@pytest.fixture
def temp_file(tmp_path):
    """
    Fixture to provide a temporary file path for testing.
    """
    file_path = tmp_path / "test_file.txt"
    yield file_path


def test_ensure_directory_exists_does_not_exist(temp_dir):
    """
    Test case to verify behavior when the directory does not exist.
    """
    directory_path = os.path.join(temp_dir, "test_directory")
    ensure_directory_exists(directory_path)
    assert os.path.exists(directory_path)

def test_ensure_directory_exists_already_exists(temp_dir):
    """
    Test case to verify behavior when the directory already exists.
    """
    directory_path = os.path.join(temp_dir, "test_directory")
    os.makedirs(directory_path)
    ensure_directory_exists(directory_path)
    assert os.path.exists(directory_path)


def test_find_longest_and_shortest_non_empty_list():
    """
    Test case to verify behavior with a non-empty list.
    """
    word_list = ["one", "two", "three", "four", "five"]
    shortest_length, longest_length = find_longest_and_shortest(word_list)
    assert longest_length == 5
    assert shortest_length == 3
    

def test_find_longest_and_shortest_empty_list():
    """
    Test case to verify behavior with an empty list.
    """
    word_list = []
    try:
        find_longest_and_shortest(word_list)
    except ValueError as e:
        assert str(e) == "Input list cannot be empty."


def test_remove_numbers_at_start_empty_string():
    """
    Test case to verify behavior when an empty string is provided.
    """
    assert remove_numbers_at_start("") == ""


def test_remove_numbers_at_start_no_numbers():
    """
    Test case to verify behavior when the string does not start with numbers.
    """
    assert remove_numbers_at_start("abc123") == "abc123"
    assert remove_numbers_at_start("xyz") == "xyz"


def test_remove_numbers_at_start_with_numbers():
    """
    Test case to verify behavior when the string starts with numbers.
    """
    assert remove_numbers_at_start("123abc") == "abc"
    assert remove_numbers_at_start("456def") == "def"
    assert remove_numbers_at_start("007bond") == "bond"
    assert remove_numbers_at_start("007 bond") == "bond"


def test_append_to_file(tmp_path, temp_file):
    """
    Test appending a string to a file with existing content.
    """
    # Initial content of the file
    initial_content = "Line 1\nLine 2\nLine 3\n"
    with open(temp_file, 'w') as file:
        file.write(initial_content)

    # String to append
    string_to_append = "New line"

    # Append the string to the file
    append_to_file(temp_file, string_to_append)

    # Read the file and check if the string was appended
    with open(temp_file, 'r') as file:
        updated_content = file.read()

    expected_content = initial_content + string_to_append + '\n'
    assert updated_content == expected_content


def test_append_to_file_empty_file(tmp_path, temp_file):
    """
    Test appending a string to an empty file.
    """
    # Create an empty file
    open(temp_file, 'a').close()

    # String to append
    string_to_append = "New line"

    # Append the string to the file
    append_to_file(temp_file, string_to_append)

    # Read the file and check if the string was appended
    with open(temp_file, 'r') as file:
        updated_content = file.read()

    expected_content = string_to_append + '\n'
    assert updated_content == expected_content


def test_read_lines_from_file_existing_file(tmp_path):
    """
    Test reading lines from an existing file.
    """
    # Create a test file with content
    file_content = "Line 1\nLine 2\nLine 3\n"
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w") as file:
        file.write(file_content)

    # Read lines from the file
    lines = read_lines_from_file(file_path)

    # Check if the lines are read correctly
    assert lines == ["Line 1", "Line 2", "Line 3"]


def test_read_lines_from_file_nonexistent_file(tmp_path):
    """
    Test handling a nonexistent file.
    """
    # Attempt to read lines from a nonexistent file
    non_existing_file = tmp_path / "non_existing_file.txt"
    with pytest.raises(FileNotFoundError):
        read_lines_from_file(non_existing_file)


def test_read_lines_from_file_permission_error(tmp_path):
    """
    Test handling a permission error.
    """
    # Create a file with restricted permissions
    restricted_file = tmp_path / "restricted_file.txt"
    with open(restricted_file, "w") as file:
        file.write("Some content")
    # Change permissions to read-only
    restricted_file.chmod(0o000)

    # Attempt to read lines from the restricted file
    with pytest.raises(PermissionError):
        read_lines_from_file(restricted_file)


def test_calculate_hp_barbarian():
    """
    Test case to verify the calculated hit points for a Barbarian character at level 5 and constitution 18.
    The test checks if the calculated hit points fall within the expected range (36 to 80).
    """
    for i in range(1, 100):
        assert 36 <= calculate_hp("barbarian", 5, 18) <= 80


def test_calculate_hp_fighter():
    """
    Test case to verify the calculated hit points for a fighter character at level 5 and constitution 18.
    The test checks if the calculated hit points fall within the expected range (49 to 130).
    """
    for i in range(1, 100):
        assert 49 <= calculate_hp("fighter", 10, 16) <= 130


def test_calculate_hp_cleric():
    """
    Test case to verify the calculated hit points for a cleric character at level 5 and constitution 18.
    The test checks if the calculated hit points fall within the expected range (28 to 130).
    """
    for i in range(1, 100):
        assert 28 <= calculate_hp("cleric", 7, 14) <= 70


def test_calculate_hp_wizard():
    """
    Test case to verify the calculated hit points for a wizard character at level 5 and constitution 18.
    The test checks if the calculated hit points fall within the expected range (5 to 85).
    """
    for i in range(1, 100):
        assert 5 <= calculate_hp("wizard", 17, 8) <= 85
        

def test_calculate_hp_unknown_class():
    """
    Test case to verify behavior when an unknown class is provided to the calculate_hp function.
    The test checks if a ValueError is raised when an unrecognized class type is provided.
    """
    with pytest.raises(ValueError):
        calculate_hp("warrior", 5, 14)


def test_calculate_proficiency_bonus():
    """
    Test cases to verify proficiency bonus calculation for different levels.
    """
    assert calculate_proficiency_bonus(1) == 2
    assert calculate_proficiency_bonus(7) == 3
    assert calculate_proficiency_bonus(10) == 4
    assert calculate_proficiency_bonus(15) == 5
    assert calculate_proficiency_bonus(20) == 6
    assert calculate_proficiency_bonus(25) == 6  # Proficiency bonus should cap at 6 for levels above 20


def test_roll_4d6_drop_lowest():
    """
    Test case to verify the functionality of the roll_4d6_drop_lowest function.
    """
    # Test the function multiple times to ensure randomness
    for _ in range(10):
        result = roll_4d6_drop_lowest(False)
        assert isinstance(result, int)  # Check if the result is an integer
        assert 3 <= result <= 18  # The sum of three highest dice should be between 3 and 18


def test_roll_4d6_drop_lowest_average():
    """
    Test case to verify the average value of rolling 4d6 and dropping the lowest.
    """
    # Test the function multiple times to ensure randomness
    results = [roll_4d6_drop_lowest(False) for _ in range(1000)]
    average = sum(results) / len(results)
    assert 11.5 <= average <= 13  # The average should be around 12.24


def test_roll_4d6_drop_lowest_distribution():
    """
    Test case to verify the distribution of rolling 4d6 and dropping the lowest.
    """
    # Test the function multiple times to ensure randomness
    counts = {i: 0 for i in range(3, 19)}  # Initialize count for each possible sum
    for _ in range(10000):
        result = roll_4d6_drop_lowest(False)
        counts[result] += 1
    
    # Assert that each possible sum has been rolled at least once
    for count in counts.values():
        assert count > 0


def test_copy_file_to_directory_success(tmp_path):
    """
    Test case to verify successful copying of a file to a directory.
    """
    # Create a temporary file
    file_path = os.path.join(tmp_path, "test_file.txt")
    with open(file_path, 'w') as f:
        f.write("Test content")

    # Create a temporary directory
    directory_path = os.path.join(tmp_path, "test_directory")
    os.makedirs(directory_path)

    # Copy the file to the directory
    copy_file_to_directory(file_path, directory_path)

    # Check if the file was copied successfully
    copied_file_path = os.path.join(directory_path, "test_file.txt")
    assert os.path.isfile(copied_file_path)

    # Check the contents of the copied file
    with open(copied_file_path, 'r') as copied_file:
        assert copied_file.read() == "Test content"


def test_copy_file_to_directory_file_not_exist(tmp_path):
    """
    Test case to verify behavior when the file doesn't exist.
    """
    # Create a temporary directory
    directory_path = os.path.join(tmp_path, "test_directory")
    os.makedirs(directory_path)

    # Try to copy a non-existing file to the directory
    with pytest.raises(ValueError):
        copy_file_to_directory("non_existing_file.txt", directory_path)


def test_copy_file_to_directory_directory_not_exist(tmp_path):
    """
    Test case to verify behavior when the directory doesn't exist.
    """
    # Create a temporary file
    file_path = os.path.join(tmp_path, "test_file.txt")
    with open(file_path, 'w') as f:
        f.write("Test content")

    # Create a temporary directory
    directory_path = os.path.join(tmp_path, "test_directory")

    # Copy the file to the directory
    copy_file_to_directory(file_path, directory_path)

    # Check if the file was copied successfully
    copied_file_path = os.path.join(directory_path, "test_file.txt")
    assert os.path.isfile(copied_file_path)

    # Check the contents of the copied file
    with open(copied_file_path, 'r') as copied_file:
        assert copied_file.read() == "Test content"


def test_move_file_to_directory_success(tmp_path):
    """
    Test case to verify successful moving of a file to a directory.
    """
    # Create a temporary file
    file_path = os.path.join(tmp_path, "test_file.txt")
    with open(file_path, 'w') as f:
        f.write("Test content")

    # Create a temporary directory
    directory_path = os.path.join(tmp_path, "test_directory")
    os.makedirs(directory_path)

    # Move the file to the directory
    move_file_to_directory(file_path, directory_path)

    # Check if the file was moved successfully
    moved_file_path = os.path.join(directory_path, "test_file.txt")
    assert os.path.isfile(moved_file_path)
    assert not os.path.isfile(file_path)

    # Check the contents of the moved file
    with open(moved_file_path, 'r') as moved_file:
        assert moved_file.read() == "Test content"


def test_move_file_to_directory_file_not_exist(tmp_path):
    """
    Test case to verify behavior when the file does not exist.
    """
    # Attempt to move a non-existent file to a directory
    with pytest.raises(ValueError):
        move_file_to_directory("non_existent_file.txt", tmp_path)


def test_move_file_to_directory_directory_not_exist(tmp_path):
    """
    Test case to verify behavior when the destination directory does not exist.
    """
    # Create a temporary file
    file_path = os.path.join(tmp_path, "test_file.txt")
    with open(file_path, 'w') as f:
        f.write("Test content")

    # Create a temporary directory
    directory_path = os.path.join(tmp_path, "test_directory")

    # Move the file to the directory
    move_file_to_directory(file_path, directory_path)

    # Check if the file was moved successfully
    moved_file_path = os.path.join(directory_path, "test_file.txt")
    assert os.path.isfile(moved_file_path)
    assert not os.path.isfile(file_path)

    # Check the contents of the moved file
    with open(moved_file_path, 'r') as moved_file:
        assert moved_file.read() == "Test content"
