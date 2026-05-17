from textual.app import ComposeResult
from textual.widgets import Static, Input, Log, ListItem, ListView, Label
from textual.containers import Horizontal, Vertical

class MainInterface(Static):
    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="side-bar"):
                yield Label("Groups", classes="sidebar-title")
                yield ListView(
                    ListItem(Static("#general"), id="group-general"),
                    ListItem(Static("#dev"), id="group-dev"),
                    id="list-groups"
                )
                yield Label("Friends", classes="sidebar-title")
                yield ListView(
                    ListItem(Static("Я")),
                    id="list-friends"
                )
                yield Static("● Voice: ВЫКЛ", id="status-mic")
            
            with Vertical(id="chat-area"):
                yield Log(id="chat-log")
                yield Input(placeholder="Send message...", id="chat-input")