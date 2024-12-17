from unittest.mock import patch, MagicMock

import pytest
from valid8 import ValidationError

from beer_hub.app import App
from beer_hub.domain import Beer, Name, Description, Brewery, BeerType, AlcoholContent, ID
from beer_hub.logic import InMemoryBeerHub


@pytest.fixture
def sample_beer():
    return Beer.of(
        name=Name("Test Beer"),
        description=Description("A test beer description"),
        brewery=Brewery("Test Brewery"),
        beer_type=BeerType("Pale Lager"),
        alcohol_content=AlcoholContent.of("5.0 %")
    )


@pytest.fixture
def mock_beer_hub():
    hub = MagicMock()
    hub.get_beers.return_value = []
    return hub


class TestApp:

    @patch('beer_hub.app.RESTBeerHub')
    def test_select_rest_hub(self, mock_rest):
        mock_rest.login.return_value = MagicMock()
        with patch('builtins.input', side_effect=['2', 'user', 'pass', '0']):
            app = App()
            assert app._App__selected_hub is not None  # Check selected_hub instead of beer_hub

    @patch('beer_hub.app.RESTBeerHub')
    def test_select_rest_hub_retry_login(self, mock_rest):
        mock_rest.login.side_effect = [None, MagicMock()]
        with patch('builtins.input', side_effect=['2', 'user', 'pass', 'user', 'pass', '0']):
            app = App()
            assert app._App__selected_hub is not None

    @patch('beer_hub.app.InMemoryBeerHub')
    def test_select_inmemory_hub(self, mock_inmemory):
        mock_hub_instance = MagicMock(spec=InMemoryBeerHub)
        mock_inmemory.return_value = mock_hub_instance

        with patch('builtins.input', side_effect=['1', '0']):
            app = App()
            assert app._App__selected_hub is not None
            assert app._App__selected_hub == mock_hub_instance

    def test_exit_hub_selection(self):
        with patch('builtins.input', side_effect=['0']):
            with pytest.raises(SystemExit):
                App()

    def test_list_beers(self, mock_beer_hub):
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=['1', '1', '0']):
                app = App()
                app.run()
                mock_beer_hub.get_beers.assert_called_once()

    def test_add_beer(self, mock_beer_hub):
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '2',  # Select add beer
                'Test Beer',  # Name
                'Description',  # Description
                'Brewery',  # Brewery
                'Pale Lager',  # Beer Type
                '5.0',  # Alcohol Content
                '0'  # Exit
            ]):
                app = App()
                app.run()
                mock_beer_hub.add_beer.assert_called_once()

    def test_search_by_id(self, mock_beer_hub, sample_beer):
        mock_beer_hub.get_beer_by_id.return_value = sample_beer
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '3',  # Search menu
                '1',  # Search by ID
                '1',  # ID value
                '0',  # Exit
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.get_beer_by_id.assert_called_once()

    def test_search_by_name(self, mock_beer_hub, sample_beer):
        mock_beer_hub.get_beer_by_name.return_value = sample_beer
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '3',  # Search menu
                '2',  # Search by name
                'Test Beer',  # Name value
                '0',  # Exit search menu
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.get_beer_by_name.assert_called_once()

    def test_update_beer(self, mock_beer_hub, sample_beer):
        mock_beer_hub.get_beer_by_id.return_value = sample_beer
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '4',  # Update beer
                '1',  # Beer ID
                'Updated Beer',  # New name
                'Updated Desc',  # New description
                'Updated Brewery',  # New brewery
                'Pale Lager',  # New beer type
                '6.0',  # New alcohol content
                '0'  # Exit
            ]):
                app = App()
                app.run()
                mock_beer_hub.update_beer_by_id.assert_called_once()

    def test_delete_beer(self, mock_beer_hub, sample_beer):
        mock_beer_hub.get_beer_by_id.return_value = sample_beer
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '5',  # Delete beer
                '1',  # Beer ID
                '0'  # Exit
            ]):
                app = App()
                app.run()
                mock_beer_hub.delete_beer_by_id.assert_called_once()

    def test_list_breweries(self, mock_beer_hub):
        mock_beer_hub.get_breweries.return_value = [Brewery("Test Brewery")]
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '6',  # Brewery operations
                '1',  # List breweries
                '0',  # Exit brewery menu
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.get_breweries.assert_called_once()

    def test_filter_by_brewery(self, mock_beer_hub, sample_beer):
        mock_beer_hub.get_beers_by_brewery.return_value = [sample_beer]
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '6',  # Brewery operations
                '2',  # Filter by brewery
                'Test Brewery',  # Brewery name
                '0',  # Exit brewery menu
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.get_beers_by_brewery.assert_called_once()

    def test_sort_ascending_alcohol(self, mock_beer_hub):
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '7',  # Sort operations
                '1',  # Sort ascending
                '0',  # Exit sort menu
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.get_beers_by_ascending_alcohol_content.assert_called_once()

    def test_sort_descending_alcohol(self, mock_beer_hub):
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '7',  # Sort operations
                '2',  # Sort descending
                '0',  # Exit sort menu
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.get_beers_by_descending_alcohol_content.assert_called_once()

    def test_statistics_total_beers(self, mock_beer_hub):
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '8',  # Statistics
                '1',  # Total beers
                '0',  # Exit statistics menu
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.number_of_beers.assert_called_once()

    def test_statistics_total_breweries(self, mock_beer_hub):
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '8',  # Statistics
                '2',  # Total breweries
                '0',  # Exit statistics menu
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.number_of_breweries.assert_called_once()

    def test_panic_error(self, mock_beer_hub):
        mock_beer_hub.get_beers.side_effect = Exception("Test error")
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=['1', '1']):
                with patch('builtins.print'):  # Suppress print output
                    app = App()
                    with pytest.raises(Exception):
                        app.run()

    def test_search_by_name_not_found(self, mock_beer_hub):
        mock_beer_hub.get_beer_by_name.return_value = None
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '3',  # Search menu
                '2',  # Search by name
                'Nonexistent Beer',  # Name value
                '0',  # Exit search menu
                '0'  # Exit main menu
            ]):
                with patch('builtins.print') as mock_print:
                    app = App()
                    app.run()
                    mock_print.assert_any_call('Beer with given name does not exist!')

    def test_update_beer_cancel(self, mock_beer_hub):
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '4',  # Update beer
                '-1',  # Cancel update
                '0'  # Exit
            ]):
                with patch('builtins.print') as mock_print:
                    app = App()
                    app.run()
                    mock_print.assert_any_call('Cancelled!')

    def test_print_empty_breweries(self, mock_beer_hub):
        mock_beer_hub.get_breweries.return_value = []
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '6',  # Brewery operations
                '1',  # List breweries
                '0',  # Exit brewery menu
                '0'  # Exit main menu
            ]):
                with patch('builtins.print') as mock_print:
                    app = App()
                    app.run()
                    mock_print.assert_any_call("No breweries to display")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_read_with_type_error(self, mock_print, mock_input):
        # Setup
        mock_input.side_effect = ['invalid', 'valid']
        type_error = TypeError('Type error')

        def builder(value):
            if value == 'invalid':
                raise type_error
            return value

        # Execute
        result = App._App__read('Test prompt', builder)

        # Assert
        assert result == 'valid'
        assert mock_print.call_args_list[0][0][0] == type_error
        assert mock_input.call_count == 2

    @patch('beer_hub.app.InMemoryBeerHub')
    def test_update_beer_nonexistent_id(self, mock_hub):
        # Setup
        mock_hub_instance = MagicMock()
        mock_hub_instance.get_beer_by_id.return_value = None
        mock_hub.return_value = mock_hub_instance

        with patch('builtins.input', side_effect=['1', '0']):
            app = App()
            # Mock the __read method to first return an ID, then raise the ValueError
            with patch.object(app, '_App__read') as mock_read:
                def read_side_effect(prompt, builder):
                    if 'updated' in prompt.lower():
                        raise ValueError('Beer with given id does not exist!')

                mock_read.side_effect = read_side_effect

                # Execute & Assert
                with pytest.raises(ValueError, match='Beer with given id does not exist!'):
                    app._App__update_beer_by_id()

    @patch('beer_hub.app.InMemoryBeerHub')
    @patch('builtins.print')
    def test_delete_beer_cancel_case(self, mock_print, mock_hub):
        mock_hub_instance = MagicMock()
        mock_hub.return_value = mock_hub_instance

        with patch('builtins.input', side_effect=['1', '0']):  # Added '0' for menu exit
            app = App()
            with patch.object(app, '_App__read') as mock_read:
                mock_read.return_value = None  # Simulate -1 input
                app._App__delete_beer_by_id()

        mock_print.assert_called_with('Cancelled!')
        assert not mock_hub_instance.delete_beer_by_id.called

    @patch('beer_hub.app.InMemoryBeerHub')
    @patch('builtins.print')
    def test_update_beer_cancel_case(self, mock_print, mock_hub):
        mock_hub_instance = MagicMock()
        mock_hub.return_value = mock_hub_instance

        with patch('builtins.input', side_effect=['1', '0']):  # Added '0' for menu exit
            app = App()
            with patch.object(app, '_App__read') as mock_read:
                mock_read.return_value = None  # Simulate -1 input
                app._App__update_beer_by_id()

        mock_print.assert_called_with('Cancelled!')

    def test_print_beer_by_id_invalid_input(self, mock_beer_hub):
        """Test handling of invalid input when searching by ID"""
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '3',  # Search menu
                '1',  # Search by ID
                'invalid',  # Invalid ID input
                '1',  # Valid ID input
                '0',  # Exit search menu
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.get_beer_by_id.assert_called_once()

    def test_print_beer_by_id_negative_input(self, mock_beer_hub):
        """Test handling of negative ID input"""
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '3',  # Search menu
                '1',  # Search by ID
                '-5',  # Negative ID input
                '1',  # Valid ID input
                '0',  # Exit search menu
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.get_beer_by_id.assert_called_once()

    def test_delete_beer_invalid_id_input(self, mock_beer_hub):
        """Test handling of invalid ID input during deletion"""
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '5',  # Delete beer
                'invalid',  # Invalid ID
                '-1',  # Cancel deletion
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.delete_beer_by_id.assert_not_called()

    def test_update_beer_with_long_description(self, mock_beer_hub, sample_beer):
        mock_beer_hub.get_beer_by_id.return_value = sample_beer

        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '4',  # Update beer
                '1',  # Beer ID
                'New Name',  # New name
                'A very long description that should be truncated in the display',  # New description
                'New Brewery',  # New brewery
                'Pale Ale',  # New beer type
                '5.5',  # New alcohol content
                '0'  # Exit
            ]):
                app = App()
                app.run()
                mock_beer_hub.update_beer_by_id.assert_called_once()

    def test_validate_beer_id_boundary_values(self, mock_beer_hub):
        """Test boundary values for beer ID validation"""
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '3',  # Search menu
                '1',  # Search by ID
                '0',  # Boundary value
                '0',  # Exit search menu
                '0'  # Exit main menu
            ]):
                app = App()
                app.run()
                mock_beer_hub.get_beer_by_id.assert_called_once_with(ID(0))

    def test_print_beer_by_id_not_found(self, mock_beer_hub):
        """Test the case where a beer with the given ID does not exist."""
        mock_beer_hub.get_beer_by_id.return_value = None
        with patch('beer_hub.app.InMemoryBeerHub', return_value=mock_beer_hub):
            with patch('builtins.input', side_effect=[
                '1',  # Select InMemory hub
                '3',  # Search menu
                '1',  # Search by ID
                '999',  # Nonexistent ID
                '0',  # Exit search menu
                '0'  # Exit main menu
            ]):
                with patch('builtins.print') as mock_print:
                    app = App()
                    app.run()
                    mock_print.assert_any_call('Beer with given id does not exist!')

    @patch('beer_hub.app.InMemoryBeerHub')
    def test_update_beer_by_id_not_found(self, mock_hub):
        """Test the builder function in __update_beer_by_id raises ValueError when beer is not found."""
        mock_hub_instance = MagicMock()
        mock_hub_instance.get_beer_by_id.return_value = None  # Simulate beer not found
        mock_hub.return_value = mock_hub_instance

        with patch('builtins.input', side_effect=['1', '0']):  # Added '0' for menu exit
            app = App()
            # Mock the __read method to simulate user input and trigger the builder
            with patch.object(app, '_App__read') as mock_read:
                def read_side_effect(prompt, builder):
                    if 'id of beer' in prompt.lower():
                        return builder('999')  # Simulate user entering ID 999

                mock_read.side_effect = read_side_effect

                # Execute & Assert
                with pytest.raises(ValueError):
                    app._App__update_beer_by_id()

    @patch('beer_hub.app.InMemoryBeerHub')
    def test_delete_beer_by_id_builder_raises_error(self, mock_hub):
        """Test the builder function in __delete_beer_by_id raises ValueError when beer is not found."""
        mock_hub_instance = MagicMock()
        mock_hub_instance.get_beer_by_id.return_value = None  # Simulate beer not found
        mock_hub.return_value = mock_hub_instance

        with patch('builtins.input', side_effect=['1', '0']):  # Added '0' for menu exit
            app = App()
            # Mock the __read method to simulate user input and trigger the builder
            with patch.object(app, '_App__read') as mock_read:
                def read_side_effect(prompt, builder):
                    if 'id of beer' in prompt.lower():
                        return builder('999')  # Simulate user entering ID 999

                mock_read.side_effect = read_side_effect

                # Execute & Assert
                with pytest.raises(ValueError):
                    app._App__delete_beer_by_id()
