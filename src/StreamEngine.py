import subprocess

from config import FFMPEG, FFPLAY

class StreamEngine:
    def __init__(self):
        self.proc = None

    def start_sharing(self, ip):
        self.stop()
        cmd = [
            FFMPEG, "-f", "gdigrab", "-framerate", "30", "-i", "desktop",
            "-c:v", "libx264", "-preset", "ultrafast", "-tune", "zerolatency",
            "-f", "mpegts", f"udp://{ip}:5006"
        ]
        self.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def watch_friend(self, port=5006):
        # Preview Video
        subprocess.Popen([FFPLAY, "-fflags", "nobuffer", "-flags", "low_delay", f"udp://0.0.0.0:{port}"])

    def stop(self):
        if self.proc:
            self.proc.terminate()
            self.proc = None