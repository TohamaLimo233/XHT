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