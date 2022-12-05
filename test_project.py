from project import is_name_valid
from project import database_exists
from project import get_title

def test_is_name_valid():
    assert is_name_valid("davidom") == True
    assert is_name_valid("javier hi") == False
    assert is_name_valid("example_1-2") == True
    assert is_name_valid("example&") == False


def test_database_exists():
    assert database_exists("davidom") == True
    assert database_exists("example") == True
    assert database_exists("davidjmalan") == False
    assert database_exists("jajajaja_joke") == False


def test_get_title():
    assert get_title("hola") == "\t\t**********\n\t\t*  HOLA  *\n\t\t**********"
    assert get_title("HoLa") == "\t\t**********\n\t\t*  HOLA  *\n\t\t**********"
    assert get_title("cs50") == "\t\t**********\n\t\t*  CS50  *\n\t\t**********"
    assert get_title("new task") == "\t\t**************\n\t\t*  NEW TASK  *\n\t\t**************"
