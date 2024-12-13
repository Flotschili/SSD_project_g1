import csv
import sys
from pathlib import Path
from typing import Any, Tuple, Callable, Optional

from valid8 import validate, ValidationError

from beer_hub.domain import Beer, Name, Brewery, BeerType, AlcoholContent, ID
from beer_hub.logic import InMemoryBeerHub, ping_backend
from beer_hub.menu import Menu, Description, Entry


class App:
    __filename = Path(__file__).parent.parent / 'default.csv'
    __delimiter = '\t'

    def __init__(self):
        self.__menu = Menu.Builder(Description('BeerHub'), auto_select=lambda: self.__after_action()) \
            .with_entry(Entry.create('1', 'List all beers', on_selected=lambda: self.__print_beers())) \
            .with_entry(Entry.create('2', 'Add beer', on_selected=lambda: self.__add_beer())) \
            .with_entry(Entry.create('3', 'Search and View', on_selected=lambda: self.__search_submenu())) \
            .with_entry(Entry.create('4', 'Update beer', on_selected=lambda: self.__update_submenu())) \
            .with_entry(Entry.create('5', 'Delete beer', on_selected=lambda: self.__delete_submenu())) \
            .with_entry(Entry.create('6', 'Brewery operations', on_selected=lambda: self.__brewery_submenu())) \
            .with_entry(Entry.create('7', 'Sort operations', on_selected=lambda: self.__sort_submenu())) \
            .with_entry(Entry.create('8', 'Statistics', on_selected=lambda: self.__statistics_submenu())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()
        self.__beer_hub = InMemoryBeerHub()

    def __search_submenu(self):
        submenu = Menu.Builder(Description('Search & View Operations'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Search beer by ID', on_selected=lambda: self.__print_beer_by_id())) \
            .with_entry(Entry.create('2', 'Search beer by name', on_selected=lambda: self.__print_beer_by_name())) \
            .with_entry(Entry.create('0', 'Back to main menu', is_exit=True)) \
            .build()
        submenu.run()

    def __update_submenu(self):
        submenu = Menu.Builder(Description('Update Operations'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Update beer by ID', on_selected=lambda: self.__update_beer_by_id())) \
            .with_entry(Entry.create('2', 'Update beer by name', on_selected=lambda: self.__update_beer_by_name())) \
            .with_entry(Entry.create('0', 'Back to main menu', is_exit=True)) \
            .build()
        submenu.run()

    def __delete_submenu(self):
        submenu = Menu.Builder(Description('Delete Operations'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Delete beer by ID', on_selected=lambda: self.__delete_beer_by_id())) \
            .with_entry(Entry.create('2', 'Delete beer by name', on_selected=lambda: self.__delete_beer_by_name())) \
            .with_entry(Entry.create('0', 'Back to main menu', is_exit=True)) \
            .build()
        submenu.run()

    def __brewery_submenu(self):
        submenu = Menu.Builder(Description('Brewery Operations'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'List all breweries', on_selected=lambda: self.__print_breweries())) \
            .with_entry(
            Entry.create('2', 'Filter beers by brewery', on_selected=lambda: self.__print_beers_by_brewery())) \
            .with_entry(Entry.create('0', 'Back to main menu', is_exit=True)) \
            .build()
        submenu.run()

    def __sort_submenu(self):
        submenu = Menu.Builder(Description('Sort Operations'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Sort by ascending alcohol content',
                                     on_selected=lambda: self.__print_beers_sorted_by_ascending_alcohol_content())) \
            .with_entry(Entry.create('2', 'Sort by descending alcohol content',
                                     on_selected=lambda: self.__print_beers_sorted_by_descending_alcohol_content())) \
            .with_entry(Entry.create('0', 'Back to main menu', is_exit=True)) \
            .build()
        submenu.run()

    def __statistics_submenu(self):
        submenu = Menu.Builder(Description('Statistics'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Total number of beers', on_selected=lambda: self.__print_number_of_beers())) \
            .with_entry(Entry.create('2', 'Total number of breweries',
                                     on_selected=lambda: self.__print_number_of_breweries())) \
            .with_entry(Entry.create('0', 'Back to main menu', is_exit=True)) \
            .build()
        submenu.run()

    def __run(self) -> None:
        try:
            self.__load_file()
        except ValueError as e:
            print(e)
            print('Continuing with an empty dataset...')

        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)

    def __load_file(self) -> None:
        if not Path(self.__filename).exists():
            return

        with open(self.__filename) as file:
            reader = csv.reader(file, delimiter=self.__delimiter)
            for row in reader:
                validate('row length', row, length=5)
                # name = Name(row[0])
                # description = Name(row[0])
                # brewery = Brewery(row[0])
                # beer_type = BeerType(row[0])
                # alcohol_content = AlcoholContent(row[0])
                beer = Beer.of(*row)
                self.__beer_hub.add_beer(beer)

    def __save_file(self) -> None:
        with open(self.__filename, 'w') as file:
            writer = csv.writer(file, delimiter=self.__delimiter, lineterminator='\n')
            for index in range(self.__beer_hub.number_of_beers()):
                beer = self.__beer_hub.get_beer_by_id(index)
                writer.writerow([beer.name, beer.brewery, beer.beer_type, beer.alcohol_content])

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
        print(self.__beer_hub.number_of_beers())

    def __print_beer_by_id(self):
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0)
            return int(value)

        id = self.__read('Beer id', builder)
        beer = self.__beer_hub.get_beer_by_id(id)

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
        self.__save_file()

    def __update_beer_by_id(self):
        def builder(value: str) -> Optional[Beer]:
            if value == '-1':
                return None

            i = ID(int(value))
            curr_beer = self.__beer_hub.get_beer_by_id(i)

            if curr_beer is None:
                raise ValueError('Beer with given id does not exist!')

            return curr_beer

        current_beer: Optional[Beer] = self.__read('Enter id of beer that should get updated (-1 to cancel)', builder)

        if current_beer is None:
            print('Cancelled!')
            return

        name = self.__read(f'Name (currently {current_beer.name})', Name)
        description = self.__read(f'Description (currently {current_beer.description[:10]} '
                                  + '...' if len(current_beer.description) > 10 else '', Description)
        brewery = self.__read(f'Brewery (currently {current_beer.brewery})', Brewery)
        beer_type = self.__read(f'Beer Type (currently {current_beer.beer_type})', BeerType)
        alcohol_content = self.__read(f'Alcohol Content (currently {current_beer.alcohol_content})', AlcoholContent.of)

        beer = Beer.of(name, description, brewery, beer_type, alcohol_content)

        self.__beer_hub.update_beer_by_id(current_beer.id, beer)

    def __update_beer_by_name(self):
        def builder(value: str) -> Optional[Beer]:
            if value == '-1':
                return None

            _ = Name(value)
            curr_beer = self.__beer_hub.get_beer_by_name(value)

            if curr_beer is None:
                raise ValueError('Beer with given name does not exist!')

            return curr_beer

        current_beer: Optional[Beer] = self.__read('Enter name of beer that should get updated (-1 to cancel)', builder)

        if current_beer is None:
            print('Cancelled!')
            return

        name = self.__read(f'Name (currently {current_beer.name})', Name)
        description = self.__read(f'Description (currently {current_beer.description[:10]} '
                                  + '...' if len(current_beer.description) > 10 else '', Description)
        brewery = self.__read(f'Brewery (currently {current_beer.brewery})', Brewery)
        beer_type = self.__read(f'Beer Type (currently {current_beer.beer_type})', BeerType)
        alcohol_content = self.__read(f'Alcohol Content (currently {current_beer.alcohol_content})', AlcoholContent.of)

        beer = Beer.of(name, description, brewery, beer_type, alcohol_content)

        self.__beer_hub.update_beer_by_name(name, beer)

    def __delete_beer_by_id(self):
        def builder(value: str) -> Optional[ID]:
            if value == '-1':
                return None

            i = ID(int(value))
            beer = self.__beer_hub.get_beer_by_id(i)

            if beer is None:
                raise ValueError('Beer with given id does not exist!')

            return i

        id: Optional[ID] = self.__read('Enter id of beer that should get deleted (-1 to cancel)', builder)

        if id is None:
            print('Cancelled!')
            return

        self.__beer_hub.delete_beer_by_id(id)

    def __delete_beer_by_name(self) -> None:
        def builder(value: str) -> Optional[Name]:
            if value == '-1':
                return None

            _ = Name(value)
            beer = self.__beer_hub.get_beer_by_name(value)

            if beer is None:
                raise ValueError('Beer with given name does not exist!')

            return _

        name: Optional[Name] = self.__read('Enter name of beer that should get deleted (-1 to cancel)', builder)

        if name is None:
            print('Cancelled!')
            return

        self.__beer_hub.delete_beer_by_name(name)

    def __print_number_of_breweries(self):
        print(self.__beer_hub.number_of_breweries())

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

    def __ping_backend(self):
        ping_backend()

    @staticmethod
    def __print_beers_internal(beers: list[Beer]) -> None:
        if not beers:
            print("No beers to display")
            return

        def print_sep():
            print('-' * 100)

        print_sep()
        fmt = '%3s %-20s %-20s %-20s %-35s %-20s'
        print(fmt % ('#', 'NAME', 'DESCRIPTION', 'BREWERY', 'BEER_TYPE', 'ALCOHOL_CONTENT'))
        print_sep()
        for index, beer in enumerate(beers):
            print(fmt % (index + 1, beer.name, beer.description, beer.brewery, beer.beer_type, beer.alcohol_content))
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

    def __after_action(self):
        pass
