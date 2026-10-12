import sys
from PyQt6.QtWidgets import QApplication
from pet import SitiPet
from tracker import ScrollTracker

def main():
    app = QApplication(sys.argv)

    siti = SitiPet()
    siti.show()

    # Inisialisasi server penerima laporan (tracker)
    tracker = ScrollTracker()
    
    # Handler pemutus arus sinyal dari tracker
    def handle_tracker_signal(action, total_tabs, active_tab_index):
        if action == "ATTACK":
            siti.attack_signal.emit(total_tabs, active_tab_index)
        elif action == "ALERT":
            siti.alert_signal.emit()

    # Hubungkan sinyal utama dari tracker ke handler
    tracker.trigger_signal.connect(handle_tracker_signal)
    
    # Jalankan server di background
    tracker.start()
    
    print("Siti stand-by menunggu laporan dari browser! 😾")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()