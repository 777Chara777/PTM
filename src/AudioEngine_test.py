import subprocess
import os

from config import FFMPEG, FFPLAY

class AudioEngine:
    def __init__(self):
        self.transmit_procs = [] # Список процессов для группового звонка
        self.listen_proc = None
        self.current_device = "default" # Название микрофона по умолчанию

    def get_devices(self):
        """devices list from ffmpeg"""
        # Команда для вывода устройств в Windows
        cmd = [FFMPEG, "-list_devices", "true", "-f", "dshow", "-i", "dummy"]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        
        devices = []
        # Простой парсинг вывода ffmpeg
        for line in result.stderr.split('\n'):
            if "DirectShow audio devices" in line: continue
            if "(audio)" in line:
                name = line.split('"')[1]
                devices.append((name, name))
        return devices if devices else [("Default", "default")]

    def start_voice(self, target_ips):
        self.stop_voice() # На всякий случай чистим старое
        
        # 1. Запускаем прием (один процесс на порт 5005)
        self.listen_proc = subprocess.Popen(
            [FFPLAY, "-nodisp", "-fflags", "nobuffer", "udp://0.0.0.0:5005"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

        # 2. Запускаем передачу каждому участнику
        for ip in target_ips:
            device_arg = f"audio={self.current_device}" if self.current_device != "default" else "audio=Microphone"
            proc = subprocess.Popen(
                [FFMPEG, "-f", "dshow", "-i", device_arg, 
                 "-c:a", "libopus", "-b:a", "32k", "-f", "mpegts", f"udp://{ip}:5005"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            self.transmit_procs.append(proc)

    def stop_voice(self):
        """We kill only those processes that we created ourselves."""
        if self.listen_proc:
            self.listen_proc.terminate()
            self.listen_proc = None
        
        for proc in self.transmit_procs:
            proc.terminate()
        self.transmit_procs.clear()