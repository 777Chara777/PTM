from .NetworkManager import NetworkManager
from .AudioEngine import AudioManager
from .StreamEngine import StreamEngine

class Controller:
    def __init__(self, app):
        self.app = app
        self.network = NetworkManager(self)
        self.audio = AudioManager()
        self.stream = StreamEngine()
        
        self.peers = {}
        self.groups = {}
        # self.peers = {"I": "0.0.0.0"}
        # self.groups = {"#general": ["I"]}
        self.current_target = "#general"

    async def send_message(self, text):
        target_ips: list[str] = self.get_current_ips() # type: ignore
        body = {"sender": "You", "channel": self.current_target, "message": text}
        data = {"type": "message", "body": body}
        await self.network.broadcast(target_ips, data)
        self.app.post_to_chat(f"[You -> {self.current_target}]: {text}")

    def on_message_received(self, msg):
        display_text = f"[{msg['sender']} @ {msg['channel']}]: {msg['message']}"
        self.app.post_to_chat(display_text)

    def toggle_voice(self):
        if not self.audio.stream:
            # self.get_current_ips()
            self.audio.start()
            return True
        self.audio.close()
        return False

    def get_current_ips(self):
        if self.current_target.startswith("#"):
            return [self.peers[name] for name in self.groups.get(self.current_target, []) if name in self.peers]
        return [self.peers.get(self.current_target)]
    