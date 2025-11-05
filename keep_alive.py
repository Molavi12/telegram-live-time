import subprocess
import time
import sys

def main():
    while True:
        try:
            print("🚀 شروع ربات ساعت زنده...")
            # اجرای ربات
            process = subprocess.Popen([sys.executable, "live_clock_bot.py"])
            
            # منتظر ماندن تا پروسه تمام شود
            process.wait()
            
        except Exception as e:
            print(f"❌ خطا: {e}")
        
        print("🔄 راه‌اندازی مجدد در 10 ثانیه...")
        time.sleep(10)

if __name__ == "__main__":
    main()
