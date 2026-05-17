from textual.widgets import Log
from textual.app import App

from src.Controller import Controller

from ui.SettingsScreen import SettingsScreen
from ui.MainScreen import MainInterface


class RadCord(App):
    CSS = """
    Screen { background: #0d0f14; }
    #side-bar { width: 25; border-right: solid #1f2335; background: #0d0f14; }
    .sidebar-title { padding: 1; color: #565f89; text-style: bold; }
    #chat-area { width: 1fr; }
    Log { background: #0d0f14; color: #a9b1d6; border: none; }
    Input { dock: bottom; background: #1a1b26; border: none; margin: 1; }
    #status-mic { height: 1; color: #565f89; margin-left: 2; }
    ListItem { padding: 0 1; }
    ListItem.-selected { background: #1a1b26; color: #7aa2f7; }
    """

    BINDINGS = [
        ("v", "toggle_voice", "Voice"),
        ("s", "open_settings", "Settings"),
        ("q", "quit", "Exit"),
    ]

    def on_mount(self) -> None:
        self.controller = Controller(self)
        self.mount(MainInterface())
        # start P2P server
        self.run_worker(self.controller.network.start_server())

    def post_to_chat(self, text):
        self.query_one("#chat-log", Log).write_line(text)

    async def on_input_submitted(self, event):
        if event.value:
            await self.controller.send_message(event.value)
            event.input.value = ""

    def on_list_view_selected(self, event):
        """change chanel"""
        new_target = str(event.item.children[0].content)
        self.controller.current_target = new_target
        self.post_to_chat(f"[System] move to {new_target}")

    def action_toggle_voice(self):
        active = self.controller.toggle_voice()
        indicator = self.query_one("#status-mic")
        if active:
            indicator.update("● Voice: on") # type: ignore
            indicator.styles.color = "#7aa2f7"
        else:
            indicator.update("● Voice: off") # type: ignore
            indicator.styles.color = "#565f89"
    
    def action_open_settings(self) -> None:
        self.push_screen(SettingsScreen())

if __name__ == "__main__":
    RadCord().run()