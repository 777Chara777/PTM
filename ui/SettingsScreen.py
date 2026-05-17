from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Select, RadioSet, RadioButton
from textual.containers import Horizontal, Vertical

class SettingsScreen(ModalScreen):
    """Окно настроек звука и темы"""
    CSS = """
    SettingsScreen { 
        align: center middle; 
    }
    
    #settings-container {
        width: 60;
        height: auto;
        min-height: 25;
        max-height: 45;
        background: #16161e;
        border: thick #3b4261;
        padding: 1 2;
    }

    #title {
        text-align: center;
        text-style: bold;
        color: #bb9af7;
        margin-bottom: 1;
    }

    .setting-label { 
        margin-top: 1; 
        text-style: bold; 
        color: #7aa2f7; 
    }

    #theme-toggle {
        margin: 1 0;
        border: none;
        background: transparent;
    }

    #buttons {
        margin-top: 2;
        height: 3;
        content-align: center middle;
    }

    #buttons Button {
        margin: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        devices = self.app.controller.audio.get_devices() # type: ignore
        current_mic = self.app.controller.audio.current_device # type: ignore
        
        valid_values = [v for k, v in devices]
        if current_mic not in valid_values:
            current_mic = valid_values[0] if valid_values else None
        
        with Vertical(id="settings-container"):
            yield Label("⚙️ Settings", id="title")
            
            yield Label("🎙️ Select mic:", classes="setting-label")
            yield Select(
                devices, 
                value=current_mic, 
                id="mic-select",
                allow_blank=False
            )
            
            yield Label("🎨 Thema:", classes="setting-label")
            with RadioSet(id="theme-toggle"):
                yield RadioButton("Dark (Tokyo Night)", value=True, id="dark")
                yield RadioButton("Light (Classic)", id="light")

            with Horizontal(id="buttons"):
                yield Button("Save", variant="success", id="save")
                yield Button("Cancle", variant="error", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save":
            mic = self.query_one("#mic-select", Select).value
            self.app.controller.audio.current_device = mic # type: ignore
            self.app.pop_screen()
        elif event.button.id == "cancel":
            self.app.pop_screen()