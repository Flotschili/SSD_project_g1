import sys
from typing import Any, Callable, Optional

from beer_hub_client import Client
from valid8 import validate, ValidationError

from beer_hub import menu
from beer_hub.domain import Beer, Name, Brewery, BeerType, AlcoholContent, ID, Description
from beer_hub.logic import InMemoryBeerHub, RESTBeerHub, BeerHub
from beer_hub.menu import Menu, Entry

BASE_URL = "http://localhost:8000/api/v1"


class App:
    def __init__(self):
        self.__beer_hub = self.__select_beer_hub()
        self.__menu = self.__create_main_menu()

    def __select_beer_hub(self) -> BeerHub:
        def create_inmemory_hub():
            self.__selected_hub = InMemoryBeerHub()

        def create_rest_hub():
            client = Client(base_url=BASE_URL, raise_on_unexpected_status=True)
            authenticated_client = None

            # login loop
            while authenticated_client is None:
                username = self.__read('Username', str)
                password = self.__read('Password', str)
                authenticated_client = RESTBeerHub.login(client, username, password)

                if authenticated_client is None:
                    print("Invalid Credentials! Try again.")

            self.__selected_hub = RESTBeerHub(authenticated_client)

        hub_selection_menu = Menu.Builder(menu.Description('Select BeerHub Implementation'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'InMemory BeerHub',
                                     on_selected=create_inmemory_hub,
                                     is_exit=True)) \
            .with_entry(Entry.create('2', 'REST BeerHub',
                                     on_selected=create_rest_hub,
                                     is_exit=True)) \
            .with_entry(Entry.create('0', 'Exit',
                                     on_selected=lambda: sys.exit(0),
                                     is_exit=True)) \
            .build()

        self.__selected_hub = None
        hub_selection_menu.run()

        if self.__selected_hub is None:
            sys.exit(1)  # Exit if no hub was selected

        return self.__selected_hub

    def __create_main_menu(self):
        return Menu.Builder(menu.Description('BeerHub'))\
            .with_entry(Entry.create('1', 'List all beers',
                                     on_selected=lambda: self.__print_beers())) \
            .with_entry(Entry.create('2', 'Add beer',
                                     on_selected=lambda: self.__add_beer())) \
            .with_entry(Entry.create('3', 'Search and View',
                                     on_selected=lambda: self.__search_submenu())) \
            .with_entry(Entry.create('4', 'Update beer by id',
                                     on_selected=lambda: self.__update_beer_by_id())) \
            .with_entry(Entry.create('5', 'Delete beer by id',
                                     on_selected=lambda: self.__delete_beer_by_id())) \
            .with_entry(Entry.create('6', 'Brewery operations',
                                     on_selected=lambda: self.__brewery_submenu())) \
            .with_entry(Entry.create('7', 'Sort operations',
                                     on_selected=lambda: self.__sort_submenu())) \
            .with_entry(Entry.create('8', 'Statistics',
                                     on_selected=lambda: self.__statistics_submenu())) \
            .with_entry(Entry.create('0', 'Exit',
                                     on_selected=lambda: print('Bye!'),
                                     is_exit=True)) \
            .build()

    def __search_submenu(self):
        submenu = Menu.Builder(menu.Description('Search and View Operations'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Search beer by ID',
                                     on_selected=lambda: self.__print_beer_by_id())) \
            .with_entry(Entry.create('2', 'Search beer by name',
                                     on_selected=lambda: self.__print_beer_by_name())) \
            .with_entry(Entry.create('0', 'Back to main menu', is_exit=True)) \
            .build()
        submenu.run()

    def __brewery_submenu(self):
        submenu = Menu.Builder(menu.Description('Brewery Operations'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'List all breweries',
                                     on_selected=lambda: self.__print_breweries())) \
            .with_entry(Entry.create('2', 'Filter beers by brewery',
                                     on_selected=lambda: self.__print_beers_by_brewery())) \
            .with_entry(Entry.create('0', 'Back to main menu', is_exit=True)) \
            .build()
        submenu.run()

    def __sort_submenu(self):
        submenu = Menu.Builder(menu.Description('Sort Operations'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Sort by ascending alcohol content',
                                     on_selected=lambda: self.__print_beers_sorted_by_ascending_alcohol_content())) \
            .with_entry(Entry.create('2', 'Sort by descending alcohol content',
                                     on_selected=lambda: self.__print_beers_sorted_by_descending_alcohol_content())) \
            .with_entry(Entry.create('0', 'Back to main menu', is_exit=True)) \
            .build()
        submenu.run()

    def __statistics_submenu(self):
        submenu = Menu.Builder(menu.Description('Statistics'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Total number of beers',
                                     on_selected=lambda: self.__print_number_of_beers())) \
            .with_entry(Entry.create('2', 'Total number of breweries',
                                     on_selected=lambda: self.__print_number_of_breweries())) \
            .with_entry(Entry.create('0', 'Back to main menu', is_exit=True)) \
            .build()
        submenu.run()

    def __run(self) -> None:
        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)
            raise

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __print_number_of_beers(self):
        print(f'Total number of beers {self.__beer_hub.number_of_beers()}')

    def __print_beer_by_id(self):
        def builder(value: str) -> ID:
            validate('value', int(value), min_value=0)
            return ID(int(value))

        _id = self.__read('Beer id', builder)
        beer = self.__beer_hub.get_beer_by_id(_id)

        if beer is None:
            print('Beer with given id does not exist!')
            return

        self.__print_beers_internal([beer])

    def __print_beer_by_name(self):
        def builder(value: str) -> Name:
            return Name(value)

        name = self.__read('Beer name', builder)
        beer = self.__beer_hub.get_beer_by_name(name)

        if beer is None:
            print('Beer with given name does not exist!')
            return

        self.__print_beers_internal([beer])

    def __add_beer(self):
        name = self.__read('Name', Name)
        description = self.__read('Description', Description)
        brewery = self.__read('Brewery', Brewery)
        beer_type = self.__read('Beer Type', BeerType)
        alcohol_content = self.__read('Alcohol Content', AlcoholContent.of)

        beer = Beer.of(name, description, brewery, beer_type, alcohol_content)

        self.__beer_hub.add_beer(beer)

    def __update_beer_by_id(self):
        def builder(value: str) -> Optional[Beer]:
            if value == '-1':
                return None

            _beer_id = ID(int(value))
            curr_beer = self.__beer_hub.get_beer_by_id(_beer_id)

            if curr_beer is None:
                raise ValueError('Beer with given id does not exist!')

            return curr_beer

        current_beer: Optional[Beer] = self.__read('Enter id of beer that should get updated (-1 to cancel)', builder)

        if current_beer is None:
            print('Cancelled!')
            return

        name = self.__read(f'Name (currently "{current_beer.name}")', Name)
        desc_str = str(current_beer.description)
        description = self.__read(f'Description (currently "{desc_str[:10]}'
                                  + ('...' if len(desc_str) > 10 else '') + '")', Description)
        brewery = self.__read(f'Brewery (currently "{current_beer.brewery}")', Brewery)
        beer_type = self.__read(f'Beer Type (currently "{current_beer.beer_type}")', BeerType)
        alcohol_content = self.__read(f'Alcohol Content (currently "{current_beer.alcohol_content}")', AlcoholContent.of)

        beer = Beer.of(name, description, brewery, beer_type, alcohol_content)

        self.__beer_hub.update_beer_by_id(current_beer.id, beer)

    def __delete_beer_by_id(self):
        def builder(value: str) -> Optional[ID]:
            if value == '-1':
                return None

            _beer_id = ID(int(value))
            beer = self.__beer_hub.get_beer_by_id(_beer_id)

            if beer is None:
                raise ValueError(f'Beer with id {_beer_id} does not exist!')

            return _beer_id

        _id: Optional[ID] = self.__read('Enter id of beer that should get deleted (-1 to cancel)', builder)

        if _id is None:
            print('Cancelled!')
            return

        self.__beer_hub.delete_beer_by_id(_id)

    def __print_number_of_breweries(self):
        print(f'Total number of breweries {self.__beer_hub.number_of_breweries()}')

    def __print_beers_by_brewery(self):
        brewery = self.__read('Enter brewery name', Brewery)
        beers = self.__beer_hub.get_beers_by_brewery(brewery)
        self.__print_beers_internal(beers)

    def __print_beers_sorted_by_ascending_alcohol_content(self):
        beers = self.__beer_hub.get_beers_by_ascending_alcohol_content()
        self.__print_beers_internal(beers)

    def __print_beers_sorted_by_descending_alcohol_content(self):
        beers = self.__beer_hub.get_beers_by_descending_alcohol_content()
        self.__print_beers_internal(beers)

    @staticmethod
    def __print_beers_internal(beers: list[Beer]) -> None:
        if not beers:
            print("No beers to display")
            return

        def print_sep():
            print('-' * 125)

        print_sep()
        fmt = '%3s %-20s %-20s %-20s %-35s %-20s'
        print(fmt % ('#', 'NAME', 'DESCRIPTION', 'BREWERY', 'BEER_TYPE', 'ALCOHOL_CONTENT'))
        print_sep()
        for beer in beers:
            print(fmt % (beer.id, beer.name, beer.description, beer.brewery, beer.beer_type, beer.alcohol_content))
        print_sep()

    @staticmethod
    def __print_breweries_internal(breweries: list[Brewery]) -> None:
        if not breweries:
            print("No breweries to display")
            return

        def print_sep():
            print('-' * 100)

        print_sep()
        fmt = '%3s %-20s'
        print(fmt % ('#', 'BREWERY'))
        print_sep()
        for index, brewery in enumerate(breweries):
            print(fmt % (index + 1, brewery))
        print_sep()

    def __print_beers(self):
        beers = self.__beer_hub.get_beers()
        self.__print_beers_internal(beers)

    def __print_breweries(self):
        breweries = self.__beer_hub.get_breweries()
        self.__print_breweries_internal(breweries)
