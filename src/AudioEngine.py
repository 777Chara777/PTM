import pyaudio
import numpy as np

class AudioManager:
    def __init__(self, rate=48000, chunk=1920, channels=1, format=pyaudio.paInt16):
        self.rate = rate
        self.chunk = chunk
        self.channels = channels
        self.format = format
        
        self.p = pyaudio.PyAudio()
        self.stream = None
        
        self.input_device_index = None
        self.output_device_index = None

    def list_devices(self):
        """Returns a list of all available audio devices."""
        try:
            default_input = self.p.get_default_input_device_info()['index']
        except IOError:
            default_input = -1

        devices = []
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            devices.append({
                'index': i,
                'name': dev['name'],
                'is_default': i == default_input
            })
        return devices

    def print_devices(self):
        """Prints the list of devices to the console."""
        print("Available devices:")
        for dev in self.list_devices():
            star = "*" if dev['is_default'] else " "
            print(f"{star} [{dev['index']}] {dev['name']}")

    def select_device(self, input_query=None, output_query=None):
        """
        Selects a device by its index (int) or by a part of its name (str).
        Example: 
            am.select_device(input_query="Microphone")
            am.select_device(output_query=3)
        """
        devices = self.list_devices()
        
        if input_query is not None:
            self.input_device_index = self._find_device(input_query, devices, "input")
            
        if output_query is not None:
            self.output_device_index = self._find_device(output_query, devices, "output")

    def _find_device(self, query, devices, dev_type):
        """Internal helper to find a device by ID or name."""
        if isinstance(query, int):
            if any(d['index'] == query for d in devices):
                return query
            raise ValueError(f"{dev_type.capitalize()} device with index {query} not found.")
        
        if isinstance(query, str):
            for d in devices:
                if query.lower() in d['name'].lower():
                    print(f"Successfully selected {dev_type} device: [{d['index']}] {d['name']}")
                    return d['index']
            raise ValueError(f"{dev_type.capitalize()} device with name containing '{query}' not found.")
        
        raise TypeError("Query must be of type int (index) or str (part of the name).")

    def start(self):
        """Opens a duplex (input/output) audio stream based on the selected settings."""
        if self.input_device_index is None:
            try:
                self.input_device_index = self.p.get_default_input_device_info()['index']
            except IOError:
                raise RuntimeError("Default input device not found.")
            
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            output=True,
            frames_per_buffer=self.chunk,
            input_device_index=self.input_device_index, # pyright: ignore[reportArgumentType]
            output_device_index=self.output_device_index
        )

    def read(self) -> np.ndarray:
        """Safely reads a chunk and returns a numpy array (float32)."""
        if not self.stream or not self.stream.is_active():
            raise RuntimeError("Stream is not running. Call start() method first.")
        raw_input = self.stream.read(self.chunk, exception_on_overflow=False)
        return np.frombuffer(raw_input, dtype=np.int16).astype(np.float32)

    def write(self, data: np.ndarray):
        """Accepts a numpy array (float32), protects against clipping, and plays it."""
        if not self.stream or not self.stream.is_active():
            raise RuntimeError("Stream is not running. Call start() method first.")
        clipped_data = np.clip(data, -32768, 32767)
        raw_output = clipped_data.astype(np.int16).tobytes()
        self.stream.write(raw_output)

    def close(self):
        """Stops the stream and releases PyAudio resources."""
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except Exception:
                pass
        if self.p:
            self.p.terminate()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
