import pytest
from ide import AndroidStudio, IntelliJ
from project import (
    game_settings,
    quiz_settings,
    command_line_ide,
    ask_user_ide,
    ask_user_level,
    ask_user_system,
)
from exceptions import InvalidChoiceError
from io import StringIO


def test_command_line_ide():
    with pytest.raises(SystemExit):
        assert command_line_ide(["-s", "mac", "pear phone", "senior"])
    with pytest.raises(SystemExit):
        assert command_line_ide(["rainbow trout", "senior"])


def test_game_settings_intellij_valid():
    assert isinstance(game_settings("intellij", "executive"), IntelliJ) is True
    assert isinstance(game_settings("intellij", "senior"), IntelliJ) is True


def test_game_settings_android_valid():
    assert (
        isinstance(game_settings("android studio", "executive", "mac"), AndroidStudio)
        is True
    )
    assert (
        isinstance(game_settings("android", "junior", "linux"), AndroidStudio) is True
    )


def test_game_settings_level_errors():
    with pytest.raises(InvalidChoiceError):
        assert game_settings("intellij", "steve young")
    with pytest.raises(InvalidChoiceError):
        assert game_settings("android", "1932")


def test_game_settings_system_errors():
    with pytest.raises(InvalidChoiceError):
        assert game_settings("android studio", "junior", "tatsumaki")
    with pytest.raises(InvalidChoiceError):
        assert game_settings("android", "executive", "nico robin")


def test_quiz_settings_valid():
    assert quiz_settings("junior") == (1, 2)
    assert quiz_settings("senior") == (2, 4)
    assert quiz_settings("executive") == (3, 6)


def test_quiz_settings_errors():
    with pytest.raises(InvalidChoiceError):
        assert quiz_settings("your mom")
    with pytest.raises(InvalidChoiceError):
        assert quiz_settings("mr.robot")


def test_double_ide_errors_one(monkeypatch):
    test_input = StringIO("cheerios")
    monkeypatch.setattr("sys.stdin", test_input)
    with pytest.raises(EOFError):
        assert ask_user_ide()


def test_double_ide_errors_two(monkeypatch):
    test_input = StringIO("1234")
    monkeypatch.setattr("sys.stdin", test_input)
    with pytest.raises(EOFError):
        assert ask_user_ide()


def test_double_level_errors_one(monkeypatch):
    test_input = StringIO("pink panther")
    monkeypatch.setattr("sys.stdin", test_input)
    with pytest.raises(EOFError):
        assert ask_user_level()


def test_double_level_errors_two(monkeypatch):
    test_input = StringIO("@@@@@@@")
    monkeypatch.setattr("sys.stdin", test_input)
    with pytest.raises(EOFError):
        assert ask_user_level()


def test_double_system_errors_one(monkeypatch):
    test_input = StringIO("sunshine")
    monkeypatch.setattr("sys.stdin", test_input)
    with pytest.raises(EOFError):
        assert ask_user_system()


def test_double_system_errors_two(monkeypatch):
    test_input = StringIO("winter berry")
    monkeypatch.setattr("sys.stdin", test_input)
    with pytest.raises(EOFError):
        assert ask_user_system()
