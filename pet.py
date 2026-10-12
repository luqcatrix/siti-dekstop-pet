import os
import sys
import pyautogui
import pygetwindow as gw
from PyQt6.QtWidgets import QLabel, QWidget, QMenu, QApplication
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QMovie, QPixmap
from config import PET_SIZE, ENLARGED_SIZE, WALK_SPEED, SCRATCH_DELAY, IDLE_TIMEOUT, SHAKE_THRESHOLD

# Fungsi pembantu lokasi path asset untuk PyInstaller
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class SitiPet(QWidget):
    # attack_signal menerima 2 parameter: total_tabs (int), active_tab_index (int)
    attack_signal = pyqtSignal(int, int)
    alert_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.attack_signal.connect(self.attack_tab)
        self.alert_signal.connect(self.trigger_alert)
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(PET_SIZE, PET_SIZE)
        
        self.label = QLabel(self)
        self.label.resize(PET_SIZE, PET_SIZE)
        self.label.setScaledContents(True)
        
        self.current_movie = None
        self.current_filename = ""
        self.state = "MEOW"
        self.pre_drag_state = "MEOW"
        
        # Variabel Orientasi & Posisi Presisi
        # Catatan: Asset default menghadap KANAN. is_flipped=True artinya dicermin menghadap KIRI.
        self.is_flipped = False  
        self.float_x = None
        self.float_y = None
        self.return_x = None
        self.return_y = None
        
        self.drag_pos = None
        self.last_mouse_pos = None
        self.shake_distance = 0
        self.target_x = 0
        self.target_y = 0
        
        # Informasi tab dari ekstensi
        self.current_total_tabs = 1
        self.current_tab_index = 0
        
        self.screen_rect = self.screen().availableGeometry()
        self.home_x = self.screen_rect.width() - PET_SIZE - 50
        self.home_y = self.screen_rect.height() - PET_SIZE - 50
        self.move(self.home_x, self.home_y)
        
        self.movement_timer = QTimer(self)
        self.movement_timer.timeout.connect(self.update_movement)
        self.movement_timer.start(16)
        
        self.idle_timer = QTimer(self)
        self.idle_timer.timeout.connect(self._go_to_sleep_sequence)
        self.idle_timer.setSingleShot(True)
        
        self.set_visual('meow.gif')
        self.reset_idle_timer()

    # ==========================================
    # MANAJER UKURAN & VISUAL (DENGAN FLIP / MIRROR)
    # ==========================================
    def set_size(self, size):
        self.resize(size, size)
        self.label.resize(size, size)

    def set_visual(self, filename, is_png=False, enlarge=False):
        if self.current_filename == filename and not is_png and self.current_movie:
            return

        self.current_filename = filename

        if enlarge:
            self.set_size(ENLARGED_SIZE)
        else:
            self.set_size(PET_SIZE)

        self.label.clear()

        # Lepas koneksi movie lama jika ada
        if self.current_movie:
            try:
                self.current_movie.frameChanged.disconnect()
            except Exception:
                pass
            self.current_movie.stop()
            self.current_movie = None

        if is_png:
            pixmap = QPixmap(resource_path(f"asset/{filename}"))
            if self.is_flipped:
                pixmap = QPixmap.fromImage(pixmap.toImage().mirrored(True, False))
            self.label.setPixmap(pixmap)
        else:
            self.current_movie = QMovie(resource_path(f"asset/{filename}"))
            if not self.current_movie.isValid():
                print(f"⚠️ ERROR VISUAL: File {filename} gagal dimuat!")
            else:
                self.current_movie.frameChanged.connect(self._update_frame)
                self.current_movie.start()

    def _update_frame(self):
        if self.current_movie:
            img = self.current_movie.currentImage()
            if self.is_flipped:
                img = img.mirrored(True, False)
            self.label.setPixmap(QPixmap.fromImage(img))

    def reset_idle_timer(self):
        self.idle_timer.start(IDLE_TIMEOUT)

    # ==========================================
    # INTERAKSI MOUSE (DRAG, SHAKE, & CONTEXT MENU)
    # ==========================================
    def contextMenuEvent(self, event):
        """Menu klik kanan untuk menutup aplikasi secara bersih"""
        menu = QMenu(self)
        exit_action = menu.addAction("Keluar / Exit")
        
        action = menu.exec(event.globalPos())
        if action == exit_action:
            QApplication.quit()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.state not in ['IDLE', 'MEOW', 'DIZZY']:
                return 

            self.idle_timer.stop()
            self.pre_drag_state = self.state if self.state in ['IDLE', 'MEOW'] else 'MEOW'
            self.state = 'DRAGGED'
            
            self.set_visual('pasrah.png', is_png=True, enlarge=False)
            
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.last_mouse_pos = event.globalPosition().toPoint()
            self.shake_distance = 0
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.state == 'DRAGGED':
            current_pos = event.globalPosition().toPoint()
            
            delta = current_pos - self.last_mouse_pos
            self.shake_distance += abs(delta.x()) + abs(delta.y())
            self.last_mouse_pos = current_pos
            
            self.move(current_pos - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.state == 'DRAGGED':
            if self.shake_distance > SHAKE_THRESHOLD:
                self.state = 'DIZZY'
                self.set_visual('pusing.gif', enlarge=False)
                QTimer.singleShot(2500, self.resolve_post_drag)
            else:
                self.resolve_post_drag()
            event.accept()

    def resolve_post_drag(self):
        if self.pre_drag_state == 'IDLE':
            self.state = 'ANGRY'
            self.set_visual('marah.gif', enlarge=False)
            QTimer.singleShot(1500, self._after_angry_drag)
        else:
            self.state = 'MEOW'
            self.is_flipped = False
            self.set_visual('meow.gif', enlarge=False)
            self.reset_idle_timer()

    def _after_angry_drag(self):
        self.state = 'SLEEP_TRANSITION'
        self.set_visual('mau_tidur.gif', enlarge=False)
        QTimer.singleShot(2000, self._start_idle_sleep)

    def _go_to_sleep_sequence(self):
        if self.state == 'MEOW':
            self.state = 'SLEEP_TRANSITION'
            self.set_visual('mau_tidur.gif', enlarge=False)
            QTimer.singleShot(2000, self._start_idle_sleep)

    def _start_idle_sleep(self):
        self.state = 'IDLE'
        self.is_flipped = False
        self.set_visual('tidur.gif', enlarge=False)

    # ==========================================
    # LOGIKA SERANGAN DOOMSCROLL DINAMIS
    # ==========================================
    def trigger_alert(self):
        if self.state in ['IDLE', 'MEOW']:
            self.state = 'MEOW'
            self.set_visual('meow.gif', enlarge=False)
            self.reset_idle_timer()

    def attack_tab(self, total_tabs=1, active_tab_index=0):
        if self.state in ['IDLE', 'MEOW']:
            self.idle_timer.stop()
            self.current_total_tabs = max(1, total_tabs)
            self.current_tab_index = max(0, active_tab_index)
            
            # SIMPAN LOKASI AWAL SEBELUM LOMPAT/MEMBESAR
            self.return_x = float(self.x())
            self.return_y = float(self.y())

            self.state = 'ANGRY'
            self.set_visual('marah.gif', enlarge=True)
            
            offset = (ENLARGED_SIZE - PET_SIZE) // 2
            self.move(self.x() - offset, self.y() - offset)
            
            QTimer.singleShot(1500, self._start_running_up)

    def _start_running_up(self):
        self.state = "RUNNING_UP"
        
        try:
            active_window = gw.getActiveWindow()
            if active_window and not active_window.isMinimized and active_window.width >= 300:
                win_x = active_window.left
                win_y = active_window.top
                
                # TARGET: Area Teks URL (Address Bar)
                url_bar_x = win_x + 380
                url_bar_y = win_y + 80
                
                calc_x = url_bar_x - (ENLARGED_SIZE // 2)
                calc_y = url_bar_y - (ENLARGED_SIZE // 2)
                
                self.target_x = max(0, min(self.screen_rect.width() - ENLARGED_SIZE, calc_x))
                self.target_y = max(0, min(self.screen_rect.height() - ENLARGED_SIZE, calc_y))
            else:
                self.target_x = (self.screen_rect.width() // 2) - (ENLARGED_SIZE // 2)
                self.target_y = 80
        except Exception:
            self.target_x = (self.screen_rect.width() // 2) - (ENLARGED_SIZE // 2)
            self.target_y = 80

        # Gerak ke KIRI (dx < 0) -> Flip = True
        dx = self.target_x - self.x()
        self.is_flipped = (dx < 0)
        self.set_visual('lari.gif', enlarge=True)

    def update_movement(self):
        if self.state == "RUNNING_UP":
            dx = self.target_x - self.x()
            dy = self.target_y - self.y()
            distance = (dx**2 + dy**2)**0.5
            
            # Gerak ke KIRI (dx < 0) -> Flip = True
            should_flip = (dx < 0)
            if self.is_flipped != should_flip:
                self.is_flipped = should_flip
                self.set_visual('lari.gif', enlarge=True)

            if distance <= WALK_SPEED:
                self.move(int(self.target_x), int(self.target_y))
                self.state = "SCRATCHING"
                self.set_visual('cakar.gif', enlarge=True)
                QTimer.singleShot(SCRATCH_DELAY, self._execute_close_tab)
            else:
                new_x = int(self.x() + (dx / distance) * WALK_SPEED)
                new_y = int(self.y() + (dy / distance) * WALK_SPEED)
                self.move(new_x, new_y)
            
        elif self.state == "RUNNING_DOWN":
            slow_speed = 1.0  # Kecepatan jalan santai saat pulang
            
            target_x = self.return_x if self.return_x is not None else float(self.home_x)
            target_y = self.return_y if self.return_y is not None else float(self.home_y)
            
            if not hasattr(self, 'float_x') or self.float_x is None:
                self.float_x = float(self.x())
                self.float_y = float(self.y())
            
            dx = target_x - self.float_x
            dy = target_y - self.float_y
            distance = (dx**2 + dy**2)**0.5

            # Gerak ke KIRI (dx < 0) -> Flip = True
            should_flip = (dx < 0)
            if self.is_flipped != should_flip:
                self.is_flipped = should_flip
                self.set_visual('jalan.gif', enlarge=False)
            
            if distance <= 1.5:  # Jika sudah sampai di posisi asal
                self.move(int(target_x), int(target_y))
                self.float_x = None
                self.float_y = None
                self.state = "MEOW"
                self.is_flipped = False  # Reset kembali ke orientasi default (Kanan)
                self.set_visual('meow.gif', enlarge=False)
                self.reset_idle_timer()
            else:
                self.set_visual('jalan.gif', enlarge=False)
                self.float_x += (dx / distance) * slow_speed
                self.float_y += (dy / distance) * slow_speed
                self.move(int(self.float_x), int(self.float_y))

    def _execute_close_tab(self):
        pyautogui.hotkey('ctrl', 'w')
        self.state = "RUNNING_DOWN"
        
        self.float_x = float(self.x())
        self.float_y = float(self.y())
        
        # Tentukan arah jalan pulang menuju return_x
        target_x = self.return_x if self.return_x is not None else float(self.home_x)
        dx = target_x - self.float_x
        self.is_flipped = (dx < 0)
        
        self.set_visual('jalan.gif', enlarge=False)