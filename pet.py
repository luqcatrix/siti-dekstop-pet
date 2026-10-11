import pyautogui
import pygetwindow as gw
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QMovie, QPixmap
from config import PET_SIZE, ENLARGED_SIZE, WALK_SPEED, SCRATCH_DELAY, IDLE_TIMEOUT, SHAKE_THRESHOLD

class SitiPet(QWidget):
    attack_signal = pyqtSignal()
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
        self.current_filename = "" # Tambahan: Untuk melacak GIF apa yang sedang diputar
        self.state = "MEOW"
        self.pre_drag_state = "MEOW"
        
        self.drag_pos = None
        self.last_mouse_pos = None
        self.shake_distance = 0
        self.target_x = 0
        self.target_y = 0
        
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
    # MANAJER UKURAN & VISUAL (DIPERBAIKI)
    # ==========================================
    def set_size(self, size):
        self.resize(size, size)
        self.label.resize(size, size)

    def set_visual(self, filename, is_png=False, enlarge=False):
        # Mencegah pemuatan ulang GIF yang sama berulang kali (Mencegah "Nyangkut")
        if self.current_filename == filename and not is_png:
            return

        self.current_filename = filename

        if enlarge:
            self.set_size(ENLARGED_SIZE)
        else:
            self.set_size(PET_SIZE)

        self.label.clear()

        if self.current_movie:
            self.current_movie.stop()
            self.current_movie = None
            
        if is_png:
            pixmap = QPixmap(f"asset/{filename}")
            self.label.setPixmap(pixmap)
        else:
            self.current_movie = QMovie(f"asset/{filename}")
            
            if not self.current_movie.isValid():
                print(f"⚠️ ERROR VISUAL: File asset/{filename} gagal dimuat! Cek namanya di folder.")
                
            self.label.setMovie(self.current_movie)
            self.current_movie.start()

    def reset_idle_timer(self):
        self.idle_timer.start(IDLE_TIMEOUT)

    # ==========================================
    # INTERAKSI MOUSE (DRAG & SHAKE)
    # ==========================================
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
        # Aturan Spesial: Jika ditarik/digoyang saat tidur -> Marah -> Mau Tidur -> Tidur
        if self.pre_drag_state == 'IDLE':
            self.state = 'ANGRY'
            self.set_visual('marah.gif', enlarge=False) # Ukuran normal saat dibangunkan
            QTimer.singleShot(1500, self._after_angry_drag)
        else:
            self.state = 'MEOW'
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
        self.set_visual('tidur.gif', enlarge=False)

    # ==========================================
    # LOGIKA SERANGAN DOOMSCROLL
    # ==========================================
    def trigger_alert(self):
        if self.state in ['IDLE', 'MEOW']:
            self.state = 'MEOW'
            self.set_visual('meow.gif', enlarge=False)
            self.reset_idle_timer()

    def attack_tab(self):
        if self.state in ['IDLE', 'MEOW']:
            self.idle_timer.stop()
            self.state = 'ANGRY'
            
            self.set_visual('marah.gif', enlarge=True)
            
            offset = (ENLARGED_SIZE - PET_SIZE) // 2
            self.move(self.x() - offset, self.y() - offset)
            
            QTimer.singleShot(1500, self._start_running_up)
            
    def _start_running_up(self):
        self.state = "RUNNING_UP"
        
        # Di sini lari.gif diputar (dan tidak akan ter-restart berkat fitur baru di set_visual)
        self.set_visual('lari.gif', enlarge=True)
        
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                self.target_x = active_window.left + (active_window.width // 2) - (ENLARGED_SIZE // 2)
                self.target_y = active_window.top + (active_window.height // 2) - (ENLARGED_SIZE // 2)
            else:
                self.target_x = (self.screen_rect.width() // 2) - (ENLARGED_SIZE // 2)
                self.target_y = (self.screen_rect.height() // 2) - (ENLARGED_SIZE // 2)
        except:
            self.target_x = (self.screen_rect.width() // 2) - (ENLARGED_SIZE // 2)
            self.target_y = (self.screen_rect.height() // 2) - (ENLARGED_SIZE // 2)

    def update_movement(self):
        if self.state == "RUNNING_UP":
            dx = self.target_x - self.x()
            dy = self.target_y - self.y()
            distance = (dx**2 + dy**2)**0.5
            
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
            target_x = self.home_x
            target_y = self.home_y
            
            dx = target_x - self.x()
            dy = target_y - self.y()
            distance = (dx**2 + dy**2)**0.5
            
            if distance <= WALK_SPEED:
                self.move(target_x, target_y)
                self.state = "MEOW"
                self.set_visual('meow.gif', enlarge=False)
                self.reset_idle_timer()
            else:
                # Disini jalan.gif di-set. Jika dipanggil berulang, set_visual akan mengabaikannya
                self.set_visual('jalan.gif', enlarge=False)
                new_x = int(self.x() + (dx / distance) * WALK_SPEED)
                new_y = int(self.y() + (dy / distance) * WALK_SPEED)
                self.move(new_x, new_y)

    def _execute_close_tab(self):
        pyautogui.hotkey('ctrl', 'w')
        self.state = "RUNNING_DOWN"
        # Memulai animasi berjalan pulang
        self.set_visual('jalan.gif', enlarge=False)