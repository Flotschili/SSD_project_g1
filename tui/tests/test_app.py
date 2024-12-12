from pathlib import Path
from unittest.mock import patch, mock_open, Mock

import pytest

from beer_hub.__main__ import main
from beer_hub.app import App

_print = print


@pytest.fixture
def mock_path():
    Path.exists = Mock()
    Path.exists.return_value = True
    return Path


@pytest.fixture
def data():
    data = [
        ['author 1', 'title 1', 'genre 1', '1:11'],
        ['author 2', 'title 2', 'genre 2', '0:11'],
        ['author 1', 'title 3', 'genre 3', '2:11'],
    ]
    return '\n'.join(['\t'.join(d) for d in data])


def assert_in_output(mocked_print, expected):
    mock_calls = '\n'.join([''.join(mock_call.args) for mock_call in mocked_print.mock_calls])
    assert expected.strip() in mock_calls


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_main(mocked_print, mocked_input):
    with patch.object(Path, 'exists') as mocked_path_exists:
        mocked_path_exists.return_value = False
        with patch('builtins.open', mock_open()):
            main('__main__')
            mocked_print.assert_any_call('*** Music Archive 2024 ***')
            mocked_print.assert_any_call('0:\tExit')
            mocked_print.assert_any_call('Bye!')
            mocked_input.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_load_datafile(mocked_print, mocked_input, mock_path, data):
    with patch('builtins.open', mock_open(read_data=data)):
        App().run()
    mock_path.exists.assert_called_once()
    assert_in_output(mocked_print, 'author 1')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_handles_corrupted_datafile(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open(read_data='xyz')):
        App().run()
    mocked_print.assert_any_call('Continuing with an empty dataset...')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', 'author', 'title', 'genre', '1:11', '0'])
@patch('builtins.print')
def test_app_add_song(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    assert list(filter(lambda x: 'author' in str(x), mocked_print.mock_calls))

    handle = mocked_open()
    handle.write.assert_called_once_with('author\ttitle\tgenre\t1:11\n')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['2', '1', '2', '1', '0'])
@patch('builtins.print')
def test_app_remove_song(mocked_print, mocked_input, mock_path, data):
    with patch('builtins.open', mock_open(read_data=data)) as mocked_open:
        App().run()
    mocked_input.assert_called()
    mocked_print.assert_called()

    handle = mocked_open()
    expected = data.split('\n')[-1] + '\n'
    assert handle.write.mock_calls[-1].args[0] == expected
    assert handle.write.mock_calls[-2].args[0] == expected
