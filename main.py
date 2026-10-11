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
    
    # Hubungkan sinyal dari tracker ke aksi Siti
    tracker.trigger_signal.connect(siti.attack_signal.emit)
    tracker.alert_signal.connect(siti.alert_signal.emit)  # BARU: Menyambungkan sinyal mode meow
    
    # Jalankan server di background
    tracker.start()
    
    print("Siti stand-by menunggu laporan dari browser! 😾")

    sys.exit(app.exec())

if __name__ == "__main__":
    main()