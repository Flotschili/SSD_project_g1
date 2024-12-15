import pytest
from unittest.mock import patch, mock_open
from beer_hub.__main__ import main


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_main(mocked_print, mocked_input):
    with patch('builtins.open', mock_open()):
        with pytest.raises(SystemExit) as exit_info:
            main('__main__')

        # Verify exit code is 0
        assert exit_info.value.code == 0

        # Verify the menu was displayed correctly
        mocked_print.assert_any_call('*************************************')
        mocked_print.assert_any_call('*** Select BeerHub Implementation ***')
        mocked_print.assert_any_call('*************************************')
        mocked_print.assert_any_call('1:\tInMemory BeerHub')
        mocked_print.assert_any_call('2:\tREST BeerHub')
        mocked_print.assert_any_call('0:\tExit')

        # Verify input was called
        mocked_input.assert_called_once_with('? ')
