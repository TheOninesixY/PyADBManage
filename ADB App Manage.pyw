import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import subprocess
import os
import threading
import sv_ttk # 导入 sv_ttk 库

class ADBInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB 应用管理器")
        try:
            # 使用绝对路径设置图标
            import os
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            # 图标设置失败不影响程序运行
            pass
        self.root.geometry("700x600")
        self.default_geometry = "700x600"
        self.root.resizable(True, True)
        self.current_theme = None # 初始主题未设置，将在_apply_theme中加载或设置为默认
        self._apply_theme() # 应用主题 (根据保存的设置或默认值)
        
        # 设置主窗口背景色 - WinUI风格
        # self.root.configure(bg='#f2f2f2') # 交给 sv_ttk 处理主题
        
    def _apply_theme(self):
        """
        应用当前主题设置。
        如果current_theme未设置，则尝试从设置加载；如果加载失败，则使用默认主题。
        """
        DEFAULT_THEME = "dark" # 定义默认主题
        
        if self.current_theme is None:
            # 在此处可以添加从配置文件加载主题的逻辑
            # 暂时直接设置为默认主题
            self.current_theme = DEFAULT_THEME
            
        try:
            sv_ttk.set_theme(self.current_theme)
        except Exception as e:
            self.log(f"设置主题失败: {self.current_theme}。回退到默认主题 {DEFAULT_THEME}。错误: {e}")
            self.current_theme = DEFAULT_THEME
            sv_ttk.set_theme(self.current_theme) # 尝试设置默认主题

        # 设置样式 - WinUI风格
        self.style = ttk.Style()
        
        # 主色调 - WinUI风格的蓝色
        winui_blue = '#0078d4'
        winui_light_blue = '#e6f3ff'
        winui_gray = '#f2f2f2'
        winui_dark_gray = '#e6e6e6'
        winui_text = '#333333'
        winui_border = '#e0e0e0'
        
        # 配置Tkinter默认对话框的样式
        # self.root.option_add('*Dialog.msg.font', 'Segoe UI 10') # 交给 sv_ttk 处理主题
        # self.root.option_add('*Dialog.btn.font', 'Segoe UI 10') # 交给 sv_ttk 处理主题
        # self.root.option_add('*Dialog.background', winui_gray) # 交给 sv_ttk 处理主题
        # self.root.option_add('*Dialog.foreground', winui_text) # 交给 sv_ttk 处理主题
        # self.root.option_add('*Dialog.button.background', winui_gray) # 交给 sv_ttk 处理主题
        # self.root.option_add('*Dialog.button.foreground', winui_text) # 交给 sv_ttk 处理主题
        # self.root.option_add('*Dialog.button.borderwidth', 1) # 交给 sv_ttk 处理主题
        # self.root.option_add('*Dialog.button.relief', 'flat') # 交给 sv_ttk 处理主题
        # self.root.option_add('*Dialog.button.highlightbackground', winui_gray) # 交给 sv_ttk 处理主题
        
        # 配置全局样式
        # self.style.configure('.',
        #                    font=('Segoe UI', 10),
        #                    foreground=winui_text,
        #                    background=winui_gray)
        
        # 配置按钮样式
        # self.style.configure('TButton',
        #                    padding=8,
        #                    relief="flat",
        #                    background=winui_gray,
        #                    foreground=winui_text,
        #                    borderwidth=1,
        #                    bordercolor=winui_border)
        
        # 按钮悬停效果
        # self.style.map('TButton',
        #               background=[('active', winui_dark_gray)],
        #               bordercolor=[('active', winui_blue)])
        
        # 配置标签样式
        # self.style.configure('TLabel',
        #                    padding=6,
        #                    foreground=winui_text,
        #                    background=winui_gray)
        
        # 配置输入框样式
        # self.style.configure('TEntry',
        #                    padding=6,
        #                    relief="flat",
        #                    borderwidth=1,
        #                    bordercolor=winui_border,
        #                    background='white')
        
        # 配置标签框架样式
        # self.style.configure('TLabelframe',
        #                    padding=10,
        #                    foreground=winui_text,
        #                    background=winui_gray)
        
        # self.style.configure('TLabelframe.Label',
        #                    font=('Segoe UI', 10, 'bold'),
        #                    padding=(5, 0, 0, 0))
        
        # 配置笔记本（选项卡）样式
        # self.style.configure('TNotebook',
        #                    background=winui_gray)
        
        # self.style.configure('TNotebook.Tab',
        #                    padding=3,
        #                    font=('Segoe UI', 10),
        #                    background=winui_dark_gray,
        #                    foreground=winui_text)
        
        # 选项卡选中效果
        # self.style.map('TNotebook.Tab',
        #               background=[('selected', 'white')],
        #               foreground=[('selected', winui_blue)])
        
        # 配置滚动条样式
        # self.style.configure('Vertical.TScrollbar',
        #                    background=winui_gray,
        #                    bordercolor=winui_border)
        
        # self.style.configure('Horizontal.TScrollbar',
        #                    background=winui_gray,
        #                    bordercolor=winui_border) # 交给 sv_ttk 处理主题
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建选项卡控件
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建管理选项卡
        self.package_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.package_tab, text="首页")

        # 创建文件管理选项卡
        self.file_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.file_tab, text="文件管理")

        # 创建设置选项卡
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="设置")
        
        # 绑定选项卡切换事件
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
                
        # 初始化变量
        self.apk_path = ""
        self.is_connected = False
        self.auto_connect = False
        self.show_emoji = True  # 默认显示emoji
        self.package_var = tk.StringVar(value="")
        self.apk_var = tk.StringVar(value="未选择文件")
        
        # 获取adb.exe路径
        self.adb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adb.exe")
        
        # 在操作状态选项卡中创建状态显示部分
        self.create_status_section()
        
        # 在设置选项卡中创建设置部分
        self.create_settings_section()
        
        # 在管理选项卡中创建包名管理部分
        self.create_package_section()
        
        # 在文件管理选项卡中创建文件管理部分
        self.create_file_section()
        
        # 加载设置
        self.load_settings()
        
        # 应用启动时自动刷新包名列表
        self.auto_refresh_packages_on_start()
        
        # 绑定Ctrl+R快捷键恢复全部设置
        self.root.bind('<Control-r>', lambda event: self.restore_all_settings())
    

    
    def create_status_section(self):
        """创建状态显示部分"""
        status_frame = ttk.LabelFrame(self.package_tab, text="操作状态", padding="10")
        status_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=5)
        
        # 状态文本框 - WinUI风格
        self.status_text = tk.Text(status_frame, 
                                 height=10,
                                 font=('Segoe UI', 10),
                                 borderwidth=1,
                                 relief='solid',
                                 highlightthickness=0)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        self.status_text.config(state=tk.DISABLED)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, before=self.status_text)
        self.status_text.config(yscrollcommand=scrollbar.set)
    

    
    def log(self, message):
        """记录日志信息"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
    

    
    def create_settings_section(self):
        """创建设置选项卡部分"""
        settings_frame = ttk.LabelFrame(self.settings_tab, text="设置选项", padding="10")
        settings_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # ADB连接配置
        conn_frame = ttk.LabelFrame(settings_frame, text="ADB连接配置", padding="10")
        conn_frame.pack(fill=tk.X, pady=5)
        
        # IP地址输入
        ttk.Label(conn_frame, text="设备IP地址:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ip_var = tk.StringVar(value="127.0.0.1")
        self.ip_entry = ttk.Entry(conn_frame, textvariable=self.ip_var)
        self.ip_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        self.ip_entry.bind('<FocusOut>', lambda event: self.save_settings())
        self.ip_entry.bind('<Return>', lambda event: self.save_settings())
        
        # 端口输入
        ttk.Label(conn_frame, text="端口:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.port_var = tk.StringVar(value="58526")
        self.port_entry = ttk.Entry(conn_frame, textvariable=self.port_var)
        self.port_entry.grid(row=0, column=3, sticky=tk.W+tk.E, pady=5)
        self.port_entry.bind('<FocusOut>', lambda event: self.save_settings())
        self.port_entry.bind('<Return>', lambda event: self.save_settings())
        
        # 配置列权重，使输入框随窗口大小调整
        conn_frame.columnconfigure(1, weight=1)
        conn_frame.columnconfigure(3, weight=1)
        
        # 连接按钮
        self.connect_btn = ttk.Button(conn_frame, text="连接", command=self.connect_device)
        self.connect_btn.grid(row=0, column=4, padx=10, pady=5, sticky=tk.W+tk.E)
        
        # 断开按钮
        self.disconnect_btn = ttk.Button(conn_frame, text="断开", command=self.disconnect_device, state=tk.DISABLED)
        self.disconnect_btn.grid(row=0, column=5, padx=10, pady=5, sticky=tk.W+tk.E)
        
        # 自动连接选项
        ttk.Label(conn_frame, text="自动连接:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # 创建开关控件
        self.auto_connect_var = tk.BooleanVar(value=self.auto_connect)
        self.auto_connect_switch = ttk.Checkbutton(
            conn_frame, 
            text="启用", 
            variable=self.auto_connect_var, 
            command=self.on_auto_connect_toggle
        )
        self.auto_connect_switch.grid(row=1, column=1, sticky=tk.W, pady=5, columnspan=5)
        
        # 配置按钮列的权重
        conn_frame.columnconfigure(4, weight=1)
        conn_frame.columnconfigure(5, weight=1)
        
        # 自定义设置
        custom_frame = ttk.LabelFrame(settings_frame, text="自定义", padding="10")
        custom_frame.pack(fill=tk.X, pady=5)
        
        # 窗口大小设置
        window_size_frame = ttk.LabelFrame(custom_frame, text="窗口大小", padding="10")
        window_size_frame.pack(fill=tk.X, pady=5)
        
        # 窗口大小输入框
        ttk.Label(window_size_frame, text="窗口大小:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.window_size_var = tk.StringVar(value=self.default_geometry)
        self.window_size_entry = ttk.Entry(window_size_frame, textvariable=self.window_size_var)
        self.window_size_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5, padx=5)
        self.window_size_entry.bind('<FocusOut>', lambda event: self.save_settings())
        self.window_size_entry.bind('<Return>', lambda event: self.save_settings())
        
        # 识别当前窗口大小按钮
        identify_btn = ttk.Button(window_size_frame, text="识别当前大小", command=self.identify_window_size)
        identify_btn.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # 恢复默认按钮
        default_btn = ttk.Button(window_size_frame, text="恢复默认", command=self.restore_default_window_size)
        default_btn.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # 配置列权重
        window_size_frame.columnconfigure(1, weight=1)
        window_size_frame.columnconfigure(2, weight=1)
        window_size_frame.columnconfigure(3, weight=1)
        
        # 显示emoji选项
        emoji_frame = ttk.LabelFrame(custom_frame, text="外观", padding="10")
        emoji_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(emoji_frame, text="显示文件emoji:").pack(side=tk.LEFT, padx=10)
        
        # 创建开关控件
        self.show_emoji_var = tk.BooleanVar(value=self.show_emoji)
        self.show_emoji_switch = ttk.Checkbutton(
            emoji_frame, 
            text="启用", 
            variable=self.show_emoji_var, 
            command=self.on_show_emoji_toggle
        )
        self.show_emoji_switch.pack(side=tk.LEFT)

        # 主题设置
        theme_frame = ttk.LabelFrame(custom_frame, text="主题", padding="10")
        theme_frame.pack(fill=tk.X, pady=5)

        ttk.Label(theme_frame, text="选择主题:").pack(side=tk.LEFT, padx=10)

        self.theme_var = tk.StringVar(value=self.current_theme) # 根据当前主题初始化
        self.light_theme_radio = ttk.Radiobutton(theme_frame, text="亮色", variable=self.theme_var, value="light", command=self.on_theme_change)
        self.light_theme_radio.pack(side=tk.LEFT, padx=5)

        self.dark_theme_radio = ttk.Radiobutton(theme_frame, text="深色", variable=self.theme_var, value="dark", command=self.on_theme_change)
        self.dark_theme_radio.pack(side=tk.LEFT, padx=5)
        
        # 恢复默认设置按钮
        restore_default_btn = ttk.Button(settings_frame, text="恢复默认设置", command=self.restore_all_settings_with_confirmation)
        restore_default_btn.pack(fill=tk.X, pady=10, padx=10)
        
    

    
    def browse_apk_manage(self):
        """管理选项卡中的浏览选择APK文件并安装"""
        file_path = filedialog.askopenfilename(
            title="选择APK文件",
            filetypes=[("APK文件", "*.apk"), ("所有文件", "*.*")]
        )
        if file_path:
            self.apk_path = file_path
            self.apk_var.set(file_path)
            self.log(f"选择APK文件: {file_path}")
            self.install_apk()
    
    def connect_device(self, is_auto_connect=False):
        """连接ADB设备"""
        ip = self.ip_var.get()
        port = self.port_var.get()
        
        if not ip or not port:
            self.show_error_dialog("错误", "请输入IP地址和端口")
            return
        
        # 禁用连接按钮，启用断开按钮
        self.connect_btn.config(state=tk.DISABLED)
        self.disconnect_btn.config(state=tk.NORMAL)
        
        # 在线程中执行ADB连接命令
        threading.Thread(target=self._connect_device_thread, args=(ip, port, is_auto_connect)).start()
    
    def _connect_device_thread(self, ip, port, is_auto_connect=False):
        """连接设备的线程函数"""
        try:
            self.log(f"正在连接设备: {ip}:{port}")
            
            # 执行ADB连接命令
            result = subprocess.run(
                [self.adb_path, "connect", f"{ip}:{port}"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            stdout = result.stdout or ""
            if "connected to" in stdout:
                self.log(f"连接成功: {ip}:{port}")
                self.is_connected = True
                # 启用安装按钮
                self.install_btn_manage.config(state=tk.NORMAL)
                # 非自动连接时显示连接成功弹窗
                if not is_auto_connect:
                    self.show_info_dialog("成功", f"设备连接成功: {ip}:{port}")
                # 检查设备状态
                self._check_device_state()
            else:
                stderr = result.stderr or ""
                error_msg = stderr or stdout
                self.log(f"连接失败: {error_msg}")
                self.is_connected = False
                # 恢复按钮状态
                self.connect_btn.config(state=tk.NORMAL)
                self.disconnect_btn.config(state=tk.DISABLED)
                self.install_btn_manage.config(state=tk.DISABLED)
        except Exception as e:
            self.log(f"连接出错: {str(e)}")
            self.is_connected = False
            # 恢复按钮状态
            self.connect_btn.config(state=tk.NORMAL)
            self.disconnect_btn.config(state=tk.DISABLED)
            self.install_btn_manage.config(state=tk.DISABLED)
    
    def _check_device_state(self):
        """检查设备状态"""
        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=5,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            stdout = result.stdout or ""
            self.log(f"设备状态:\n{stdout}")
        except Exception as e:
            self.log(f"检查设备状态出错: {str(e)}")
    
    def disconnect_device(self):
        """断开ADB设备连接"""
        # 禁用断开按钮，启用连接按钮
        self.disconnect_btn.config(state=tk.DISABLED)
        self.connect_btn.config(state=tk.NORMAL)
        self.install_btn_manage.config(state=tk.DISABLED)
        
        # 在线程中执行ADB断开命令
        threading.Thread(target=self._disconnect_device_thread).start()
    
    def _disconnect_device_thread(self):
        """断开设备的线程函数"""
        try:
            self.log("正在断开设备连接")
            
            # 执行ADB断开命令
            result = subprocess.run(
                [self.adb_path, "disconnect"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            stdout = result.stdout or ""
            self.log(f"断开连接结果: {stdout}")
            self.is_connected = False
        except Exception as e:
            self.log(f"断开连接出错: {str(e)}")
    
    def install_apk(self):
        """安装APK文件"""
        if not self.apk_path:
            self.show_error_dialog("错误", "请选择APK文件")
            return
        
        if not self.is_connected:
            self.show_error_dialog("错误", "请先连接设备")
            return
        
        # 在线程中执行APK安装命令
        threading.Thread(target=self._install_apk_thread).start()
    
    def _install_apk_thread(self):
        """安装APK的线程函数"""
        try:
            self.log(f"正在安装APK: {self.apk_path}")
            
            # 执行ADB安装命令
            process = subprocess.Popen(
                [self.adb_path, "install", self.apk_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # 实时输出安装过程
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                try:
                    # 尝试使用utf-8解码
                    decoded_line = line.decode('utf-8', errors='replace').strip()
                    self.log(decoded_line)
                except Exception as decode_error:
                    self.log(f"解码输出时出错: {str(decode_error)}")
            
            process.wait()
            
            if process.returncode == 0:
                self.log("APK安装成功！")
                self.show_info_dialog("成功", "APK安装成功！")
            else:
                self.log("APK安装失败！")
                self.show_error_dialog("错误", "APK安装失败！")
        except Exception as e:
            self.log(f"安装出错: {str(e)}")
            self.show_error_dialog("错误", f"安装出错: {str(e)}")
    
    def uninstall_app(self):
        """卸载应用"""
        package_name = self.package_var.get().strip()
        
        if not package_name:
            self.show_error_dialog("错误", "请输入应用包名")
            return
        
        if not self.is_connected:
            self.show_error_dialog("错误", "请先连接设备")
            return
        
        # 在线程中执行应用卸载命令
        threading.Thread(target=self._uninstall_app_thread, args=(package_name,)).start()
    
    def _uninstall_app_thread(self, package_name):
        """卸载应用的线程函数"""
        try:
            self.log(f"正在卸载应用: {package_name}")
            
            # 执行ADB卸载命令
            process = subprocess.Popen(
                [self.adb_path, "uninstall", package_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # 实时输出卸载过程
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                try:
                    # 尝试使用utf-8解码
                    decoded_line = line.decode('utf-8', errors='replace').strip()
                    self.log(decoded_line)
                except Exception as decode_error:
                    self.log(f"解码输出时出错: {str(decode_error)}")
            
            process.wait()
            
            if process.returncode == 0:
                self.log(f"应用 {package_name} 卸载成功！")
                self.show_info_dialog("成功", f"应用 {package_name} 卸载成功！")
            else:
                self.log(f"应用 {package_name} 卸载失败！")
                self.show_error_dialog("错误", f"应用 {package_name} 卸载失败！")
        except Exception as e:
            self.log(f"卸载出错: {str(e)}")
            self.show_error_dialog("错误", f"卸载出错: {str(e)}")
    
    def load_settings(self):
        """加载设置"""
        # 使用脚本所在目录作为基础路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(script_dir, "data")
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        if line.startswith('auto_connect='):
                            value = line.split('=', 1)[1].lower()
                            self.auto_connect = value == 'true'
                            if hasattr(self, 'auto_connect_var'):
                                self.auto_connect_var.set(self.auto_connect)
                        elif line.startswith('ip='):
                            value = line.split('=', 1)[1]
                            if hasattr(self, 'ip_var'):
                                self.ip_var.set(value)
                        elif line.startswith('port='):
                            value = line.split('=', 1)[1]
                            if hasattr(self, 'port_var'):
                                self.port_var.set(value)
                        elif line.startswith('show_emoji='):
                            value = line.split('=', 1)[1].lower()
                            self.show_emoji = value == 'true'
                            if hasattr(self, 'show_emoji_var'):
                                self.show_emoji_var.set(self.show_emoji)
                        elif line.startswith('window_size='):
                            value = line.split('=', 1)[1]
                            if hasattr(self, 'window_size_var'):
                                self.window_size_var.set(value)
                            # 应用窗口大小
                            self.root.geometry(value)
                        elif line.startswith('theme='):
                            value = line.split('=', 1)[1]
                            self.current_theme = value
                            if hasattr(self, 'theme_var'):
                                self.theme_var.set(value)
                            sv_ttk.set_theme(value) # 应用主题
                self.log("设置加载成功")
                
                # 如果启用了自动连接，尝试连接设备
                if self.auto_connect:
                    self.log("启用了自动连接，正在尝试连接设备...")
                    ip = self.ip_var.get()
                    port = self.port_var.get()
                    if ip and port:
                        self.connect_device(is_auto_connect=True)
        except Exception as e:
            self.log(f"加载设置出错: {str(e)}")
    
    def save_settings(self):
        """保存设置"""
        # 使用脚本所在目录作为基础路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(script_dir, "data")
        self.auto_connect = self.auto_connect_var.get()
        self.show_emoji = self.show_emoji_var.get()
        ip = self.ip_var.get()
        port = self.port_var.get()
        
        window_size = self.window_size_var.get()
        # 应用窗口大小
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(f"auto_connect={self.auto_connect}\n")
            f.write(f"show_emoji={self.show_emoji}\n")
            f.write(f"ip={ip}\n")
            f.write(f"port={port}\n")
            f.write(f"window_size={window_size}\n")
            f.write(f"theme={self.current_theme}\n") # 保存主题设置
    
    def on_auto_connect_toggle(self):
        """自动连接开关切换时的回调"""
        # 这里可以添加一些即时反馈，比如显示提示信息
        self.save_settings()
    
    def on_show_emoji_toggle(self):
        """显示emoji开关切换时的回调"""
        # 这里可以添加一些即时反馈，比如显示提示信息
        self.save_settings()
    
    def on_theme_change(self):
        """主题切换时的回调"""
        selected_theme = self.theme_var.get()
        sv_ttk.set_theme(selected_theme)
        self.current_theme = selected_theme
        self.save_settings()
    
    def identify_window_size(self):
        """识别当前窗口大小并填入输入框"""
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        self.window_size_var.set(f"{width}x{height}")
        self.log(f"已识别当前窗口大小: {width}x{height}")
    
    def restore_default_window_size(self):
        """恢复默认窗口大小"""
        default_size = self.default_geometry
        self.window_size_var.set(default_size)
        self.root.geometry(default_size)
        self.log(f"已恢复默认窗口大小: {default_size}")
    
    def restore_all_settings_with_confirmation(self):
        """恢复全部设置到默认值（带确认）"""
        if self.ask_yes_no_dialog("确认恢复", "确定将所有设置恢复为默认值吗？"):
            self.restore_all_settings()

    def restore_all_settings(self):
        """恢复全部设置到默认值"""
        # 恢复默认窗口大小
        default_size = "600x600"
        self.window_size_var.set(default_size)
        self.root.geometry(default_size)
        
        # 恢复其他默认设置
        self.auto_connect_var.set(False)
        self.show_emoji_var.set(True)
        self.ip_var.set("127.0.0.1")
        self.port_var.set("58526")
        
        self.log("已恢复全部设置到默认值")
    
    def create_package_section(self):
        """创建包名管理部分"""
        package_frame = ttk.LabelFrame(self.package_tab, text="已安装包名", padding="10")
        package_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 搜索框部分
        search_frame = ttk.Frame(package_frame)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="搜索包名:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.search_entry.bind('<KeyRelease>', self.filter_packages)
        
        # 安装按钮
        self.install_btn_manage = ttk.Button(search_frame, text="安装", command=self.browse_apk_manage)
        self.install_btn_manage.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        
        # 刷新按钮
        self.refresh_btn = ttk.Button(search_frame, text="刷新包名", command=self.refresh_packages)
        self.refresh_btn.pack(side=tk.RIGHT, padx=5, fill=tk.X, expand=True)
        
        # 包名列表
        list_frame = ttk.Frame(package_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 包名列表框 - WinUI风格
        self.package_listbox = tk.Listbox(list_frame, 
                                         height=15,
                                         font=('Segoe UI', 10),
                                         borderwidth=1,
                                         relief='solid',
                                         highlightthickness=0)
        self.package_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, command=self.package_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.package_listbox.config(yscrollcommand=scrollbar.set)
        
        # 为列表框添加右键菜单
        self.package_listbox.bind('<Button-3>', self.show_package_menu)
        # 为列表框添加双击事件
        self.package_listbox.bind('<Double-1>', self.on_package_double_click)
        
        # 创建右键菜单
        self.package_menu = tk.Menu(self.root, tearoff=0) # 移除硬编码颜色，交给 sv_ttk 处理主题
        self.package_menu.add_command(label="卸载", command=self.uninstall_selected_package)
        self.package_menu.add_command(label="复制包名", command=self.copy_package_name)
        
        # 包名数据
        self.package_list = []
    
    def refresh_packages(self):
        """刷新已安装包名列表"""
        if not self.is_connected:
            self.show_error_dialog("错误", "请先连接设备")
            return
        
        # 清空列表
        self.package_listbox.delete(0, tk.END)
        self.log("正在获取已安装包名...")
        
        # 在线程中执行ADB命令获取包名
        threading.Thread(target=self._refresh_packages_thread).start()
    
    def _refresh_packages_thread(self):
        """获取包名的线程函数"""
        try:
            # 执行ADB命令获取所有包名
            result = subprocess.run(
                [self.adb_path, "shell", "pm", "list", "packages"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            stdout = result.stdout or ""
            if stdout:
                # 解析包名
                self.package_list = []
                for line in stdout.strip().split('\n'):
                    if line.startswith('package:'):
                        package_name = line[8:]  # 移除 'package:' 前缀
                        self.package_list.append(package_name)
                
                # 更新列表框
                self.root.after(0, self._update_package_listbox)
                self.log(f"成功获取 {len(self.package_list)} 个包名")
            else:
                self.log("未获取到包名信息")
        except Exception as e:
            self.log(f"获取包名出错: {str(e)}")
    
    def _update_package_listbox(self):
        """更新包名列表框"""
        self.package_listbox.delete(0, tk.END)
        for package in self.package_list:
            self.package_listbox.insert(tk.END, package)
    
    def filter_packages(self, event=None):
        """根据搜索框输入过滤包名列表"""
        search_text = self.search_var.get().lower()
        
        # 清空列表
        self.package_listbox.delete(0, tk.END)
        
        # 过滤并显示匹配的包名
        for package in self.package_list:
            if search_text in package.lower():
                self.package_listbox.insert(tk.END, package)
    
    def on_tab_changed(self, event):
        """选项卡切换事件处理"""
        # 获取当前选中的选项卡索引
        current_tab = self.notebook.index(self.notebook.select())
        # 获取所有选项卡的文本
        tab_texts = []
        for i in range(self.notebook.index('end')):
            tab_texts.append(self.notebook.tab(i, 'text'))
        
        # 如果切换到首页选项卡
        if '首页' in tab_texts and tab_texts[current_tab] == '首页':
            # 自动刷新包名列表
            if self.is_connected:
                self.refresh_packages()
    
    def show_package_menu(self, event):
        """显示包名右键菜单"""
        # 获取点击位置的索引
        index = self.package_listbox.nearest(event.y)
        if index >= 0:
            # 选中点击的项
            self.package_listbox.selection_clear(0, tk.END)
            self.package_listbox.selection_set(index)
            # 显示菜单
            self.package_menu.post(event.x_root, event.y_root)
    
    def on_package_double_click(self, event):
        """处理包名双击事件"""
        # 获取双击位置的索引
        index = self.package_listbox.nearest(event.y)
        if index >= 0:
            # 选中点击的项
            self.package_listbox.selection_clear(0, tk.END)
            self.package_listbox.selection_set(index)
            # 显示菜单
            self.show_package_menu(event)
    
    def uninstall_selected_package(self):
        """卸载选中的包"""
        # 获取选中的包名
        selected_indices = self.package_listbox.curselection()
        if not selected_indices:
            self.show_error_dialog("错误", "请先选择要卸载的包")
            return
        
        # 获取包名
        package_name = self.package_listbox.get(selected_indices[0])
        
        # 调用卸载方法
        self.package_var.set(package_name)
        self.uninstall_app()
    
    def copy_package_name(self):
        """复制选中的包名到剪贴板"""
        # 获取选中的包名
        selected_indices = self.package_listbox.curselection()
        if not selected_indices:
            self.show_error_dialog("错误", "请先选择要复制的包名")
            return
        
        # 获取包名
        package_name = self.package_listbox.get(selected_indices[0])
        
        # 复制到剪贴板
        self.root.clipboard_clear()
        self.root.clipboard_append(package_name)
        self.log(f"已复制包名到剪贴板: {package_name}")
        self.show_info_dialog("成功", f"已复制包名到剪贴板: {package_name}")
    
    def auto_refresh_packages_on_start(self):
        """应用启动时自动刷新包名列表"""
        # 检查是否已连接设备
        if self.is_connected:
            self.log("应用启动，自动刷新包名列表...")
            self.refresh_packages()
        else:
            # 如果未连接，延迟一段时间后再次检查
            self.root.after(2000, self._check_connection_and_refresh)
    
    def _check_connection_and_refresh(self):
        """检查连接状态并刷新包名列表"""
        if self.is_connected:
            self.log("设备已连接，自动刷新包名列表...")
            self.refresh_packages()
    
    def create_file_section(self):
        """创建文件管理部分"""
        # 创建文件管理主框架
        file_frame = ttk.LabelFrame(self.file_tab, text="文件管理", padding="10")
        file_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 顶部操作栏
        top_frame = ttk.Frame(file_frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        # 路径输入
        ttk.Label(top_frame, text="设备路径:").pack(side=tk.LEFT, padx=5)
        self.device_path_var = tk.StringVar(value="/storage/emulated/0")
        self.device_path_entry = ttk.Entry(top_frame, textvariable=self.device_path_var)
        self.device_path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        # 绑定回车键事件，当用户按下回车键时刷新文件列表
        self.device_path_entry.bind('<Return>', lambda event: self.refresh_files())
        # 绑定焦点离开事件，当用户输入完成并离开输入框时刷新文件列表
        self.device_path_entry.bind('<FocusOut>', lambda event: self.refresh_files())
        
        # 刷新按钮
        refresh_btn = ttk.Button(top_frame, text="刷新", command=self.refresh_files)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # 文件列表框架
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 文件列表
        self.file_listbox = tk.Listbox(list_frame, 
                                     height=15,
                                     font=('Segoe UI', 10),
                                     borderwidth=1,
                                     relief='solid',
                                     highlightthickness=0)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(list_frame, command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        
        # 为文件列表添加右键菜单
        self.file_listbox.bind('<Button-3>', self.show_file_menu)
        # 为文件列表添加双击事件
        self.file_listbox.bind('<Double-1>', self.on_file_double_click)
        
        # 创建右键菜单
        self.file_menu = tk.Menu(self.root, tearoff=0) # 移除硬编码颜色，交给 sv_ttk 处理主题
        self.file_menu.add_command(label="上传文件", command=self.upload_file)
        self.file_menu.add_command(label="下载文件", command=self.download_file)
        self.file_menu.add_command(label="安装APK", command=self.install_apk_from_file)
        self.file_menu.add_command(label="创建目录", command=self.create_directory)
        self.file_menu.add_command(label="创建文件", command=self.create_file)
        self.file_menu.add_command(label="重命名", command=self.rename_file)
        self.file_menu.add_command(label="删除", command=self.delete_file)
        
        # 底部操作按钮
        bottom_frame = ttk.Frame(file_frame)
        bottom_frame.pack(fill=tk.X, pady=5)
        
        # 上传按钮
        upload_btn = ttk.Button(bottom_frame, text="上传文件", command=self.upload_file)
        upload_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 下载按钮
        download_btn = ttk.Button(bottom_frame, text="下载文件", command=self.download_file)
        download_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 创建目录按钮
        mkdir_btn = ttk.Button(bottom_frame, text="创建目录", command=self.create_directory)
        mkdir_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 创建文件按钮
        create_file_btn = ttk.Button(bottom_frame, text="创建文件", command=self.create_file)
        create_file_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 重命名按钮
        rename_btn = ttk.Button(bottom_frame, text="重命名", command=self.rename_file)
        rename_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 删除按钮
        delete_btn = ttk.Button(bottom_frame, text="删除", command=self.delete_file)
        delete_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 文件数据
        self.file_list = []
    
    def refresh_files(self):
        """刷新设备文件列表"""
        if not self.is_connected:
            self.show_error_dialog("错误", "请先连接设备")
            return
        
        path = self.device_path_var.get().strip()
        if not path:
            self.show_error_dialog("错误", "请输入设备路径")
            return
        
        # 清空列表
        self.file_listbox.delete(0, tk.END)
        self.log(f"正在获取设备文件列表: {path}")
        
        # 在线程中执行ADB命令获取文件列表
        threading.Thread(target=self._refresh_files_thread, args=(path,)).start()
    
    def _refresh_files_thread(self, path):
        """获取文件列表的线程函数"""
        try:
            # 执行ADB命令获取文件列表
            result = subprocess.run(
                [self.adb_path, "shell", "ls", "-la", path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            stdout = result.stdout or ""
            if stdout:
                # 解析文件列表，提取文件类型和文件名
                self.file_list = []
                self.file_types = {}  # 存储文件类型，True为文件夹，False为文件
                
                # 添加返回项
                if self.show_emoji:
                    return_display_name = "⬅️ 返回"
                else:
                    return_display_name = "返回"
                self.file_list.append(return_display_name)
                self.file_types[return_display_name] = True  # 标记为文件夹类型，方便处理
                
                for line in stdout.strip().split('\n'):
                    if line and not line.startswith('total '):
                        parts = line.split()
                        if parts:
                            # 第一个字符表示文件类型，d表示目录
                            is_directory = parts[0].startswith('d')
                            file_name = parts[-1]
                            # 为无后缀文件添加.后缀（仅在不显示emoji时）
                            if not self.show_emoji and not is_directory and '.' not in file_name:
                                base_name = file_name + '.'
                            else:
                                base_name = file_name
                            # 根据设置添加emoji
                            if self.show_emoji:
                                if is_directory:
                                    display_name = f"📁 {base_name}"
                                else:
                                    display_name = f"📄 {base_name}"
                            else:
                                display_name = base_name
                            self.file_list.append(display_name)
                            self.file_types[display_name] = is_directory
                
                # 更新列表框
                self.root.after(0, self._update_file_listbox)
                self.log(f"成功获取文件列表")
            else:
                self.log("未获取到文件信息")
        except Exception as e:
            self.log(f"获取文件列表出错: {str(e)}")
    
    def _update_file_listbox(self):
        """更新文件列表框"""
        self.file_listbox.delete(0, tk.END)
        for file_info in self.file_list:
            self.file_listbox.insert(tk.END, file_info)
    
    def show_file_menu(self, event):
        """显示文件右键菜单"""
        # 获取点击位置的索引
        index = self.file_listbox.nearest(event.y)
        if index >= 0:
            # 选中点击的项
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(index)
            # 显示菜单
            self.file_menu.post(event.x_root, event.y_root)
    
    def on_file_double_click(self, event):
        """处理文件双击事件"""
        # 获取双击位置的索引
        index = self.file_listbox.nearest(event.y)
        if index >= 0:
            # 选中点击的项
            self.file_listbox.selection_clear(0, tk.END)
            self.file_listbox.selection_set(index)
            # 获取文件名
            display_name = self.file_listbox.get(index)
            
            # 检查是否为返回项
            if display_name == "⬅️ 返回" or display_name == "返回":
                # 处理返回上一级目录
                current_path = self.device_path_var.get().strip()
                if current_path and current_path != "/":
                    # 移除路径的最后一部分
                    if current_path.endswith('/'):
                        current_path = current_path[:-1]
                    new_path = '/'.join(current_path.split('/')[:-1])
                    if not new_path:
                        new_path = "/"
                    self.device_path_var.set(new_path)
                    self.refresh_files()
                return
            
            # 检查是否为文件夹
            if display_name in self.file_types and self.file_types[display_name]:
                # 是文件夹，进入该目录
                # 移除emoji，得到真实文件夹名
                if display_name.startswith('📁 '):
                    folder_name = display_name[2:]
                else:
                    folder_name = display_name
                current_path = self.device_path_var.get().strip()
                if current_path.endswith('/'):
                    new_path = current_path + folder_name.rstrip('.')
                else:
                    new_path = current_path + '/' + folder_name.rstrip('.')
                self.device_path_var.set(new_path)
                self.refresh_files()
            else:
                # 是文件，显示菜单
                self.show_file_menu(event)
    
    def upload_file(self):
        """上传文件到设备"""
        if not self.is_connected:
            self.show_error_dialog("错误", "请先连接设备")
            return
        
        # 选择本地文件
        local_file = filedialog.askopenfilename(
            title="选择要上传的文件",
            filetypes=[("所有文件", "*.*")]
        )
        
        if not local_file:
            return
        
        device_path = self.device_path_var.get().strip()
        if not device_path:
            self.show_error_dialog("错误", "请输入设备路径")
            return
        
        # 在线程中执行上传操作
        threading.Thread(target=self._upload_file_thread, args=(local_file, device_path)).start()
    
    def _upload_file_thread(self, local_file, device_path):
        """上传文件的线程函数"""
        try:
            file_name = os.path.basename(local_file)
            device_file = os.path.join(device_path, file_name).replace('\\', '/')
            
            self.log(f"正在上传文件: {local_file} -> {device_file}")
            
            # 执行ADB上传命令
            process = subprocess.Popen(
                [self.adb_path, "push", local_file, device_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # 实时输出上传过程
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                try:
                    decoded_line = line.decode('utf-8', errors='replace').strip()
                    self.log(decoded_line)
                except Exception as decode_error:
                    self.log(f"解码输出时出错: {str(decode_error)}")
            
            process.wait()
            
            if process.returncode == 0:
                self.log(f"文件上传成功: {file_name}")
                self.show_info_dialog("成功", f"文件上传成功: {file_name}")
                # 刷新文件列表
                self.refresh_files()
            else:
                self.log("文件上传失败！")
                self.show_error_dialog("错误", "文件上传失败！")
        except Exception as e:
            self.log(f"上传文件出错: {str(e)}")
            self.show_error_dialog("错误", f"上传文件出错: {str(e)}")
    
    def download_file(self):
        """从设备下载文件"""
        if not self.is_connected:
            self.show_error_dialog("错误", "请先连接设备")
            return
        
        # 获取选中的文件
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            self.show_error_dialog("错误", "请先选择要下载的文件")
            return
        
        # 获取文件名（显示名称）
        display_name = self.file_listbox.get(selected_indices[0])
        # 移除emoji和显示用的.后缀，得到真实文件名
        if display_name.startswith('📁 ') or display_name.startswith('📄 '):
            base_name = display_name[2:]
        else:
            base_name = display_name
        file_name = base_name.rstrip('.')
        
        # 选择保存位置
        local_file = filedialog.asksaveasfilename(
            title="保存文件",
            initialfile=file_name
        )
        
        if not local_file:
            return
        
        device_path = self.device_path_var.get().strip()
        if not device_path:
            self.show_error_dialog("错误", "请输入设备路径")
            return
        
        device_file = os.path.join(device_path, file_name).replace('\\', '/')
        
        # 在线程中执行下载操作
        threading.Thread(target=self._download_file_thread, args=(device_file, local_file)).start()
    
    def _download_file_thread(self, device_file, local_file):
        """下载文件的线程函数"""
        try:
            self.log(f"正在下载文件: {device_file} -> {local_file}")
            
            # 执行ADB下载命令
            process = subprocess.Popen(
                [self.adb_path, "pull", device_file, local_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # 实时输出下载过程
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                try:
                    decoded_line = line.decode('utf-8', errors='replace').strip()
                    self.log(decoded_line)
                except Exception as decode_error:
                    self.log(f"解码输出时出错: {str(decode_error)}")
            
            process.wait()
            
            if process.returncode == 0:
                self.log(f"文件下载成功: {local_file}")
                self.show_info_dialog("成功", f"文件下载成功: {local_file}")
            else:
                self.log("文件下载失败！")
                self.show_error_dialog("错误", "文件下载失败！")
        except Exception as e:
            self.log(f"下载文件出错: {str(e)}")
            self.show_error_dialog("错误", f"下载文件出错: {str(e)}")
    
    def create_directory(self):
        """在设备上创建目录"""
        if not self.is_connected:
            self.show_error_dialog("错误", "请先连接设备")
            return
        
        # 使用自定义对话框获取目录名称
        dir_name = self.ask_string_dialog("创建目录", "请输入目录名称:")
        if not dir_name:
            return
        
        device_path = self.device_path_var.get().strip()
        if not device_path:
            self.show_error_dialog("错误", "请输入设备路径")
            return
        
        new_dir = os.path.join(device_path, dir_name).replace('\\', '/')
        
        # 在线程中执行创建目录操作
        threading.Thread(target=self._create_directory_thread, args=(new_dir,)).start()
    
    def _create_directory_thread(self, new_dir):
        """创建目录的线程函数"""
        try:
            self.log(f"正在创建目录: {new_dir}")
            
            # 执行ADB命令创建目录
            result = subprocess.run(
                [self.adb_path, "shell", "mkdir", "-p", new_dir],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0:
                self.log(f"目录创建成功: {new_dir}")
                self.show_info_dialog("成功", f"目录创建成功: {new_dir}")
                # 刷新文件列表
                self.refresh_files()
            else:
                stderr = result.stderr or ""
                error_msg = stderr or result.stdout
                self.log(f"目录创建失败: {error_msg}")
                self.show_error_dialog("错误", f"目录创建失败: {error_msg}")
        except Exception as e:
            self.log(f"创建目录出错: {str(e)}")
            self.show_error_dialog("错误", f"创建目录出错: {str(e)}")
    
    def delete_file(self):
        """删除设备上的文件或文件夹"""
        if not self.is_connected:
            self.show_error_dialog("错误", "请先连接设备")
            return
        
        # 获取选中的项目
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            self.show_error_dialog("错误", "请先选择要删除的项目")
            return
        
        # 获取项目名称（显示名称）
        display_name = self.file_listbox.get(selected_indices[0])
        
        # 检查是否为返回项
        if display_name == "⬅️ 返回" or display_name == "返回":
            self.show_error_dialog("错误", "无法删除返回项")
            return
        
        # 移除emoji和显示用的.后缀，得到真实名称
        if display_name.startswith('📁 ') or display_name.startswith('📄 '):
            base_name = display_name[2:]
        else:
            base_name = display_name
        item_name = base_name.rstrip('.')
        
        # 检查是否为文件夹
        is_folder = display_name in self.file_types and self.file_types[display_name]
        
        # 确认删除
        if is_folder:
            if not self.ask_yes_no_dialog("确认删除", f"确定要删除文件夹: {item_name} 吗？"):
                return
        else:
            if not self.ask_yes_no_dialog("确认删除", f"确定要删除文件: {item_name} 吗？"):
                return
        
        device_path = self.device_path_var.get().strip()
        if not device_path:
            self.show_error_dialog("错误", "请输入设备路径")
            return
        
        device_item = os.path.join(device_path, item_name).replace('\\', '/')
        
        # 在线程中执行删除操作
        threading.Thread(target=self._delete_file_thread, args=(device_item, is_folder)).start()
    
    def _delete_file_thread(self, device_item, is_folder):
        """删除文件或文件夹的线程函数"""
        try:
            if is_folder:
                self.log(f"正在删除文件夹: {device_item}")
            else:
                self.log(f"正在删除文件: {device_item}")
            
            # 执行ADB命令删除文件或文件夹
            result = subprocess.run(
                [self.adb_path, "shell", "rm", "-rf", device_item],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0:
                if is_folder:
                    self.log(f"文件夹删除成功: {device_item}")
                    self.show_info_dialog("成功", "文件夹删除成功！")
                else:
                    self.log(f"文件删除成功: {device_item}")
                    self.show_info_dialog("成功", "文件删除成功！")
                # 刷新文件列表
                self.refresh_files()
            else:
                stderr = result.stderr or ""
                error_msg = stderr or result.stdout
                if is_folder:
                    self.log(f"文件夹删除失败: {error_msg}")
                    self.show_error_dialog("错误", f"文件夹删除失败: {error_msg}")
                else:
                    self.log(f"文件删除失败: {error_msg}")
                    self.show_error_dialog("错误", f"文件删除失败: {error_msg}")
        except Exception as e:
            if is_folder:
                self.log(f"删除文件夹出错: {str(e)}")
                self.show_error_dialog("错误", f"删除文件夹出错: {str(e)}")
            else:
                self.log(f"删除文件出错: {str(e)}")
                self.show_error_dialog("错误", f"删除文件出错: {str(e)}")
    
    def create_file(self):
        """在设备上创建新文件"""
        if not self.is_connected:
            self.show_error_dialog("错误", "请先连接设备")
            return
        
        # 使用自定义对话框获取文件名
        file_name = self.ask_string_dialog("创建文件", "请输入文件名:")
        if not file_name:
            return
        
        device_path = self.device_path_var.get().strip()
        if not device_path:
            self.show_error_dialog("错误", "请输入设备路径")
            return
        
        new_file = os.path.join(device_path, file_name).replace('\\', '/')
        
        # 在线程中执行创建文件操作
        threading.Thread(target=self._create_file_thread, args=(new_file,)).start()
    
    def _create_file_thread(self, new_file):
        """创建文件的线程函数"""
        try:
            self.log(f"正在创建文件: {new_file}")
            
            # 执行ADB命令创建文件
            result = subprocess.run(
                [self.adb_path, "shell", "touch", new_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0:
                self.log(f"文件创建成功: {new_file}")
                self.show_info_dialog("成功", f"文件创建成功: {new_file}")
                # 刷新文件列表
                self.refresh_files()
            else:
                stderr = result.stderr or ""
                error_msg = stderr or result.stdout
                self.log(f"文件创建失败: {error_msg}")
                self.show_error_dialog("错误", f"文件创建失败: {error_msg}")
        except Exception as e:
            self.log(f"创建文件出错: {str(e)}")
            self.show_error_dialog("错误", f"创建文件出错: {str(e)}")
    
    def rename_file(self):
        """重命名文件或文件夹"""
        if not self.is_connected:
            self.show_error_dialog("错误", "请先连接设备")
            return
        
        # 获取选中的文件
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            self.show_error_dialog("错误", "请先选择要重命名的文件或文件夹")
            return
        
        # 获取文件名（显示名称）
        display_name = self.file_listbox.get(selected_indices[0])
        
        # 检查是否为返回项
        if display_name == "⬅️ 返回" or display_name == "返回":
            self.show_error_dialog("错误", "无法重命名返回项")
            return
        
        # 移除emoji和显示用的.后缀，得到真实文件名
        if display_name.startswith('📁 ') or display_name.startswith('📄 '):
            base_name = display_name[2:]
        else:
            base_name = display_name
        old_file_name = base_name.rstrip('.')
        
        # 使用自定义对话框获取新文件名
        new_file_name = self.ask_string_dialog("重命名", "请输入新文件名:", initialvalue=old_file_name)
        if not new_file_name:
            return
        
        device_path = self.device_path_var.get().strip()
        if not device_path:
            self.show_error_dialog("错误", "请输入设备路径")
            return
        
        old_file = os.path.join(device_path, old_file_name).replace('\\', '/')
        new_file = os.path.join(device_path, new_file_name).replace('\\', '/')
        
        # 在线程中执行重命名操作
        threading.Thread(target=self._rename_file_thread, args=(old_file, new_file)).start()
    
    def _rename_file_thread(self, old_file, new_file):
        """重命名文件的线程函数"""
        try:
            self.log(f"正在重命名文件: {old_file} -> {new_file}")
            
            # 执行ADB命令重命名文件
            result = subprocess.run(
                [self.adb_path, "shell", "mv", old_file, new_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0:
                self.log(f"文件重命名成功: {old_file} -> {new_file}")
                self.show_info_dialog("成功", "文件重命名成功！")
                # 刷新文件列表
                self.refresh_files()
            else:
                stderr = result.stderr or ""
                error_msg = stderr or result.stdout
                self.log(f"文件重命名失败: {error_msg}")
                self.show_error_dialog("错误", f"文件重命名失败: {error_msg}")
        except Exception as e:
            self.log(f"重命名文件出错: {str(e)}")
            self.show_error_dialog("错误", f"重命名文件出错: {str(e)}")
    
    def install_apk_from_file(self):
        """从设备安装APK文件"""
        if not self.is_connected:
            self.show_error_dialog("错误", "请先连接设备")
            return
        
        # 获取选中的文件
        selected_indices = self.file_listbox.curselection()
        if not selected_indices:
            self.show_error_dialog("错误", "请先选择要安装的APK文件")
            return
        
        # 获取文件名（显示名称）
        display_name = self.file_listbox.get(selected_indices[0])
        
        # 检查是否为返回项
        if display_name == "⬅️ 返回" or display_name == "返回":
            self.show_error_dialog("错误", "无法安装返回项")
            return
        
        # 移除emoji和显示用的.后缀，得到真实文件名
        if display_name.startswith('📁 ') or display_name.startswith('📄 '):
            base_name = display_name[2:]
        else:
            base_name = display_name
        file_name = base_name.rstrip('.')
        
        # 检查是否为APK文件
        if not file_name.lower().endswith('.apk'):
            self.show_error_dialog("错误", "请选择APK文件")
            return
        
        device_path = self.device_path_var.get().strip()
        if not device_path:
            self.show_error_dialog("错误", "请输入设备路径")
            return
        
        apk_file = os.path.join(device_path, file_name).replace('\\', '/')
        
        # 在线程中执行安装操作
        threading.Thread(target=self._install_apk_from_file_thread, args=(apk_file,)).start()
    
    def _install_apk_from_file_thread(self, apk_file):
        """从设备安装APK的线程函数"""
        try:
            self.log(f"正在安装APK: {apk_file}")
            
            # 执行ADB安装命令
            process = subprocess.Popen(
                [self.adb_path, "install", apk_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # 实时输出安装过程
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                try:
                    # 尝试使用utf-8解码
                    decoded_line = line.decode('utf-8', errors='replace').strip()
                    self.log(decoded_line)
                except Exception as decode_error:
                    self.log(f"解码输出时出错: {str(decode_error)}")
            
            process.wait()
            
            if process.returncode == 0:
                self.log("APK安装成功！")
                self.show_info_dialog("成功", "APK安装成功！")
            else:
                self.log("APK安装失败！")
                self.show_error_dialog("错误", "APK安装失败！")
        except Exception as e:
            self.log(f"安装出错: {str(e)}")
            self.show_error_dialog("错误", f"安装出错: {str(e)}")
    
    def ask_string_dialog(self, title, prompt, initialvalue=""):
        """自定义输入对话框"""
        # 创建对话框窗口
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("500x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()  # 模态对话框
        
        # 设置背景色
        dialog.configure(bg='SystemWindow') # 使用系统默认窗口背景色，让sv_ttk管理
        
        # 创建框架
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加提示标签
        label = ttk.Label(frame, text=prompt)
        label.pack(pady=(0, 10))
        
        # 添加输入框
        entry_var = tk.StringVar(value=initialvalue)
        entry = ttk.Entry(frame, textvariable=entry_var, width=30)
        entry.pack(pady=(0, 15))
        entry.focus_set()  # 自动获取焦点
        
        # 结果变量
        result = [None]
        
        # 确认按钮回调
        def on_ok():
            result[0] = entry_var.get()
            dialog.destroy()
        
        # 取消按钮回调
        def on_cancel():
            result[0] = None
            dialog.destroy()
        
        # 添加按钮框架
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        # 确认按钮
        ok_button = ttk.Button(button_frame, text="确认", command=on_ok)
        ok_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 取消按钮
        cancel_button = ttk.Button(button_frame, text="取消", command=on_cancel)
        cancel_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # 绑定回车键
        dialog.bind('<Return>', lambda event: on_ok())
        # 绑定ESC键
        dialog.bind('<Escape>', lambda event: on_cancel())
        
        # 等待对话框关闭
        self.root.wait_window(dialog)
        
        return result[0]
    
    def show_info_dialog(self, title, message):
        """自定义信息对话框"""
        # 创建对话框窗口
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x180")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 设置背景色
        dialog.configure(bg='SystemWindow') # 使用系统默认窗口背景色，让sv_ttk管理
        
        # 创建框架
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加消息标签
        label = ttk.Label(frame, text=message, wraplength=260)
        label.pack(pady=10)
        
        # 确定按钮回调
        def on_ok():
            dialog.destroy()
        
        # 添加确定按钮
        ok_button = ttk.Button(frame, text="确定", command=on_ok)
        ok_button.pack(pady=10)
        
        # 绑定回车键和ESC键
        dialog.bind('<Return>', lambda event: on_ok())
        dialog.bind('<Escape>', lambda event: on_ok())
        
        # 等待对话框关闭
        self.root.wait_window(dialog)
    
    def show_error_dialog(self, title, message):
        """自定义错误对话框"""
        # 创建对话框窗口
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x180")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 设置背景色
        dialog.configure(bg='SystemWindow') # 使用系统默认窗口背景色，让sv_ttk管理
        
        # 创建框架
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加消息标签
        label = ttk.Label(frame, text=message, wraplength=260)
        label.pack(pady=10)
        
        # 确定按钮回调
        def on_ok():
            dialog.destroy()
        
        # 添加确定按钮
        ok_button = ttk.Button(frame, text="确定", command=on_ok)
        ok_button.pack(pady=10)
        
        # 绑定回车键和ESC键
        dialog.bind('<Return>', lambda event: on_ok())
        dialog.bind('<Escape>', lambda event: on_ok())
        
        # 等待对话框关闭
        self.root.wait_window(dialog)
    
    def ask_yes_no_dialog(self, title, message):
        """自定义确认对话框"""
        # 创建对话框窗口
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x180")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 设置背景色
        dialog.configure(bg='SystemWindow') # 使用系统默认窗口背景色，让sv_ttk管理
        
        # 创建框架
        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 添加消息标签
        label = ttk.Label(frame, text=message, wraplength=260)
        label.pack(pady=10)
        
        # 结果变量
        result = [False]
        
        # 是按钮回调
        def on_yes():
            result[0] = True
            dialog.destroy()
        
        # 否按钮回调
        def on_no():
            result[0] = False
            dialog.destroy()
        
        # 添加按钮框架
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X)
        
        # 是按钮
        yes_button = ttk.Button(button_frame, text="是", command=on_yes)
        yes_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 否按钮
        no_button = ttk.Button(button_frame, text="否", command=on_no)
        no_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # 绑定回车键和ESC键
        dialog.bind('<Return>', lambda event: on_yes())
        dialog.bind('<Escape>', lambda event: on_no())
        
        # 等待对话框关闭
        self.root.wait_window(dialog)
        
        return result[0]

if __name__ == "__main__":
    root = tk.Tk()
    app = ADBInstaller(root)
    root.mainloop()

