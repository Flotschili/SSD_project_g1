import re
from dataclasses import dataclass, InitVar, field
from typing import Any

from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@dataclass(frozen=True, order=True)
class Author:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern(r'[0-9A-Za-z ]*'))

    def __str__(self):
        return self.value


@dataclass(frozen=True, order=True)
class Title:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern(r'[0-9A-Za-z ]*'))

    def __str__(self):
        return self.value


@dataclass(frozen=True, order=True)
class Genre:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern(r'[0-9A-Za-z ]*'))

    def __str__(self):
        return self.value


@dataclass(frozen=True, order=True)
class Duration:
    value_in_seconds: int
    create_key: InitVar[Any] = field(default=None)

    __create_key = object()
    __max_value = 36000
    __parse_pattern = re.compile(r'(?P<minutes>\d{1,3}):(?P<seconds>\d{2})')

    def __post_init__(self, create_key):
        validate('create_key', create_key, equals=self.__create_key)
        validate_dataclass(self)
        validate('value_in_seconds', self.value_in_seconds, min_value=0, max_value=self.__max_value)

    def __str__(self):
        return f'{self.minutes}:{self.seconds:02}'

    @staticmethod
    def create(minutes: int = 0, seconds: int = 0) -> 'Duration':
        validate('minutes', minutes, min_value=0, max_value=Duration.__max_value // 60)
        validate('seconds', seconds, min_value=0, max_value=59)
        return Duration(minutes * 60 + seconds, Duration.__create_key)

    @staticmethod
    def parse(value: str) -> 'Duration':
        m = Duration.__parse_pattern.fullmatch(value)
        validate('value', m)
        minutes = m.group('minutes')
        seconds = m.group('seconds')
        return Duration.create(int(minutes), int(seconds))

    @property
    def minutes(self) -> int:
        return self.value_in_seconds // 60

    @property
    def seconds(self) -> int:
        return self.value_in_seconds % 60

    def add(self, other: 'Duration') -> 'Duration':
        return Duration(self.value_in_seconds + other.value_in_seconds, self.__create_key)


@dataclass(frozen=True, order=True)
class Song:
    author: Author
    title: Title
    genre: Genre
    duration: Duration

    @staticmethod
    def of(author: str, title: str, genre: str, duration: str) -> 'Song':
        return Song(
            Author(author),
            Title(title),
            Genre(genre),
            Duration.parse(duration),
        )


@dataclass(frozen=True, order=True)
class MusicArchive:
    __songs: list[Song] = field(default_factory=list, init=False, repr=False)

    def number_of_songs(self) -> int:
        return len(self.__songs)

    def song_at_index(self, index) -> Song:
        validate('index', index, min_value=0, max_value=len(self.__songs) - 1)
        return self.__songs[index]

    def add_song(self, song: Song) -> None:
        self.__songs.append(song)

    def remove_song(self, index: int) -> None:
        self.__songs.pop(index)

    def list_of_authors(self) -> list[Author]:
        return list({song.author for song in self.__songs})

    def songs_of_author(self, author: Author) -> list[Song]:
        return [song for song in self.__songs if song.author == author]

    def sort_by_ascending_duration(self) -> None:
        self.__songs.sort(key=lambda song: song.duration)
