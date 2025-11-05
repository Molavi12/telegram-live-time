from telethon import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
import asyncio
from datetime import datetime, timedelta
import pytz
import jdatetime
import logging

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LiveClockBot:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('live_clock_session', api_id, api_hash)
        self.tehran_tz = pytz.timezone('Asia/Tehran')
        
    def get_current_time(self):
        """دریافت زمان فعلی تهران"""
        tehran_time = datetime.now(self.tehran_tz)
        return tehran_time.strftime("%H:%M")
    
    def get_days_until_bahman(self):
        """محاسبه روزهای باقیمانده تا دوم بهمن"""
        now = jdatetime.datetime.now()
        
        # تعیین سال - اگر الان بعد از بهمن هستیم، سال بعد را در نظر می‌گیریم
        if now.month > 11 or (now.month == 11 and now.day > 2):
            target_year = now.year + 1
        else:
            target_year = now.year
            
        target_date = jdatetime.datetime(target_year, 11, 2)  # 11 = Bahman
        days_left = (target_date - now).days
        
        return days_left
    
    def get_first_name(self):
        """تولید نام اصلی اکانت"""
        current_time = self.get_current_time()
        return f"{current_time} +این مجموعه استیکر که هر دقیقه همراه ساعت تغییر می‌کند 🏓🥇دقیقه بعدی🥈دقیقه بعدی 🥉"
    
    def get_bio(self):
        """تولید بیوگرافی"""
        days_left = self.get_days_until_bahman()
        return f"⏳ زمان باقیمانده تا دوم بهمن: {days_left} روز"
    
    async def update_profile(self):
        """بروزرسانی پروفایل"""
        try:
            first_name = self.get_first_name()
            bio = self.get_bio()
            
            await self.client(UpdateProfileRequest(
                first_name=first_name,
                about=bio
            ))
            
            logger.info(f"✅ پروفایل بروزرسانی شد - زمان: {self.get_current_time()}")
            
        except Exception as e:
            logger.error(f"❌ خطا در بروزرسانی پروفایل: {e}")
    
    async def run(self):
        """اجرای اصلی ربات"""
        await self.client.start(phone=self.phone_number)
        logger.info("🚀 ربات ساعت زنده فعال شد!")
        
        while True:
            try:
                await self.update_profile()
                # انتظار 60 ثانیه برای بروزرسانی بعدی
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"❌ خطا در اجرای اصلی: {e}")
                await asyncio.sleep(30)  # در صورت خطا 30 ثانیه صبر کن

# تنظیمات شما
API_ID = 26600960
API_HASH = '73746434553a3b392291b51a49cd41fc'
PHONE_NUMBER = '+989929903206'

async def main():
    bot = LiveClockBot(API_ID, API_HASH, PHONE_NUMBER)
    await bot.run()

if __name__ == '__main__':
    asyncio.run(main())
