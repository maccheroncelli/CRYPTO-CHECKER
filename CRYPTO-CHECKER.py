# CUSTOMTKINTER VERSION OF CRYPTO CHECKER

import json
import os
import re
import subprocess
import ctypes
import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import winreg

SITE_FILE = "sites.json"

def is_bitcoin_address(value):
    return re.match(r'^(bc1([ac-hj-np-z02-9]{6,87})|[13][a-km-zA-HJ-NP-Z1-9]{25,34})$', value, re.IGNORECASE)

def is_hex_address(value):
    return re.match(r'^0x[a-fA-F0-9]{40}$', value)

def is_tron_address(value):
    return re.match(r'^T[0-9a-zA-Z]{33}$', value)

VALIDATOR_MAP = {
    "is_bitcoin_address": is_bitcoin_address,
    "is_hex_address": is_hex_address,
    "is_tron_address": is_tron_address
}

def load_sites():
    if not os.path.exists(SITE_FILE):
        return {}
    with open(SITE_FILE, "r") as f:
        return json.load(f)

def save_sites(data):
    with open(SITE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_default_browser_progid():
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice"
        ) as key:
            prog_id, _ = winreg.QueryValueEx(key, "ProgId")
            return prog_id
    except Exception as e:
        print(f"Registry lookup failed: {e}")
        return None

def get_browser_path_from_progid(prog_id):
    progid_to_path = {
        "ChromeHTML": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "FirefoxURL": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        "MSEdgeHTM": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
    }
    return progid_to_path.get(prog_id)

class BlockchainHandler:
    def __init__(self, name, validator_keys, url_templates):
        self.name = name
        self.validators = [VALIDATOR_MAP[k] for k in validator_keys if k in VALIDATOR_MAP]
        self.url_templates = url_templates

    def matches(self, value):
        return any(v(value) for v in self.validators)

    def build_urls(self, value):
        return [(label, url.format(value=value)) for label, url in self.url_templates.items()]

from tkinter import StringVar

class CryptoCheckerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Checker")
        self.geometry("250x540")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        self.sites_config = load_sites()
        self.handlers = [
            BlockchainHandler(name, data.get("validators", []), data.get("urls", {}))
            for name, data in self.sites_config.items()
        ]

        self.current_handler_name = None
        self.current_urls = []
        self.check_vars = []
        self.checked_state_memory = self.load_checked_state_memory()

        self.entry = ctk.CTkEntry(self, width=200, placeholder_text="Enter address or TXID")
        self.entry.pack(pady=12)
        self.entry.bind("<Return>", lambda e: self.detect_and_display())

        self.detect_button = ctk.CTkButton(self, text="Detect Type", command=self.detect_and_display)
        self.detect_button.pack(pady=6)

        self.type_label = ctk.CTkLabel(self, text="", text_color="skyblue", wraplength=180, justify="left", font=ctk.CTkFont(size=12))
        self.type_label.pack(pady=6)

        self.checkbox_frame = ctk.CTkScrollableFrame(self)
        self.checkbox_frame.pack(pady=10, fill="both", expand=False, padx=10)

        self.open_button = ctk.CTkButton(self, text="Open Selected Sites", command=self.open_selected)
        self.open_button.pack(pady=4)

        self.add_site_button = ctk.CTkButton(self, text="Add Site", command=self.add_site)
        self.add_site_button.pack(pady=4)
        
        self.language_var = StringVar(value="English")
        self.language_dropdown = ctk.CTkOptionMenu(self, values=["English", "Vietnamese", "Thai", "Lao", "Khmer", "Arabic"], variable=self.language_var, command=self.update_language)
        self.language_dropdown.pack(pady=4)

    def detect_and_display(self):
        value = self.entry.get().strip()
        self.type_label.configure(text="")
        self.clear_checkboxes()

        for handler in self.handlers:
            if handler.matches(value):
                self.current_handler_name = handler.name
                urls = handler.build_urls(value)
                # Move Google and Chainabuse to the end
                special_labels = ["Google Search", "Chainabuse"]
                prioritized = [item for item in urls if item[0] not in special_labels]
                deprioritized = [item for item in urls if item[0] in special_labels]
                self.current_urls = prioritized + deprioritized
                print(f"Matched handler: {handler.name}")
                print(f"Generated URLs: {self.current_urls}")

                if handler.name == "Hexadecimal":
                    hex_note = {
                                "English": "Detected: Hexadecimal address\nNote: These addresses are used across multiple blockchains,\nFurther research is recommended to confirm ownership and purpose.",
                                "Vietnamese": "Đã phát hiện: địa chỉ dạng Hex\nLưu ý: Các địa chỉ này được dùng trên nhiều blockchain khác nhau.\nCần nghiên cứu thêm để xác định mục đích.",
                                "Thai": "ตรวจพบ: ที่อยู่เลขฐานสิบหก\nที่อยู่เหล่านี้ใช้ในหลายบล็อกเชน\nโปรดศึกษาข้อมูลเพิ่มเติมเพื่อระบุวัตถุประสงค์.",
                                "Lao": "ພົບ: ທີ່ຢູ່ແບບ Hex\nແມ່ນຖືກໃຊ້ໃນຫຼາຍ Blockchain\nຄວນຄົ້ນຄວ້າເພີ່ມເຕີມເພື່ອກຳນົດຄວາມໝາຍ.",
                                "Khmer": "បានរកឃើញ៖ អាសយដ្ឋាន Hexadecimal\nអាសយដ្ឋានទាំងនេះត្រូវបានប្រើលើ blockchain ច្រើន\nសូមស្វែងរកបន្ថែមដើម្បីយល់អំពីគោលបំណង។",
                                "Arabic": "تم الكشف: عنوان سداسي عشري\nتُستخدم هذه العناوين عبر العديد من شبكات البلوكتشين،\nيُنصح بإجراء مزيد من البحث لتحديد الغرض والاستخدام."}
                    message = hex_note.get(self.language_var.get(), hex_note["English"])
                    self.type_label.configure(
                        text=message,
                        text_color="red",
                        wraplength=180,
                        font=ctk.CTkFont(size=12),
                        justify="center"
                    )
                        
                else:
                    self.type_label.configure(text=f"Detected: {handler.name} address", text_color="red", font=ctk.CTkFont(size=12, weight="bold"))
                    self.render_checkboxes()
                return

        self.current_handler_name = "TXID"
        tx_urls = self.sites_config.get("TXID", {}).get("urls", {})
        self.current_urls = [(label, url.format(value=value)) for label, url in tx_urls.items()]
        self.type_label.configure(text="No address match — treating as TXID", text_color="red")
        self.render_checkboxes()

    def wrap_text(self, text, max_length=25):
        return "".join([text[i:i+max_length] for i in range(0, len(text), max_length)])

    def render_checkboxes(self):
        self.checked_state_memory.setdefault(self.current_handler_name, {})
        self.clear_checkboxes()
        for label, url in self.current_urls:
            var = tk.BooleanVar()
            if label in self.checked_state_memory[self.current_handler_name]:
                var.set(self.checked_state_memory[self.current_handler_name][label])
            default_checked = label not in ["Chainabuse", "Google Search"]
            if self.current_handler_name == "Hexadecimal":
                default_checked = label in ["Etherscan", "Tokenview", "Blockscan"]
            elif self.current_handler_name == "Bitcoin":
                default_checked = label not in ["Chainabuse", "Google Search"]
            var.set(self.checked_state_memory[self.current_handler_name].get(label, default_checked))

            row = ctk.CTkFrame(self.checkbox_frame)
            row.pack(fill="x", pady=2, padx=10)

            wrapped_label = self.wrap_text(label, max_length=25)
            chk = ctk.CTkCheckBox(row, text=wrapped_label, variable=var)
            chk.pack(side="left")

            del_btn = ctk.CTkButton(row, text="✖", width=20, fg_color="red", hover_color="darkred", command=lambda l=label: self.delete_site(l))
            del_btn.pack(side="right", padx=(10, 0))

            self.check_vars.append((label, var, url))
            var.trace_add("write", lambda *args, l=label, v=var: self.checked_state_memory[self.current_handler_name].update({l: v.get()}))

    def save_checked_state_memory(self):
        try:
            with open("checked_memory.json", "w") as f:
                json.dump(self.checked_state_memory, f, indent=2)
        except Exception as e:
            print(f"Failed to save checked memory: {e}")

    def load_checked_state_memory(self):
        try:
            if os.path.exists("checked_memory.json"):
                with open("checked_memory.json", "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"Failed to load checked memory: {e}")
        return {}  # fallback

    def clear_checkboxes(self):
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()
        self.check_vars.clear()

    def open_selected(self):
        selected_urls = [url for _, var, url in self.check_vars if var.get()]
        if not selected_urls:
            messagebox.showwarning("No sites selected", "Please select at least one website.")
            return

        if os.name == "nt":
            self.launch_browser_new_window(selected_urls)
        elif os.name == "posix":
            for url in selected_urls:
                subprocess.Popen(['xdg-open', url])
        else:
            messagebox.showinfo("Unsupported", "Unsupported platform.")

    def launch_browser_new_window(self, urls):
        progid = get_default_browser_progid()
        path = get_browser_path_from_progid(progid)

        if path and os.path.exists(path):
            try:
                subprocess.Popen([path, "--new-window"] + urls)
                return
            except Exception as e:
                print(f"Failed to open browser: {e}")

        messagebox.showerror("Browser not found", f"Could not launch default browser: {progid}")

    def add_site(self):
        if not self.current_handler_name:
            messagebox.showinfo("Info", "Please detect a type first.")
            return

        site_data = self.sites_config.setdefault(self.current_handler_name, {}).setdefault("urls", {})
        label_dialog = ctk.CTkInputDialog(text="Enter site label", title="Add Site")
        label = label_dialog.get_input()

        url_dialog = ctk.CTkInputDialog(text="Enter site URL (use {value})", title="Add Site")
        url = url_dialog.get_input()
        if label and url and "{value}" in url:
            site_data[label] = url
            save_sites(self.sites_config)
            self.handlers = [
                BlockchainHandler(name, data.get("validators", []), data.get("urls", {}))
                for name, data in self.sites_config.items()
            ]
            self.detect_and_display()
        else:
            messagebox.showwarning("Invalid", "URL must contain '{value}'.")

    def on_closing(self):
        self.save_checked_state_memory()
        self.destroy()

    def update_language(self, lang):
        translations = {
            "English": {
                "detect_type": "Detect Type",
                "open_selected": "Open Selected Sites",
                "add_site": "Add Site",
                "info": "Please detect a type first.",
                "invalid": "URL must contain '{value}'.",
                "no_selection": "Please select at least one website.",
                "unsupported": "Unsupported platform."
            },
            "Vietnamese": {
                "detect_type": "Phát hiện loại",
                "open_selected": "Mở các trang đã chọn",
                "add_site": "Thêm trang",
                "info": "Vui lòng phát hiện loại trước.",
                "invalid": "URL phải chứa '{value}'.",
                "no_selection": "Vui lòng chọn ít nhất một trang web.",
                "unsupported": "Nền tảng không được hỗ trợ."
            },
            "Thai": {
                "detect_type": "ตรวจหาประเภท",
                "open_selected": "เปิดเว็บไซต์ที่เลือก",
                "add_site": "เพิ่มเว็บไซต์",
                "info": "กรุณาตรวจหาประเภทก่อน",
                "invalid": "URL ต้องมี '{value}'",
                "no_selection": "กรุณาเลือกอย่างน้อยหนึ่งเว็บไซต์",
                "unsupported": "ไม่รองรับแพลตฟอร์ม"
            },
            "Lao": {
                "detect_type": "ກວດພົບປະເພດ",
                "open_selected": "ເປີດເວັບໄຊທີ່ເລືອກ",
                "add_site": "ເພີ່ມເວັບໄຊທ໌",
                "info": "ກະລຸນາກວດພົບປະເພດກ່ອນ",
                "invalid": "URL ຕ້ອງມີ '{value}'",
                "no_selection": "ກະລຸນາເລືອກເວັບໄຊທ໌ຢ່າງໜ້ອຍໜຶ່ງ",
                "unsupported": "ບໍ່ຮອງຮັບແພລດຟອມ"
            },
            "Khmer": {
                "detect_type": "រកឃើញប្រភេទ",
                "open_selected": "បើកគេហទំព័រដែលបានជ្រើស",
                "add_site": "បន្ថែមគេហទំព័រ",
                "info": "សូមរកឃើញប្រភេទជាមុន",
                "invalid": "URL ត្រូវមាន '{value}'",
                "no_selection": "សូមជ្រើសរើសយ៉ាងហោចណាស់មួយគេហទំព័រ",
                "unsupported": "មិនគាំទ្រផ្នែករឹងនេះទេ"
            },
            "Arabic": {
                "detect_type": "تحديد النوع",
                "open_selected": "فتح المواقع المحددة",
                "add_site": "إضافة موقع",
                "info": "يرجى تحديد النوع أولاً.",
                "invalid": "يجب أن يحتوي الرابط على '{value}'",
                "no_selection": "يرجى تحديد موقع واحد على الأقل.",
                "unsupported": "النظام غير مدعوم."
            },
                "no_selection": "សូមជ្រើសរើសយ៉ាងហោចណាស់មួយគេហទំព័រ",
                "unsupported": "មិនគាំទ្រផ្នែករឹងនេះទេ"
            }
        
        t = translations.get(lang, translations["English"])
        self.detect_button.configure(text=t["detect_type"])
        self.open_button.configure(text=t["open_selected"])
        self.add_site_button.configure(text=t["add_site"])
        self.texts = t

    def delete_site(self, label):
        site_data = self.sites_config.get(self.current_handler_name, {}).get("urls", {})
        if label in site_data and messagebox.askyesno("Confirm", f"Delete '{label}'?"):
            del site_data[label]
            save_sites(self.sites_config)
            self.handlers = [
                BlockchainHandler(name, data.get("validators", []), data.get("urls", {}))
                for name, data in self.sites_config.items()
            ]
            self.detect_and_display()

if __name__ == "__main__":
    app = CryptoCheckerGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
