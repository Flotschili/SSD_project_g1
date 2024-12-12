# test Author
# test Title
# test Genre
import pytest
from valid8 import ValidationError

from beer_hub.domain import Duration, MusicArchive, Song, Author


def test_duration_is_zero_by_default():
    assert Duration.create() == Duration.create(0, 0)


def test_duration_str_representation():
    assert str(Duration.create(4, 44)) == "4:44"


def test_duration_parse():
    assert Duration.parse("4:44") == Duration.create(4, 44)
    with pytest.raises(ValidationError):
        Duration.parse("4.44")


def test_duration_minutes():
    assert Duration.create(4, 44).minutes == 4


def test_duration_seconds():
    assert Duration.create(4, 44).seconds == 44


def test_duration_add():
    assert Duration.create(4, 44).add(Duration.create(0, 16)) == Duration.create(5)


# test Song

def test_song_factory_method_of():
    assert Song.of('Author', 'Title', 'Genre', '1:11').duration == Duration.create(1, 11)


def test_music_archive_starts_with_empty_list():
    assert MusicArchive().number_of_songs() == 0


def test_music_archive_can_add_song():
    music_archive = MusicArchive()
    assert music_archive.number_of_songs() == 0
    music_archive.add_song(Song.of('Author', 'Title', 'Genre', '1:11'))
    assert music_archive.number_of_songs() == 1


def test_music_archive_can_remove_song():
    music_archive = MusicArchive()
    assert music_archive.number_of_songs() == 0
    music_archive.add_song(Song.of('Author 1', 'Title', 'Genre', '0:11'))
    assert music_archive.number_of_songs() == 1
    music_archive.remove_song(0)
    assert music_archive.number_of_songs() == 0


def test_music_archive_can_access_song():
    song = Song.of('Author', 'Title', 'Genre', '1:11')
    music_archive = MusicArchive()
    music_archive.add_song(song)
    assert music_archive.song_at_index(0) == song


def test_music_archive_can_give_the_list_of_authors():
    music_archive = MusicArchive()
    music_archive.add_song(Song.of('Author 1', 'Title', 'Genre', '0:11'))
    music_archive.add_song(Song.of('Author 2', 'Title', 'Genre', '0:11'))
    music_archive.add_song(Song.of('Author 1', 'Title', 'Genre', '0:11'))
    assert {author.value for author in music_archive.list_of_authors()} == {'Author 1', 'Author 2'}


def test_music_archive_songs_of_author():
    music_archive = MusicArchive()
    music_archive.add_song(Song.of('Author 1', 'Title 1', 'Genre', '0:11'))
    music_archive.add_song(Song.of('Author 2', 'Title 2', 'Genre', '0:11'))
    music_archive.add_song(Song.of('Author 1', 'Title 3', 'Genre', '0:11'))
    assert len(music_archive.songs_of_author(Author('Author 1'))) == 2
    assert len(music_archive.songs_of_author(Author('Author 2'))) == 1


def test_music_archive_order_by_ascending_duration():
    music_archive = MusicArchive()
    songs = [
        Song.of('Author 1', 'Title 1', 'Genre', '1:11'),
        Song.of('Author 2', 'Title 2', 'Genre', '0:11'),
        Song.of('Author 1', 'Title 3', 'Genre', '2:11'),
    ]
    for song in songs:
        music_archive.add_song(song)

    music_archive.sort_by_ascending_duration()
    assert music_archive.song_at_index(0) == songs[1]
    assert music_archive.song_at_index(1) == songs[0]
    assert music_archive.song_at_index(2) == songs[2]
