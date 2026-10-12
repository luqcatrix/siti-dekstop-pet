import json
import asyncio
import websockets
from PyQt6.QtCore import QThread, pyqtSignal

class ScrollTracker(QThread):
    # Sinyal membawa 3 parameter: action (str), total_tabs (int), active_tab_index (int)
    trigger_signal = pyqtSignal(str, int, int)

    def __init__(self, port=8765):
        super().__init__()
        self.port = port

    async def handler(self, websocket):
        print("🔗 [Siti] Mata-mata browser berhasil terhubung!")
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    action = data.get("action", "")
                    
                    # Dukung pembacaan key camelCase maupun snake_case
                    total_tabs = data.get("totalTabs", data.get("total_tabs", 1))
                    active_tab_index = data.get("activeTabIndex", data.get("active_tab_index", 0))

                    print(f"📩 [Siti] Laporan browser: Action={action} | Total Tab={total_tabs} | Index Tab={active_tab_index}")
                    self.trigger_signal.emit(action, total_tabs, active_tab_index)

                except json.JSONDecodeError:
                    action = str(message)
                    print(f"📩 [Siti] Laporan teks mentah diterima: {action}")
                    self.trigger_signal.emit(action, 1, 0)

        except websockets.exceptions.ConnectionClosed:
            print("🔌 [Siti] Ekstensi terputus.")
        except Exception as e:
            print(f"⚠️ [Siti] Error WebSocket: {e}")

    async def start_server(self):
        async with websockets.serve(self.handler, "localhost", self.port):
            print(f"🚀 [Siti] WebSocket Server berjalan di ws://localhost:{self.port}")
            await asyncio.Future()  # Biarkan server tetap standby

    def run(self):
        # Buat event loop terpisah untuk thread ini agar aman di lingkungan GUI PyQt
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start_server())