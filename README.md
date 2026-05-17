# PTM (Peer-to-Peer Terminal Messenger)

PTM is a lightweight, high-performance terminal-based communication platform designed for privacy, speed, and efficiency. Built with Python and powered by the Textual TUI framework, it provides a Discord-like experience directly in your terminal, leveraging true P2P architecture.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Framework](https://img.shields.io/badge/UI-Textual-green.svg)

## 🚀 Features

-   **True P2P Architecture:** No central servers. Communication happens directly between peers.
-   **Rich TUI:** A modern, responsive Terminal User Interface with support for themes and intuitive navigation.
-   **Voice & Video:** Integrated high-quality audio and video streaming using **FFmpeg** and **FFplay**.
-   **Low Latency:** Uses **UDP** for media streaming to ensure real-time performance.
-   **Secure Messaging:** Reliable text delivery via **TCP**.
-   **Group Channels:** Support for multiple rooms and direct messaging.
-   **Resource Efficient:** Extremely low RAM and CPU footprint compared to Electron-based apps.

## 🛠 Tech Stack

-   **Frontend:** [Textual](https://github.com/Textualize/textual) (TUI Framework)
-   **Backend:** Asyncio (Asynchronous Networking)
-   **Media Engine:** [FFmpeg](https://ffmpeg.org/) (Real-time encoding and streaming)
-   **Protocol:** Custom hybrid TCP (Signaling/Text) & UDP (Media)

## 📋 Prerequisites

Before running PTM, ensure you have the following installed:

1.  **Python 3.10+**
2.  **Port Forwarding / VPN:** As a P2P application, peers must be able to reach each other's IP addresses on ports `5005-5007`.

## 📥 Installation

1. Clone the repository:

```bash
git clone https://github.com/777Chara777/PTM.git
cd PTM
```

2. Install dependencies:

```bash
uv sync
```

## 🎮 Usage

Run the application using:

```bash
uv run main.py
```

### Keybindings

* `V`: Toggle Voice Chat
* `S`: Open Settings (Microphone/Themes)
* `Q`: Quit Application

## ⚙️ Configuration

<!--  -->

## 🛡 Privacy

Since PTM is peer-to-peer, your data never touches a third-party server. All text and media streams are sent directly to the recipient.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.