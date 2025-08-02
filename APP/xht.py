import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QSystemTrayIcon, QMenu, QMessageBox, QMainWindow
from PySide6.QtGui import Qt, QColor, QPainter, QBrush, QIcon
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer, QTime, Property
import os, subprocess, threading
import platform

from APP import API, LogMaker, Config
import UI.About as AboutUI

#Banner
print(" __   ___    _ _______ ")
print(" \\ \\ / / |  | |__   __|")
print("  \\ V /| |__| |  | |   ")
print("   > < |  __  |  | |   ")
print("  / . \\| |  | |  | |   ")
print(" /_/ \\_\\_|  |_|  |_|   ")

log = LogMaker.logger()

log.info(f"""
运行平台：{platform.system()}
OS版本：{platform.release()}
Python版本：{platform.python_version()}
PID：{os.getpid()}""")
if platform.system() == "Windows" or platform.system() == "Darwin":
    import pygetwindow as gw
elif platform.system() == "Linux":
    from ewmh import ewmh

class xht(QWidget):
    def __init__(self, config_path):        
        super().__init__()
        #先决条件
        sys.excepthook = self.handle_exception
        self.weather_api = API.WeatherAPI()
        self.background_color = QColor(0, 0, 0)
        self.config = Config.load_config(config_path)

        #布局
        self.global_layout = None # 全局布局
        self.ui_type  = "original" #预设UI种类

        #动画
        self.size_animation = QPropertyAnimation(self, b"size")  # 初始化尺寸动画
        self.size_animation.setDuration(180)
        self.show_animation = QPropertyAnimation(self, b"pos")   # 初始化显示动画
        self.hide_animation = QPropertyAnimation(self, b"pos")   # 初始化隐藏动画
        self.is_hiding = False  # 动画状态

        # 新增初始化位置动画
        self.position_animation = QPropertyAnimation(self, b"pos")  # 初始化位置动画
        
        # 身位相关
        self.edge_height = self.config.get("edge_height")  # 边缘
        self.horizontal_edge_margin = self.config.get("horizontal_edge_margin")  # 水平方向边距
        self.is_hidden = False  # 是否隐藏
        self.auto_hide = False # 自动隐藏
        self.windowpos = self.config.get("windowpos")  # 窗口位置
        self.drag_threshold = self.config.get("drag_threshold")  # 拖动触发阈值
        self.window_start_pos = None

        #其他
        self.fullscreen_apps = self.config.get("auto_hide_apps")  # 全屏检测关键词列表
        
        # 添加系统托盘图标支持
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("res/icon/common.ico"))
        self.tray_icon.setToolTip("小黑条-正常运行中")
        self.tray_icon.activated.connect(self.handle_tray_activation)

        # 加载样式表
        self.setStyleSheet("""
                           QLabel {
                           color: white; 
                           font-size: 18px; 
                           font-weight: bold;
                           }""")
          
        self.create_tray_menu()        
        self.initUI()

    def create_tray_menu(self):
        menu = QMenu()
        restore_action = menu.addAction("显示/隐藏")
        about_action = menu.addAction("关于")
        quit_action = menu.addAction("退出")
        
        about_action.triggered.connect(self.show_about_window)
        quit_action.triggered.connect(self.quit_app)
        restore_action.triggered.connect(self.toggle)
        
        self.tray_icon.setContextMenu(menu)

    def toggle(self):
        if self.is_hidden:
            log.info("事件：托盘图标点击，显示窗口")
            self.show_with_animation()
        else:
            log.info("事件：托盘图标点击，隐藏窗口")
            self.hide_with_animation()
    def handle_tray_activation(self, reason):
        return  

    def quit_app(self):
        log.info("程序退出")
        try:
            subprocess.Popen(["taskkill", "/F", "/PID", str(os.getpid())])
        except:
            subprocess.Popen(["kill", str(os.getpid())])

    def initUI(self):
        log.info("程序正在启动")
        self.setMinimumSize(120, 16)
        self.setMaximumSize(600, 400)
        screen = QApplication.primaryScreen().availableGeometry()

        # 根据 windowpos 设置初始位置为屏幕外
        if self.windowpos == "L":
            initial_x = -self.width()
        elif self.windowpos == "R":
            initial_x = screen.width()
        else:
            initial_x = (screen.width() - self.width()) // 2

        self.setGeometry(initial_x, self.edge_height, 120, 16)

        # 设置窗口标志并优化 Wayland 支持
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool
        if platform.system() == "Linux":
            session_type = os.getenv("XDG_SESSION_TYPE", "").lower()
            if session_type == "wayland":
                self.setAttribute(Qt.WA_NativeWindow, True)
                flags = Qt.WindowType.Window  # Use a native window type for Wayland support

        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('XHT')

        self.original_ui()
        threading.Thread(target=self.update_weather).start()
        self.reg_timers()
        self.tray_icon.show()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_position()
        
        screen = QApplication.primaryScreen().availableGeometry()
        current_pos = self.pos()
        
        # 根据windowpos确定初始位置
        if self.windowpos == "L":
            initial_pos = QPoint(-self.width(), current_pos.y())
        elif self.windowpos == "R":
            initial_pos = QPoint(screen.width(), current_pos.y())
        else:  # M
            initial_pos = QPoint(current_pos.x(), -self.height())
        
        # 在 Wayland 环境下避免动画导致窗口不可见
        if platform.system() == "Linux" and os.getenv("XDG_SESSION_TYPE", "").lower() == "wayland":
            self.move(initial_pos)
        else:
            self.position_animation.setDuration(250)
            self.position_animation.setStartValue(initial_pos)
            self.position_animation.setEndValue(current_pos)
            self.position_animation.setEasingCurve(QEasingCurve.OutQuad)
            self.position_animation.start()

    def getBackgroundColor(self):
        return self.background_color

    def setBackgroundColor(self, color):
        self.background_color = color
        self.update()

    backgroundColor = Property(QColor, getBackgroundColor, setBackgroundColor)

    def handle_exception(self, exc_type, exc_value, traceback):
        error_msg = f"{exc_type.__name__}: {exc_value}"
        log.critical(f"严重错误: {error_msg}", exc_info=True)
        
        QTimer.singleShot(0, lambda: self.show_error_window(error_msg))
        
    def show_error_window(self, msg):
        QMessageBox.critical(self,"严重错误",  msg)
        self.quit_app()
    def reg_timers(self):
        self.ortime_timer = QTimer(self)
        self.ortime_timer.timeout.connect(self.update_time)
        self.ortime_timer.start(1500)

        self.check_wea = QTimer(self)
        self.check_wea.timeout.connect(self.update_weather)
        self.check_wea.start(720000)

        self.fullscreen_check_timer = QTimer(self)
        self.fullscreen_check_timer.timeout.connect(self.fcd)
        self.fullscreen_check_timer.start(2000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(self.background_color))
        painter.setPen(Qt.PenStyle.NoPen)
        if platform.system() == "Windows":
            painter.drawRoundedRect(self.rect(), 24, 24)
        if platform.system() == "Linux":
            painter.drawRoundedRect(self.rect(), 24, 24)
        if platform.system() == "Darwin":
            painter.drawRoundedRect(self.rect(), 32, 32)

    def update_time(self):
        if self.ui_type  == "original":
            self.current_time = QTime.currentTime().toString("hh:mm")
            if  self.ui_type == "original":
                self.time_label.setText(self.current_time)
                #self.a=self.a+510
                #self.time_label.setText(str(self.a))
                self.set_size()
        else:
            return 

    def update_weather(self):
        if self.ui_type  == "original":
            weather = self.weather_api.GetWeather()
            self.weather_label.setText(f"  {weather.get('weather')} {str(weather['temperature'])}{weather['unit']}")
            log.info(f"{weather['region']}的天气数据更新成功")
        else:
            return

    def update_position(self):
        screen = QApplication.primaryScreen().availableGeometry()
        if self.windowpos == "L":
            target_x = self.horizontal_edge_margin  # 使用统一的水平边距
        elif self.windowpos == "R":
            target_x = (screen.width() - self.width()) - self.horizontal_edge_margin  # 右侧边距
        else:
            target_x = (screen.width() - self.width()) // 2
        current_y = self.y()
        current_pos = self.pos()
        target_pos = QPoint(target_x, current_y)

        if self.position_animation.state() == QPropertyAnimation.Running:
            self.position_animation.stop()

        self.position_animation.setDuration(250)
        self.position_animation.setStartValue(current_pos)
        self.position_animation.setEndValue(target_pos)
        self.position_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.position_animation.start()

    def set_size(self):
        self.layout().activate()
        self.updateGeometry()
        
        # 获取建议尺寸时考虑布局边距
        content_size = self.layout().sizeHint().expandedTo(self.minimumSize())
        content_size = content_size.boundedTo(self.maximumSize())
        
        # 尺寸未变化时直接返回
        if self.size() == content_size:
            return
        
        if self.size_animation.state() == QPropertyAnimation.Running:
            self.size_animation.stop()
        
        self.size_animation.setStartValue(self.size())
        self.size_animation.setEndValue(content_size)
        
        def on_finish():
            self.resize(content_size)
            self.update_position()
        
        self.size_animation.finished.connect(on_finish)
        self.size_animation.start()

    def original_ui(self):
        log.info("UI模式切换：original")
        self.ui_type = "original"
        self.time_label = QLabel(self)
        self.time_label.setText(QTime.currentTime().toString("hh:mm"))
        self.weather_label = QLabel(self)
        self.weather_label.setText("获取信息中")
        self.weather_label.installEventFilter(self)
        
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.global_layout = QHBoxLayout()
        self.global_layout.addWidget(self.time_label)
        self.global_layout.addWidget(self.weather_label)

        self.setLayout(self.global_layout)
        self.set_size()
    def html_ui(self):
        log.info("UI模式切换：html")
        self.ui_type = "html"
        self.original_ui()
        self.html_text = QLabel(self)
        self.html_text.setText("<html><head><style>body { color: white; font-size: 14px; }</style></head><body>这是HTML模式的文本</body></html>")
        self.html_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.global_layout.addWidget(self.html_text)
        self.set_size()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_pos = event.globalPos()
            self.window_start_pos = self.pos()  # 新增记录窗口初始位置
            self.is_dragging = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.drag_start_pos is not None:
                delta = event.globalPos() - self.drag_start_pos
                if not self.is_dragging and (abs(delta.x()) > self.drag_threshold or abs(delta.y()) > self.drag_threshold):
                    self.is_dragging = True
                if self.is_dragging:
                    # 如果 window_start_pos 未初始化，则使用当前窗口位置
                    if self.window_start_pos is None:
                        self.window_start_pos = self.pos()
                    # 实时水平拖动逻辑
                    new_x = self.window_start_pos.x() + delta.x()
                    self.move(new_x, self.window_start_pos.y())  # 保持原Y坐标不变
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.toggle()
        super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.is_dragging:
            screen = QApplication.primaryScreen().availableGeometry()
            screen_width = screen.width()
            window_center = self.pos().x() + self.width() / 2

            # 根据窗口中心相对于屏幕宽度的比例划分区域
            if window_center < screen_width * 0.30:
                self.windowpos = "L"  
            elif window_center > screen_width * 0.70:
                self.windowpos = "R"  
            else:
                self.windowpos = "M"  

            self.update_position()
        self.drag_start_pos = None
        self.is_dragging = False
        super().mouseReleaseEvent(event)

    def show_with_animation(self):
        log.info("事件：显示")
        if self.is_hiding or not self.is_hidden:
            return

        self.is_hiding = True
        current_pos = self.pos()
        screen = QApplication.primaryScreen().availableGeometry()

        # 确定 Y 坐标：优先使用 window_start_pos，否则使用当前 Y
        window_y = current_pos.y()
        if self.window_start_pos is not None:
            window_y = self.window_start_pos.y()

        if self.windowpos == "L":
            # 从左侧隐藏位置开始，移动到正常位置
            initial_pos = QPoint(-self.width() + self.edge_height, current_pos.y())
            target_pos = QPoint(self.horizontal_edge_margin, window_y)
        elif self.windowpos == "R":
            screen_width = screen.width()
            screen_width_minus_margin = screen_width - self.width() - self.horizontal_edge_margin
            # 从右侧隐藏位置开始，移动到正常位置
            initial_pos = QPoint(screen_width - self.edge_height, current_pos.y())
            target_pos = QPoint(screen_width_minus_margin, window_y)
        else:
            # 垂直方向处理保持不变
            initial_pos = QPoint(current_pos.x(), -self.height())
            target_pos = QPoint(current_pos.x(), self.edge_height)

        if not self.show_animation:
            self.show_animation = QPropertyAnimation(self, b"pos", self)
        self.show_animation.setDuration(250)
        self.show_animation.setStartValue(initial_pos)
        self.show_animation.setEndValue(target_pos)
        self.show_animation.setEasingCurve(QEasingCurve.OutQuad)

        def on_finished():
            self.is_hiding = False
            self.is_hidden = False

        self.show_animation.finished.connect(on_finished)
        self.show_animation.start()

    def hide_with_animation(self):
        log.info("事件：隐藏")
        if self.is_hiding:
            return
        
        self.is_hiding = True
        current_pos = self.pos()
        screen = QApplication.primaryScreen().availableGeometry()
        
        if self.windowpos in ["L", "R"]:
            if self.windowpos == "L":
                # 保留edge_height宽度可见
                target_x = 0 - (self.width() - self.edge_height)
            else:
                # 保留edge_height宽度可见
                target_x = screen.width() - self.edge_height
                
            target_pos = QPoint(target_x, current_pos.y())
        else:
            # 垂直方向保持原逻辑
            target_y = current_pos.y() - (self.height() - self.edge_height)
            target_pos = QPoint(current_pos.x(), target_y)
        
        if not self.hide_animation:
            self.hide_animation = QPropertyAnimation(self, b"pos", self)
        self.hide_animation.setDuration(250)
        self.hide_animation.setStartValue(current_pos)
        self.hide_animation.setEndValue(target_pos)
        self.hide_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        def on_finished():
            self.is_hiding = False
            self.is_hidden = True
            
        self.hide_animation.finished.connect(on_finished)
        self.hide_animation.start()

    def closeEvent(self, event):
        event.ignore()  # 忽略关闭事件

    def fcd(self):
        try:
            if platform.system() == "Linux":
                import os
                session_type = os.getenv("XDG_SESSION_TYPE", "").lower()
                if session_type == "wayland":
                    log.warning("检测到 Wayland 环境，自动隐藏功能可能无法正常工作。")
                    self.title = ""
                else:
                    try:
                        ewmh_obj = ewmh.EWMH()
                        active_window = ewmh_obj.getActiveWindow()
                        if active_window:
                            self.title = ewmh_obj.getWmName(win=active_window)
                        else:
                            self.title = ""
                    except Exception as e:
                        log.warning(f"Linux 窗口检测异常: {str(e)}")
                        self.title = ""
            else:
                # 原有 Windows/macOS 逻辑
                active_window = gw.getActiveWindow()
                if not active_window:
                    return
                try:
                    self.title = active_window.title
                except AttributeError:
                    self.title = ""
        except Exception as e:
            log.warning(f"窗口检测异常: {str(e)}")

    def show_about_window(self):
        """显示关于窗口"""
        
        self.about_window = QMainWindow()
        ui = AboutUI.Ui_AboutWindow()
        ui.setupUi(self.about_window)
        log.info("事件：显示关于窗口")
        self.about_window.show()

    def refresh(self, config_path):
        """刷新窗口"""
        if self.ui_type == "original":
            self.config = Config.load_config(config_path)
            self.edge_height = self.config.get("edge_height")  # 边缘
            self.horizontal_edge_margin = self.config.get("horizontal_edge_margin")  # 水平方向边距
            self.windowpos = self.config.get("windowpos")  # 窗口位置
            self.drag_threshold = self.config.get("drag_threshold")  # 拖动触发阈值
            self.fullscreen_apps = self.config.get("auto_hide_apps")
            self.update_position()
            self.set_size()
            self.update_time()
            self.update_weather()
