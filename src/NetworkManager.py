import asyncio
import json
import typing

if typing.TYPE_CHECKING:
    from src.Controller import Controller

class NetworkManager:
    def __init__(self, controller: "Controller", **kwargs):
        self.controller = controller
        self.tcp_port = kwargs.get("tcp_port") if kwargs.get("tcp_port") else 5007
        self.udp_port = kwargs.get("udp_port") if kwargs.get("udp_port") else 5005 # post to audio/video

    async def start_server(self):
        """Launching the TCP server (messaging) and UDP server (streaming)"""
        tcp_task = asyncio.create_task(self._start_tcp_server())
        udp_task = asyncio.create_task(self._start_udp_receiver())
        await asyncio.gather(tcp_task, udp_task)

    async def _start_tcp_server(self):
        server = await asyncio.start_server(self._handle_tcp_client, '0.0.0.0', self.tcp_port)
        async with server:
            await server.serve_forever()

    async def _handle_tcp_client(self, reader, writer):
        data = await reader.read(4096)
        if data:
            try:
                payload = json.loads(data.decode())
                msg_type = payload.get("type")
                body = payload.get("body")
                
                match msg_type:
                    case "message":
                        self.controller.on_message_received(body)
                    # case "voice_call_request":
                    #     self.controller.on_call_incoming(payload.get("sender"))
                    # case "stream_start":
                    #     self.controller.on_stream_incoming(payload.get("sender"))
                    case "system_notification":
                        self.controller.app.post_to_chat(f"[System]: {body.get('text')}")
               
            except json.JSONDecodeError:
                pass
        writer.close()

    async def _start_udp_receiver(self):
        """
        A UDP server for receiving streaming data. 
        Note: In reality, FFplay opens the UDP port itself. 
        This method is required if we wish to process the data within Python.
        """
        loop = asyncio.get_running_loop()
        pass

    async def send_to_ip(self, ip: str, data: dict):
        """Send TCP Package"""
        try:
            reader, writer = await asyncio.open_connection(ip, self.tcp_port)
            writer.write(json.dumps(data).encode())
            await writer.drain()
            writer.close()
        except Exception as e:
            self.controller.app.post_to_chat(f"[NetworkManager-Error]: Unable to contact {ip}")

    async def broadcast(self, ips: list[str], data: dict):
        tasks = [self.send_to_ip(ip, data) for ip in ips]
        await asyncio.gather(*tasks)