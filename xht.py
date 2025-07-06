import sys
sys.dont_write_bytecode = True
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QSystemTrayIcon, QMenu, QMessageBox
from PySide6.QtGui import Qt, QColor, QPainter, QBrush, QIcon
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer, QTime, Property
import psutil
import pygetwindow as gw
import os, subprocess

import API
import LogMaker
import Config


print(" __   ___    _ _______ ")
print(" \\ \\ / / |  | |__   __|")
print("  \\ V /| |__| |  | |   ")
print("   > < |  __  |  | |   ")
print("  / . \\| |  | |  | |   ")
print(" /_/ \\_\\_|  |_|  |_|   ")

log=LogMaker.logger()


class xht(QWidget):
    def __init__(self):        
        super().__init__()
        
        sys.excepthook = self.handle_exception
        
        self.weather_api = API.WeatherAPI()
        #self.config = Config.Config().load_config()
        self.background_color = QColor(0, 0, 0)
        self.global_layout = None # 全局布局
        self.ui_type  = "original" #预设UI种类
        self.size_animation = QPropertyAnimation(self, b"size")  # 初始化尺寸动画
        self.size_animation.setDuration(180)  # 将 300 替换为期望的毫秒数
        self.show_animation = QPropertyAnimation(self, b"pos")   # 初始化显示动画
        self.hide_animation = QPropertyAnimation(self, b"pos")   # 初始化隐藏动画
        self.edge_height = 4  # 边缘
        self.is_hiding = False  # 动画状态
        self.is_hidden = False  # 是否隐藏
        self.auto_hide = False # 自动隐藏
        self.is_sleepy = False #班主任视奸状态
        self.fullscreen_apps = ["PowerPoint ", "WPS Presentation Slide ", "希沃白板","Microsoft Edge"]  # 全屏检测关键词列表
        self.sleepy_apps=["AtHomeVideoStreamer"] #视奸应用关键词列表
        
        # 添加系统托盘图标支持
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "res", "icon", "tray_de.ico")))  # 需要准备图标文件
        self.tray_icon.setToolTip("小黑条-正常运行中")
        self.tray_icon.activated.connect(self.handle_tray_activation)
          
        self.create_tray_menu()        
        self.initUI()

    def create_tray_menu(self):
        menu = QMenu()
        restore_action = menu.addAction("显示/隐藏")
        quit_action = menu.addAction("退出")
        
        restore_action.triggered.connect(self.toggle_window)
        quit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(menu)

    def handle_tray_activation(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.toggle_window()

    def toggle_window(self):
        if self.is_hidden:
            self.show_with_animation()
        else:
            self.hide_with_animation()

    def quit_app(self):
        log.info("程序已退出")
        try:
            subprocess.Popen(["taskkill", "/F", "/PID", str(os.getpid())])
        except:
            subprocess.Popen(["kill", str(os.getpid())])

    def initUI(self):
        log.info("程序正在启动")
        self.setMinimumSize(120, 16)
        self.setMaximumSize(600, 400)
        self.setGeometry(0, 8, 120, 16)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle('XHT')

        self.original_ui()
        self.reg_timers()
        self.update_weather()
        
        self.tray_icon.show()

    def getBackgroundColor(self):
        return self.background_color

    def setBackgroundColor(self, color):
        self.background_color = color
        self.update()

    backgroundColor = Property(QColor, getBackgroundColor, setBackgroundColor)

    def handle_exception(self, exc_type, exc_value, traceback):
        error_msg = f"{exc_type.__name__}: {exc_value}"
        log.cirical(f"严重错误: {error_msg}", exc_info=True)
        
        # 在主线程显示错误窗口
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
        self.fullscreen_check_timer.start(3000) 

        self.sleepy_check_timer = QTimer(self)
        self.sleepy_check_timer.timeout.connect(self.scd)
        self.sleepy_check_timer.start(5000)

    def showEvent(self, event):
        super().showEvent(event)
        self.update_position()

        animation = QPropertyAnimation(self, b"pos", self)
        animation.setDuration(250)
        screen = QApplication.primaryScreen().availableGeometry()
        target_x = (screen.width() - self.width()) // 2
        target_y = 8
        initial_pos = QPoint(target_x, -self.height())
        animation.setStartValue(initial_pos)
        animation.setEndValue(QPoint(target_x, target_y))
        animation.setEasingCurve(QEasingCurve.OutQuad)
        animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(self.background_color))  # 使用可配置颜色
        painter.setPen(Qt.PenStyle.NoPen)
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
            city = self.weather_api.GetCity()
            if not city:
                return
            city_id = self.weather_api.LookupCity(city)
            data = self.weather_api.FetchWeatherData(city_id)
            if isinstance(data, dict):
                weather_desc = data["weather_desc"]
                temp = data["temp"] + data["unit"]
                self.weather_label.setText(f"  {weather_desc} {temp}")
                log.info(f"{city}的天气数据更新成功")
        else:
            return

    def update_position(self):
        screen = QApplication.primaryScreen().availableGeometry()
        target_x = (screen.width() - self.width()) // 2
        current_y = self.y()
        self.move(target_x, current_y)

    def set_size(self):
        self.layout().activate()  # 确保布局更新
        self.updateGeometry()     # 更新几何信息
        
        # 获取建议尺寸时考虑布局边距
        content_size = self.layout().sizeHint().expandedTo(self.minimumSize())
        content_size = content_size.boundedTo(self.maximumSize())
        
        # 尺寸未变化时直接返回
        if self.size() == content_size:
            return
        
        # 终止正在进行的动画
        if self.size_animation.state() == QPropertyAnimation.Running:
            self.size_animation.stop()
        
        # 配置复用动画参数
        self.size_animation.setStartValue(self.size())
        self.size_animation.setEndValue(content_size)
        
        # 动画结束处理
        def on_finish():
            self.resize(content_size)
            self.update_position()
        
        # 优化信号连接逻辑 - 避免重复断开连接
        self.size_animation.finished.connect(on_finish)
        self.size_animation.start()

    def original_ui(self):
        log.info("UI模式切换：original")
        self.ui_type = "original"
        # 创建两个独立的标签
        self.time_label = QLabel(self)
        self.weather_label = QLabel(self)
        
        # 保持原有样式
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.apply_label_style(self.time_label)
        self.apply_label_style(self.weather_label)
        
        # 使用水平布局排列两个标签
        self.global_layout = QHBoxLayout()
        self.global_layout.addWidget(self.time_label)
        self.global_layout.addWidget(self.weather_label)
        self.setLayout(self.global_layout)
        self.set_size()

    def apply_label_style(self, label):
        label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            log.info("事件：左键点击")
            if self.is_hidden:
                self.show_with_animation()
            else:
                self.hide_with_animation()
            return
        if event.button() == Qt.RightButton:
            log.info("事件：右键点击")
            self.sleepying()
        super().mousePressEvent(event)

    def show_with_animation(self):
        log.info("执行动作：显示")
        if self.is_hiding or not self.is_hidden:
            return
        
        self.is_hiding = True
        current_pos = self.pos()
        screen = QApplication.primaryScreen().availableGeometry()
        target_x = (screen.width() - self.width()) // 2
        
        # 添加动画存在性判断
        if not self.show_animation:
            self.show_animation = QPropertyAnimation(self, b"pos", self)
        self.show_animation.setDuration(250)
        self.show_animation.setStartValue(current_pos)
        self.show_animation.setEndValue(QPoint(target_x, 8))
        self.show_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        # 添加动画结束事件处理
        def on_finished():
            self.is_hiding = False
            self.is_hidden = False
            
        self.show_animation.finished.connect(on_finished)
        self.show_animation.start()

    def hide_with_animation(self):
        log.info("执行动作：隐藏")
        if self.is_hiding:
            return
        
        self.is_hiding = True
        current_pos = self.pos()
        target_y = current_pos.y() - (self.height() - self.edge_height)
        
        # 添加动画存在性判断
        if not self.hide_animation:
            self.hide_animation = QPropertyAnimation(self, b"pos", self)
        self.hide_animation.setDuration(250)
        self.hide_animation.setStartValue(current_pos)
        self.hide_animation.setEndValue(QPoint(current_pos.x(), target_y))
        self.hide_animation.setEasingCurve(QEasingCurve.OutQuad)
        
        # 添加动画结束事件处理
        def on_finished():
            self.is_hiding = False
            self.is_hidden = True
            
        self.hide_animation.finished.connect(on_finished)
        self.hide_animation.start()

    def unsleepying(self):
        if self.is_sleepy:
            log.info(f"事件：指定的程序触发sleepy蓝点销毁")           
            self.is_sleepy = False
            self.sleepy.hide()
            self.global_layout.removeWidget(self.sleepy)
            self.sleepy.deleteLater()  # 改用deleteLater
            self.sleepy = None
            self.global_layout.update()
            self.set_size()

    def sleepying(self):
        if self.is_sleepy:
            return
        log.info(f"事件：指定的程序触发sleepy蓝点显示") 
        self.is_sleepy = True
        self.sleepy = QLabel(self)
        self.sleepytext=QLabel(self)
        self.sleepytext.setText("监控已开启")
        self.sleepy.setFixedSize(10, 10)
        self.sleepy.setStyleSheet("background-color: #359aff;border: 1px solid #359aff; border-radius: 5px;")
        self.sleepytext.setStyleSheet("color: white;")
        self.global_layout.insertWidget(0, self.sleepy)  # 插入到最左边
        self.global_layout.insertWidget(1, self.sleepytext)  # 插入在小蓝点之后
        self.global_layout.update()
        # 修改为延时2秒后自动删除标签
        QTimer.singleShot(2000, self.sleepytext.deleteLater)
        self.set_size()

    def closeEvent(self, event):
        event.ignore()  # 忽略关闭事件，阻止窗口被关闭

    def fcd(self):
        # 替换win32gui实现跨平台窗口检测
        try:
            active_window = gw.getActiveWindow()
            if not active_window:
                return
            
            # 增加属性访问异常处理和类型校验
            try:
                self.title = active_window.title
            except AttributeError:
                self.title = ""
                
            if not isinstance(self.title, str):
                return
                
            if any(keyword in self.title for keyword in self.fullscreen_apps):
                if not self.is_hidden and not self.auto_hide:
                    log.info(f"事件：指定的程序触发隐藏")
                    self.auto_hide = True
                    self.hide_with_animation()
            else:
                if self.is_hidden and self.auto_hide:
                    log.info(f"事件：指定的程序触发显示")
                    self.auto_hide = False
                    self.show_with_animation()
        except Exception as e:
            log.warn(f"窗口检测异常: {str(e)}")

    def scd(self):
        running_processes = []
        for proc in psutil.process_iter(['name']):
            try:
                if proc.status() == 'running':
                    running_processes.append(proc.name().lower())
            except psutil.NoSuchProcess:
                continue
        # 检查是否有目标进程正在运行
        if any(any(keyword.lower() in proc_name for keyword in self.sleepy_apps) 
              for proc_name in running_processes):
            self.sleepying()
        else:
            self.unsleepying()