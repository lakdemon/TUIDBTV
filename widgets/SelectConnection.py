import json

from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import OptionList, Placeholder, Button

from widgets.NewConnection import NewConnection


class SelectConnection(ModalScreen):
    connectionsList = []
    highlighted_index = 0
    can_quit = True

    def __init__(self, _can_quit=True):
        super().__init__()
        self.can_quit=_can_quit

    def compose(self) -> ComposeResult:
        yield Grid(
            OptionList(id="select_connection_list"),
            Placeholder(),
            Button("New Connection", variant="primary", id="new_connection_button"),
            Button.warning("Cancel", id="cancel_select_connection_button", disabled = not self.can_quit),
            Button.success("Connect", id="connect_button", disabled=True),
            id="select_connection_dialog"
        )

    def on_mount(self):
        optionList: OptionList = self.query_one("#select_connection_list")
        with open("connections.json", 'r') as file:
            connections = json.load(file)
            self.connectionsList = connections["connections"]
            for connection in self.connectionsList:
                optionList.add_option(connection["connectionName"])

    def on_button_pressed(self, event):
        if event.button.id == "new_connection_button":
            self.parent.push_screen(NewConnection())
        else:
            selectedConnection: OptionList = self.query_one("#select_connection_list")
            selectedOption = selectedConnection.get_option_at_index(self.highlighted_index).prompt.__str__()
            for connection in self.connectionsList:
                if connection['connectionName'] == selectedOption:
                    self.dismiss(connection)

    def on_option_list_option_highlighted(self, event: OptionList.OptionMessage):
        self.query_one("#connect_button").disabled = False
        self.highlighted_index = event.option_index

    def on_option_list_option_selected(self, event):
        for connection in self.connectionsList:
            if connection['connectionName'] == event.option.prompt.__str__():
                self.dismiss(connection)