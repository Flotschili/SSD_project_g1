from beer_hub.app import App


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
