import asyncio
import websockets
from PyQt6.QtCore import QThread, pyqtSignal

class ScrollTracker(QThread):
    # Sinyal khusus untuk memicu serangan Siti
    trigger_signal = pyqtSignal()
    # Sinyal BARU untuk memicu mode waspada (meow)
    alert_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

    async def handler(self, websocket):
        print("[Siti] Mata-mata browser berhasil terhubung!")
        
        async for message in websocket:
            if message == "ATTACK":
                print("[Siti] Laporan doomscrolling diterima! Menyerang...")
                self.trigger_signal.emit()
            elif message == "ALERT":
                print("[Siti] User masuk ke sarang doomscrolling! Waspada...")
                self.alert_signal.emit()

    async def start_server(self):
        async with websockets.serve(self.handler, "localhost", 8765):
            await asyncio.Future()  

    def run(self):
        asyncio.run(self.start_server())