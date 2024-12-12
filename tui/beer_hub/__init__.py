import typeguard
from typeguard import CollectionCheckStrategy, install_import_hook

typeguard.config.collection_check_strategy = CollectionCheckStrategy.ALL_ITEMS
install_import_hook('music_archive')
