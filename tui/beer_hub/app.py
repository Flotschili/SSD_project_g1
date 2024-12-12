import csv
import sys
from pathlib import Path
from typing import Any, Tuple, Callable

from valid8 import validate, ValidationError

from beer_hub.domain import BeerHub, Beer, Name, Brewery, BeerType, AlcoholContent
from beer_hub.menu import Menu, Description, Entry


class App:
    __filename = Path(__file__).parent.parent / 'default.csv'
    __delimiter = '\t'

    def __init__(self):
        self.__menu = Menu.Builder(Description('BeerHub'), auto_select=lambda: self.__after_action())\
            .with_entry(Entry.create('1', 'List beers', on_selected=lambda: self.__print_beers()))\
            .with_entry(Entry.create('2', 'Add beer', on_selected=lambda: self.__add_beer()))\
            .with_entry(Entry.create('3', 'Remove beer', on_selected=lambda: self.__remove_beer()))\
            .with_entry(Entry.create('4', 'List breweries', on_selected=lambda: self.__list_breweries()))\
            .with_entry(Entry.create('5', 'Filter by breweries', on_selected=lambda: self.__filter_by_breweries()))\
            .with_entry(Entry.create('6', 'Sort by ascending alcohol content', on_selected=lambda: self.__sort_by_ascending_alcohol_content()))\
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True))\
            .build()
        self.__beer_hub = BeerHub()

    def __run(self) -> None:
        try:
            self.__load()
        except ValueError as e:
            print(e)
            print('Continuing with an empty dataset...')

        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)

    def __load(self) -> None:
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

    def __save(self) -> None:
        with open(self.__filename, 'w') as file:
            writer = csv.writer(file, delimiter=self.__delimiter, lineterminator='\n')
            for index in range(self.__beer_hub.number_of_beers()):
                beer = self.__beer_hub.beer_at_index(index)
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

    def __add_beer(self):
        name = self.__read('Name', Name)
        description = self.__read('Description', Description)
        brewery = self.__read('Brewery', Brewery)
        beer_type = self.__read('Beer Type', BeerType)
        alcohol_content = self.__read('Alcohol Content', AlcoholContent.of)
        beer = Beer(name, description, brewery, beer_type, alcohol_content)
        self.__beer_hub.add_beer(beer)
        self.__save()

    def __remove_beer(self):
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__beer_hub.number_of_beers())
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled!')
            return
        self.__beer_hub.remove_beer(index - 1)
        self.__save()

    def __list_breweries(self):
        pass #TODO

    def __filter_by_breweries(self):
        pass #TODO

    def __sort_by_ascending_alcohol_content(self):
        pass #TODO

    @staticmethod
    def __print_beers_internal(beers):
        def print_sep():
            print('-' * 100)

        print_sep()
        fmt = '%3s %-20s %-20s %-20s %-35s %-20s'
        print(fmt % ('#', 'NAME', 'DESCRIPTION', 'BREWERY', 'BEER_TYPE', 'ALCOHOL_CONTENT'))
        print_sep()
        for index, beer in enumerate(beers):
            print(fmt % (index + 1, beer.name, beer.description, beer.brewery, beer.beer_type, beer.alcohol_content))
        print_sep()

    def __print_beers(self):
        beer = [self.__beer_hub.beer_at_index(index) for index in range(self.__beer_hub.number_of_beers())]
        self.__print_beers_internal(beer)

    def __after_action(self):
        pass
