import pytest
from valid8 import ValidationError
from beer_hub.menu import Description, Key, Entry, Menu


def test_description_valid_creation():
    desc = Description("Valid description")
    assert str(desc) == "Valid description"
    assert desc.value == "Valid description"


def test_description_validation_errors():
    with pytest.raises(ValidationError):
        Description("")  # too short
    with pytest.raises(ValidationError):
        Description("a" * 1001)  # too long
    with pytest.raises(ValidationError):
        Description("Invalid$Description")  # invalid characters


def test_description_comparison():
    assert Description("A") < Description("B")
    assert Description("A") == Description("A")
    assert Description("B") > Description("A")


def test_key_valid_creation():
    key = Key("valid_key")
    assert str(key) == "valid_key"
    assert key.value == "valid_key"


def test_key_validation_errors():
    with pytest.raises(ValidationError):
        Key("")  # too short
    with pytest.raises(ValidationError):
        Key("a" * 11)  # too long
    with pytest.raises(ValidationError):
        Key("invalid key")  # contains space
    with pytest.raises(ValidationError):
        Key("invalid$key")  # invalid characters


def test_key_comparison():
    assert Key("a") < Key("b")
    assert Key("a") == Key("a")
    assert Key("b") > Key("a")


def test_entry_creation():
    def dummy_callback():
        # No need to implement
        pass

    entry = Entry(Key("1"), Description("Test"), dummy_callback, False)
    assert entry.key.value == "1"
    assert entry.description.value == "Test"
    assert not entry.is_exit


def test_entry_create_helper():
    entry = Entry.create("1", "Test")
    assert entry.key.value == "1"
    assert entry.description.value == "Test"
    assert not entry.is_exit


def test_entry_with_exit():
    entry = Entry.create("q", "Quit", is_exit=True)
    assert entry.is_exit


def test_entry_callback():
    callback_called = False

    def test_callback():
        nonlocal callback_called
        callback_called = True

    entry = Entry.create("1", "Test", test_callback)
    entry.on_selected()
    assert callback_called


def test_menu_builder():
    builder = Menu.Builder(Description("Test Menu"))
    menu = (builder
            .with_entry(Entry.create("1", "Option 1"))
            .with_entry(Entry.create("q", "Quit", is_exit=True))
            .build())

    assert menu.description.value == "Test Menu"


def test_menu_builder_requires_exit():
    builder = Menu.Builder(Description("Test Menu"))
    with pytest.raises(ValidationError):
        builder.with_entry(Entry.create("1", "Option 1")).build()


def test_menu_duplicate_keys():
    builder = Menu.Builder(Description("Test Menu"))
    builder.with_entry(Entry.create("1", "Option 1"))

    with pytest.raises(ValidationError):
        builder.with_entry(Entry.create("1", "Option 2"))


# test_menu.py (updated version)

def test_menu_auto_select(monkeypatch):
    auto_select_called = False

    def test_auto_select():
        nonlocal auto_select_called
        auto_select_called = True

    # Simulate user input
    inputs = ["q"]  # immediately quit
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    menu = (Menu.Builder(Description("Test Menu"), test_auto_select)
            .with_entry(Entry.create("q", "Quit", is_exit=True))
            .build())

    menu.run()
    assert auto_select_called

def test_menu_display(monkeypatch, capsys):
    # Simulate user input
    inputs = ["q"]  # immediately quit
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    menu = (Menu.Builder(Description("Test Menu"))
            .with_entry(Entry.create("1", "Option 1"))
            .with_entry(Entry.create("q", "Quit", is_exit=True))
            .build())

    menu.run()

    captured = capsys.readouterr()
    assert "Test Menu" in captured.out
    assert "Option 1" in captured.out
    assert "Quit" in captured.out


def test_menu_interaction(monkeypatch, capsys):
    option1_called = False

    def option1_callback():
        nonlocal option1_called
        option1_called = True

    # Simulate selecting option 1 and then quitting
    inputs = ["1", "q"]
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    menu = (Menu.Builder(Description("Test Menu"))
            .with_entry(Entry.create("1", "Option 1", option1_callback))
            .with_entry(Entry.create("q", "Quit", is_exit=True))
            .build())

    menu.run()

    assert option1_called
    captured = capsys.readouterr()
    assert "Test Menu" in captured.out


def test_menu_invalid_selection(monkeypatch, capsys):
    # Simulate invalid input followed by quit
    inputs = ["invalid", "q"]
    input_iterator = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_iterator))

    menu = (Menu.Builder(Description("Test Menu"))
            .with_entry(Entry.create("q", "Quit", is_exit=True))
            .build())

    menu.run()

    captured = capsys.readouterr()
    assert "Invalid selection" in captured.out


def test_menu_integration(monkeypatch):
    # Track callback execution
    option_selected = False

    def option_callback():
        nonlocal option_selected
        option_selected = True

    # Create menu
    menu = (Menu.Builder(Description("Test Menu"))
            .with_entry(Entry.create("1", "Option 1", option_callback))
            .with_entry(Entry.create("q", "Quit", is_exit=True))
            .build())

    # Simulate user input: select option 1, then quit
    inputs = iter(["1", "q"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Run menu
    menu.run()

    assert option_selected


def test_menu_invalid_input(monkeypatch, capsys):
    menu = (Menu.Builder(Description("Test Menu"))
            .with_entry(Entry.create("q", "Quit", is_exit=True))
            .build())

    # Simulate invalid input followed by quit
    inputs = iter(["invalid", "q"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    menu.run()

    captured = capsys.readouterr()
    assert "Invalid selection" in captured.out
