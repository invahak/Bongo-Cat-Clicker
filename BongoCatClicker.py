import os
import sys
import time
import random
import threading
import datetime

try:
    import customtkinter as ctk
    import tkinter as tk
    import tkinter.messagebox as messagebox
    from PIL import ImageGrab, Image
    import pyautogui
    import cv2
    import numpy as np
    import keyboard
    import mss
    from screeninfo import get_monitors
except ImportError as e:
    print(f"Не хватает библиотеки: {e}. Установи всё через pip install -r requirements.txt")
    sys.exit(1)
import ctypes

def resource_path(relative_path):
    """Для корректного поиска файлов и внутри exe, и в разработке"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


APP_CONFIG = {
    "TITLE": "Bongo Cat Clicker v.2 by invahak",
    "WINDOW_SIZE": "470x415",
    "THEME": "dark",
    "FONT": ("Inter", 16, "bold"),
    "MAX_LOG_LINES": 400,
}

TRANSLATIONS = {
    "ru": {
        "header": "Bongo Cat Clicker",
        "pick_click": "Выбрать точку клика",
        "pick_area": "Выбрать область сундука (2 клика)",
        "collapse_hide": "Скрыть логи",
        "collapse_show": "Показать логи",
        "not_chosen": "не выбрана",
        "status_stopped": "Кликер остановлен (F8 — запуск/стоп)",
        "status_work": "Кликер работает (F8 — стоп)",
        "status_error": "Ошибка. Кликер остановлен",
        "point_set": "Точка клика выбрана",
        "area_set": "Область выбрана",
        "choose_click": "Нажми ЛКМ для точки клика",
        "choose_area1": "Сначала выбери ЛЕВЫЙ ВЕРХНИЙ угол",
        "choose_area2": "Теперь ПРАВЫЙ НИЖНИЙ угол",
        "log_ready": "Юи-лог: Готов к работе!",
        "log_no_point": "❌ Точка клика не выбрана!",
        "log_no_area": "❌ Область не выбрана!",
        "log_found": "🟫 Найден сундук по цвету! Клик по ({},{})",
        "log_not_found": "❌ Сундук не найден (по цвету).",
        "log_click": "✅ Клик {} в точку {}",
        "log_stop": "🛑 Кликер остановлен!",
        "log_start": "▶️ Кликер стартовал!",
        "log_error": "❌ Ошибка работы кликера: {}",
        "msg_set_point": "Сначала выбери точку клика и область сундука!",
        "msg_title": "Внимание",
        "label_click_prefix": "Точка клика: ",
        "label_area_prefix": "Область сундука: ",
        "label_area_coords": "Область: ({x1}, {y1}) — ({x2}, {y2})",
        "log_area_set": "🟤 Область сундука: ({x1}, {y1}) — ({x2}, {y2})",
        "log_cancel_click": "❌ Выбор точки отменён",
        "log_cancel_area": "❌ Выбор области отменён",
        "lang_click_mode": "Клик + Поиск сундука",
        "lang_chest_mode": "Поиск сундука",
        "pick_prompt_click": "Кликни ЛКМ — будет точка клика",
        "pick_prompt_area1": "Кликни ЛКМ — ЛЕВЫЙ ВЕРХНИЙ угол",
        "pick_prompt_area2": "Кликни ЛКМ — ПРАВЫЙ НИЖНИЙ угол",
        "pick_overlay_title": "Выбор точки",
        "f8_info": "▶️ Старт/стоп — кнопка F8",
        "log_searching_chest": "🔍 Поиск сундука (по шаблону)…",
        "log_waiting_before_search": "⏳ Ждём 10 секунд перед поиском сундука...",
        "log_grayscale_not_found": "❌ Сундук не найден (совпадение grayscale {score:.2f}).",
        "unknown_mode": "❓ Неизвестный режим: {}",
        "log_point_set": "📍 Точка клика выбрана: {}",
        "log_chest_retry": "❌ Сундук не найден, ждём ещё 10 секунд.",
        "log_click_n": "   🖱️ Клик {n}/3"
    },
    "en": {
        "header": "BongoCat Clicker",
        "pick_click": "Pick click point",
        "pick_area": "Pick chest area (2 clicks)",
        "collapse_hide": "Hide logs",
        "collapse_show": "Show logs",
        "not_chosen": "not chosen",
        "status_stopped": "Clicker stopped (F8 to start/stop)",
        "status_work": "Clicker running (F8 to stop)",
        "status_error": "Error. Clicker stopped",
        "point_set": "Click point set",
        "area_set": "Chest area set",
        "choose_click": "Click LMB to set click point",
        "choose_area1": "First, select the TOP LEFT corner",
        "choose_area2": "Now, select the BOTTOM RIGHT corner",
        "log_ready": "Log: Ready to work!",
        "log_no_point": "❌ Click point not set!",
        "log_no_area": "❌ Area not set!",
        "log_found": "🟫 Chest found at ({},{})!",
        "log_not_found": "❌ Chest not found.",
        "log_click": "✅ Click {} at {}",
        "log_stop": "🛑 Clicker stopped!",
        "log_start": "▶️ Clicker started!",
        "log_error": "❌ Clicker error: {}",
        "msg_set_point": "Set click point and chest area first!",
        "msg_title": "Warning",
        "label_click_prefix": "Click point: ",
        "label_area_prefix": "Chest area: ",
        "label_area_coords": "Area: ({x1}, {y1}) — ({x2}, {y2})",
        "log_area_set": "🟤 Chest area: ({x1}, {y1}) — ({x2}, {y2})",
        "log_cancel_click": "❌ Click selection canceled",
        "log_cancel_area": "❌ Area selection canceled",
        "lang_click_mode": "Click + Chest Search",
        "lang_chest_mode": "Chest Only",
        "pick_prompt_click": "Click LMB — set click point",
        "pick_prompt_area1": "Click LMB — TOP LEFT corner",
        "pick_prompt_area2": "Click LMB — BOTTOM RIGHT corner",
        "pick_overlay_title": "Pick a point",
        "f8_info": "▶️ Start/Stop — press F8",
        "log_searching_chest": "🔍 Searching for chest (template)...",
        "log_waiting_before_search": "⏳ Waiting 10 seconds before chest search...",
        "log_grayscale_not_found": "❌ Chest not found (grayscale match {score:.2f}).",
        "unknown_mode": "❓ Unknown mode: {}",
        "log_point_set": "📍 Click point set: {}",
        "log_chest_retry": "❌ Chest not found, waiting 10 more seconds.",
        "log_click_n": "   🖱️ Click {n}/3"
    }
}

# --- SendInput wrapper ("human" click) ---
SendInput = ctypes.windll.user32.SendInput
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.c_ulonglong),  # ULONG_PTR
    ]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]

    _anonymous_ = ("u",)
    _fields_ = [("type", ctypes.c_ulong), ("u", _INPUT)]

def send_click_human():
    down = INPUT(type=0, mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, 0))
    up = INPUT(type=0, mi=MOUSEINPUT(0, 0, 0, MOUSEEVENTF_LEFTUP, 0, 0))
    SendInput(1, ctypes.byref(down), ctypes.sizeof(INPUT))
    time.sleep(random.uniform(0.015, 0.03))
    SendInput(1, ctypes.byref(up), ctypes.sizeof(INPUT))

# --- Logger (thread‑safe) ---
class Logger:
    def __init__(self, textbox, max_lines=400):
        self.textbox = textbox
        self.max_lines = max_lines

    def _write(self, msg):
        self.textbox.configure(state="normal")
        lines = self.textbox.get("1.0", "end-1c").split("\n")
        if len(lines) > self.max_lines:
            self.textbox.delete("1.0", str(len(lines) - self.max_lines) + ".0")
        self.textbox.insert("end", msg + "\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def log(self, msg):
        # Гарантируем вызов в GUI‑потоке
        try:
            self.textbox.after(0, self._write, msg)
        except RuntimeError:
            # окно закрыто
            pass

# --- Clicker Engine ---
class ClickerEngine:
    def __init__(self, logger, update_status, get_app_state, get_mode, color_range=((30, 20, 25), (140, 110, 95))):
        self.strings = TRANSLATIONS["ru"]  # дефолт
        self.logger = logger
        self.update_status = update_status
        self.get_app_state = get_app_state
        self.get_mode = get_mode
        self.color_range = color_range
        self.running_event = threading.Event()

        self.chest_templates = []
        for fname in ('chest1.png', 'chest2.png'):
            tpl = cv2.imread(resource_path(fname), cv2.IMREAD_UNCHANGED)
            if tpl is None:
                raise RuntimeError(f"Не найден файл шаблона {fname}! Поместите {fname} рядом со скриптом.")
            # приведение к BGR (как было в исходном коде)
            if len(tpl.shape) == 3:
                if tpl.shape[2] == 4:
                    tpl = cv2.cvtColor(tpl, cv2.COLOR_BGRA2BGR)
                elif tpl.shape[2] == 1:
                    tpl = cv2.cvtColor(tpl, cv2.COLOR_GRAY2BGR)
            elif len(tpl.shape) == 2:
                tpl = cv2.cvtColor(tpl, cv2.COLOR_GRAY2BGR)
            # сохраняем кортеж (шаблон, ширина, высота)
            self.chest_templates.append((tpl, tpl.shape[1], tpl.shape[0]))

    def start(self):
        if self.running_event.is_set():
            return
        self.running_event.set()
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running_event.clear()

    def _loop(self):
        self.update_status(self.strings["status_work"])
        self.logger.log(self.strings["log_start"])
        i = 0
        while self.running_event.is_set():
            mode = self.get_mode()
            app_state = self.get_app_state()
            if mode == "normal":
                i += 1
                # Стандартное поведение: кликать, раз в 50 искать сундук
                if i % 50 == 0 and app_state["search_area"]:
                    self.logger.log(self.strings["log_searching_chest"])
                    self.find_and_click_chest(app_state["search_area"])
                if app_state["click_point"]:
                    try:
                        pyautogui.moveTo(*app_state["click_point"])
                        send_click_human()
                        self.logger.log(self.strings["log_click"].format(i, app_state["click_point"]))
                    except Exception as e:
                        self.logger.log(self.strings["log_error"].format(e))
                else:
                    self.logger.log(self.strings["log_no_point"])
                    break
                time.sleep(random.uniform(0.08, 0.15))
            elif mode == "chest_only":
                self.logger.log(self.strings["log_waiting_before_search"])
                for _ in range(10):
                    if not self.running_event.is_set():
                        break  # выход сразу, если нажали F8
                    time.sleep(1)
                if not self.running_event.is_set():
                    break
                app_state = self.get_app_state()
                if app_state["search_area"]:
                    found = self.find_and_click_chest(app_state["search_area"])
                    if not found:
                        self.logger.log(self.strings["log_chest_retry"])
                else:
                    self.logger.log(self.strings["log_no_area"])

            else:
                self.logger.log(self.strings["unknown_mode"].format(mode))
                break
        self.running_event.clear()
        self.update_status(self.strings["status_stopped"])
        self.logger.log(self.strings["log_stop"])

    def find_and_click_chest(self, area):
        try:
            x1, y1, x2, y2 = area
            width = x2 - x1
            height = y2 - y1

            with mss.mss() as sct:
                monitor = {"left": x1, "top": y1, "width": width, "height": height}
                sct_img = sct.grab(monitor)
                screenshot_cv = np.array(sct_img)[..., :3]  # BGR

            screenshot_gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)

            # пройти по шаблонам в порядке приоритета (chest1 -> chest2)
            for tpl, tpl_w, tpl_h in self.chest_templates:
                tpl_gray = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
                res = cv2.matchTemplate(screenshot_gray, tpl_gray, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)

                if max_val >= 0.7:  # порог совпадения можно настроить
                    center_x = x1 + max_loc[0] + tpl_w // 2
                    center_y = y1 + max_loc[1] + tpl_h // 2
                    self.logger.log(f"Найден шаблон сундука (score={max_val:.2f}) по центру ({center_x},{center_y})")
                    pyautogui.moveTo(center_x, center_y)
                    for n in range(3):
                        send_click_human()
                        self.logger.log(self.strings["log_click_n"].format(n=n + 1))
                        time.sleep(1)
                    return True
                # если не найден — продолжаем к следующему шаблону

            # ни по одному шаблону не попали
            self.logger.log(self.strings["log_grayscale_not_found"].format(score=max_val if 'max_val' in locals() else 0.0))
            return False
        except Exception as e:
            self.logger.log(self.strings["log_error"].format(e))
            return False

# --- Основное приложение ---
class ClickerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.language = tk.StringVar(value="ru")  # текущий язык
        self.strings = TRANSLATIONS[self.language.get()]
        

        self.title(APP_CONFIG["TITLE"])
        self.geometry(APP_CONFIG["WINDOW_SIZE"])
        self.resizable(False, False)
        ctk.set_appearance_mode(APP_CONFIG["THEME"])

        self.app_state = {"search_area": None, "click_point": None}

        # --- Вот тут ДО _build_ui! ---
        self.mode_var = tk.BooleanVar(value=False)

        self._build_ui()
        self.engine = ClickerEngine(
            logger=self.logger,
            update_status=self.set_status,
            get_app_state=self.get_app_state,
            get_mode=lambda: "chest_only" if self.mode_var.get() else "normal",
            color_range=((30, 20, 25), (140, 110, 95)),
        )
        self.engine.strings = self.strings
        keyboard.add_hotkey("f8", self.toggle_clicker)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
    def update_ui_texts(self):
        self.header.configure(text=self.strings["header"])
        self.btn_pick_click.configure(text=self.strings["pick_click"])
        self.btn_pick_area.configure(text=self.strings["pick_area"])
        self.btn_collapse.configure(text=self.strings["collapse_hide"])
        self.label_click_point.configure(text=f"{self.strings['pick_click']}: {self.strings['not_chosen']}")
        self.label_area.configure(text=f"{self.strings['pick_area']}: {self.strings['not_chosen']}")
        self.status_bar.configure(text=self.strings["status_stopped"])
        self.label_left.configure(text=self.strings["lang_click_mode"])
        self.label_right.configure(text=self.strings["lang_chest_mode"])
        self.f8_info.configure(text=self.strings["f8_info"])



    def set_language(self, lang_code):
        self.language.set(lang_code)
        self.strings = TRANSLATIONS[lang_code]
        self.engine.strings = self.strings  # <-- передай и в ClickerEngine
        self.update_ui_texts()  # обновить кнопки, лейблы и статус

    # --- UI helpers ---
    def _build_ui(self):
        self.header = ctk.CTkLabel(self, text=self.strings["header"], font=("Inter", 22, "bold"), text_color="#a78bfa")
        lang_frame = ctk.CTkFrame(self)
        lang_frame.pack()
        ctk.CTkButton(lang_frame, text="RU", command=lambda: self.set_language("ru")).pack(side="left", padx=4)
        ctk.CTkButton(lang_frame, text="EN", command=lambda: self.set_language("en")).pack(side="left", padx=4)

        self.header.pack(pady=(16, 5))

        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", pady=(4, 6))

# Новый стиль: Switch
        mode_frame = ctk.CTkFrame(self)
        mode_frame.pack(fill="x", padx=16, pady=(0, 2))

        mode_frame.columnconfigure((0, 1, 2), weight=1)  # 3 колонки, растягиваются

        self.label_left = ctk.CTkLabel(
            mode_frame,
            text=self.strings["lang_click_mode"],
            font=("Inter", 13),
            text_color="#c7d2fe"
        )
        self.label_left.grid(row=0, column=0, sticky="e", padx=(4, 4))

        self.mode_switch = ctk.CTkSwitch(
            mode_frame,
            text="",
            variable=self.mode_var,
            onvalue=True, offvalue=False,
            width=40
        )
        self.mode_switch.grid(row=0, column=1, padx=(4, 4))

        self.label_right = ctk.CTkLabel(
            mode_frame,
            text=self.strings["lang_chest_mode"],
            font=("Inter", 13),
            text_color="#c7d2fe"
        )
        self.label_right.grid(row=0, column=2, sticky="w", padx=(4, 4))


        self.btn_pick_click = ctk.CTkButton(
            btn_frame,
            text=self.strings["pick_click"],
            command=self.pick_click_point,
            font=APP_CONFIG["FONT"],
            fg_color="#27272a",
            hover_color="#57534e",
            corner_radius=16,
        )
        self.btn_pick_click.pack(fill="x", padx=16, pady=(4, 2))

        self.btn_pick_area = ctk.CTkButton(
            btn_frame,
            text=self.strings["pick_area"],
            command=self.pick_search_area,
            font=APP_CONFIG["FONT"],
            fg_color="#27272a",
            hover_color="#57534e",
            corner_radius=16,
        )
        self.btn_pick_area.pack(fill="x", padx=16, pady=(2, 4))

        self.f8_info = ctk.CTkLabel(self, text=self.strings["f8_info"], font=("Inter", 14, "bold"), text_color="#fde047")
        self.f8_info.pack(pady=(0, 2))

        self.btn_collapse = ctk.CTkButton(
            self,
            text=self.strings["collapse_hide"],
            command=self.toggle_logs,
            width=120,
            fg_color="#334155",
            text_color="#f8fafc",
            corner_radius=14,
            font=("Inter", 12, "bold"),
        )
        self.btn_collapse.pack(pady=(2, 2))

        info_frame = ctk.CTkFrame(self)
        info_frame.pack(fill="x", padx=10)

        self.label_click_point = ctk.CTkLabel(
            info_frame,
            text=f"Точка клика: {self.strings['not_chosen']}",
            font=("Inter", 12),
            text_color="#c7d2fe",
        )
        self.label_click_point.pack(side="left", padx=(5, 6), pady=2)

        self.label_area = ctk.CTkLabel(
            info_frame,
            text=f"Область сундука: {self.strings['not_chosen']}",
            font=("Inter", 12),
            text_color="#fde68a",
        )
        self.label_area.pack(side="right", padx=(6, 5), pady=2)

        self.status_bar = ctk.CTkLabel(self, text=self.strings["status_stopped"], font=("Inter", 14, "bold"), text_color="#ef4444")
        self.status_bar.pack(fill="x", padx=8, pady=(1, 6))

        self.log_collapsed = False
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.pack(fill="both", padx=15, pady=(0, 10), expand=True)

        self.log_box = ctk.CTkTextbox(
            self.log_frame,
            height=7,
            font=("Consolas", 11),
            fg_color="#27272a",
            text_color="#f8fafc",
            wrap="word",
            corner_radius=12,
        )
        self.log_box.pack(fill="both", expand=True)

        self.logger = Logger(self.log_box, APP_CONFIG["MAX_LOG_LINES"])
        self.logger.log(self.strings["log_ready"])

    # --- UI actions ---
    def toggle_logs(self):
        self.log_collapsed = not self.log_collapsed
        if self.log_collapsed:
            self.log_frame.pack_forget()
            self.btn_collapse.configure(text=self.strings["collapse_show"])
        else:
            self.log_frame.pack(fill="both", padx=15, pady=(0, 10), expand=True)
            self.btn_collapse.configure(text=self.strings["collapse_hide"])

    def pick_point_with_overlay(self, callback, prompt):
        monitors = get_monitors()
        overlays = []
        point = {"pos": None}

        def on_click(event):
            x, y = event.x_root, event.y_root
            point["pos"] = (x, y)
            for o in overlays:
                try:
                    o.grab_release()
                    o.destroy()
                except Exception:
                    pass
            callback((x, y))

        def on_close():
            for o in overlays:
                try:
                    o.grab_release()
                    o.destroy()
                except Exception:
                    pass
            callback(None)

        for mon in monitors:
            overlay = ctk.CTkToplevel(self)
            overlay.geometry(f"{mon.width}x{mon.height}+{mon.x}+{mon.y}")
            overlay.attributes("-alpha", 0.35)
            overlay.configure(bg="black")
            overlay.title(self.strings["pick_overlay_title"])
            overlay.protocol("WM_DELETE_WINDOW", on_close)
            label = ctk.CTkLabel(overlay, text=prompt, font=("Inter", 22, "bold"), text_color="white", fg_color="black")
            label.pack(expand=True)
            overlay.bind("<Button-1>", on_click)
            overlay.focus_set()
            overlay.grab_set()
            overlays.append(overlay)

        self.wait_window(overlays[0])

    def pick_click_point(self):
        self.set_status(self.strings["choose_click"], "#0ea5e9")

        def callback(pos):
            if pos is None:
                self.set_status(self.strings["status_stopped"], "#ef4444")
                self.logger.log(self.strings["log_cancel_click"])
                return
            self.app_state["click_point"] = pos
            self.label_click_point.configure(text=f"{self.strings['label_click_prefix']}{pos}")
            self.set_status(self.strings["point_set"], "#16a34a")
            self.logger.log(self.strings["log_point_set"].format(pos))
        self.pick_point_with_overlay(callback, self.strings["pick_prompt_click"])

    def pick_search_area(self):
        self.set_status(self.strings['choose_area1'], "#f59e42")
        def pick_first(pos1):
            if pos1 is None:
                self.set_status(self.strings["status_stopped"], "#ef4444")
                self.logger.log(self.strings["log_cancel_area"])
                return
            self.set_status(self.strings['choose_area2'], "#eab308")
            def pick_second(pos2):
                if pos2 is None:
                    self.set_status(self.strings["status_stopped"], "#ef4444")
                    self.logger.log(self.strings["log_cancel_area"])
                    return
                x1, y1 = pos1
                x2, y2 = pos2
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)
                self.app_state['search_area'] = (x1, y1, x2, y2)
                self.label_area.configure(text=self.strings["label_area_coords"].format(x1=x1, y1=y1, x2=x2, y2=y2))
                self.set_status(self.strings['area_set'], "#fde68a")
                self.logger.log(self.strings["log_area_set"].format(x1=x1, y1=y1, x2=x2, y2=y2))
            self.pick_point_with_overlay(pick_second, self.strings["pick_prompt_area2"])
        self.pick_point_with_overlay(pick_first, self.strings["pick_prompt_area1"])

    def toggle_clicker(self, event=None):
        if getattr(self.engine, 'running_event', None) and self.engine.running_event.is_set():
            self.engine.stop()
        else:
            if not self.app_state['click_point'] or not self.app_state['search_area']:
                self.show_info(self.strings['msg_set_point'], self.strings['msg_title'])
                return
            self.engine.start()

    def set_status(self, text, color=None):
        self.status_bar.configure(text=text)
        if color:
            self.status_bar.configure(text_color=color)

    def get_app_state(self):
        return self.app_state

    def show_info(self, msg, header):
        tk.messagebox.showinfo(header, msg)

    def _on_close(self):
        try:
            self.engine.stop()
        except Exception:
            pass
        self.destroy()

if __name__ == "__main__":
    try:
        app = ClickerApp()
        app.mainloop()
    except Exception as e:
        import traceback
        print("=== ОШИБКА ===")
        traceback.print_exc()
        