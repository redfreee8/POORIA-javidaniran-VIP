import requests
import base64
import urllib.parse
import random
from typing import List, Set, Dict

# .لیستی از جاویدنامان خیزش زن، زندگی، آزادی و آبان ۹۸
JAVID_NAMAN: List[str] = [
    # --- جاویدنامان خیزش زن، زندگی، آزادی ---
    "مهسا امینی", "نیکا شاکرمی", "سارینا اسماعیل‌زاده", "حدیث نجفی", "مینو مجیدی", "غزاله چلابی",
    "حنانه کیا", "محسن شکاری", "مجیدرضا رهنورد", "محمدمهدی کرمی", "سید محمد حسینی", "کیان پیرفلک",
    "خدیجه نقدی", "جواد حیدری", "فرشته احمدی", "رضا شهپرنیا", "عرفان زمانی", "یلدا آقافضلی",
    "ابوالفضل آدینه‌زاده", "اسرا پناهی", "محسن قیصری", "حمیدرضا روحی", "آیلار حقی", "سپهر مقصودی",
    "مهدی زارع اشکذری", "دنیا فرهادی", "آرشیا امامقلی‌زاده", "نگین عبدالمالکی", "مهرشاد شهیدی",
    "سارینا ساعدی", "کومار درافتاده", "بهناز افشاری", "آرمین صیادی", "امیرحسین شمس", "دانیال پابندی",
    "عرفان خزایی", "شیرین علیزاده", "فواد محمدی", "پویا شیدا", "مهرگان زحمتکش", "سیاوش محمودی",
    "پدرام آذرنوش", "علی روزبهانی", "مهدی حضرتی", "آرمان عمادی", "میلاد سعیدیان‌جو", "آیدا رستمی",
    "علی سیدی", "امیرمهدی فرخی‌پور", "سمانه نیک‌نام", "اسماعیل دزوار", "فریدون محمودی", "رضا لطفی",
    "زکریا خیال", "مومن زندکریمی", "صدرالدین لیتانی", "عاطفه نعامی", "آرنیکا قائم مقامی",
    "محمدحسن ترکمان", "مبین میرزایی", "جواد موسوی", "آیدین درویش", "متین نصرتی", "سینا نادری",
    "عرفان کاکایی", "اسماعیل مولودی", "آرین مریدی", "سینا ملایری", "امید حسنی", "آرین خوش‌گواریان",
    "روزبه خادمیان", "رضا کاظمی", "حمید گلی", "محمد حاجی‌رسول‌پور", "شمال خدیری‌پور", "ابراهیم میرزایی",
    "نسرین قادری", "آرمان اکبری", "پوریا احمدی", "محمدامین هاشمی", "امیر فلاحت‌دوست", "میلاد خوشکام",
    "هومن عبداللهی", "امیرمحمد رحیمی", "شورش نیکنام", "محمدحسین کمندلو", "محمود احمدی", "حمیدرضا براهویی",
    "محمد اقبال شهنوازی", "محمد ریگی", "عمر شهنوازی", "سامر هاشم‌زهی", "متین قنبرزهی", "جابر شیروزهی",

    # --- جاویدنامان آبان ۹۸ ---
    "پویا بختیاری", "نیکتا اسفندانی", "نوید بهبودی", "فرزاد انصاری‌فر", "ارشام ابراهیمی", "ابراهیم کتابدار",
    "پژمان قلی‌پور", "مهدی نکویی", "آذر میرزاپور", "منوچهر رضایی", "محسن جعفرپناه", "امیررضا عبداللهی",
    "رضا معظمی", "امیرحسین صادقی", "سعید زینبی", "علیرضا نوری", "محمد حشم‌دار", "مهرداد معین‌فر",
    "وحید دامور", "برهان منصوری", "کمال فرجی", "حمید رسولی", "محمدجواد عابدی", "جواد بابایی",
    "مهدی پازوکی", "علی رحمانی", "مسعود رضوی", "امیر الوندی‌مهر", "آرش کهزادی", "ناصر رضایی",
    "رضا حسن‌وند", "آرمین قادری", "امیر شاملو", "حسین قدمی", "میلاد محبوبی", "بهمن جعفری",
    "محمد ملکی", "میثم احمدی", "فرهاد مجدم", "علی قیصری", "مهدی دالوند", "پوریا ناصرخانی"
]

# لیست لینک‌های سابسکریپشن شما
SUB_LINKS: List[str] = [
    "https://raw.githubusercontent.com/liketolivefree/kobabi/main/sub.txt",
    "https://long-credit-187f.mehdipost675.workers.dev/?token=jHfTut2MRAd9yyPUJQ7K05kiRFDW4hKV",
    "https://withered-math-1242.mehdipost675.workers.dev/?token=U47yXioeT6Q4nwXbkDztDBQBsaDoB5UH",
    "https://lively-dream-c48b.mehdipost675.workers.dev/?token=fedfed7b41b828f17cfb2371c8ee16df"
]

# --- نام فایل‌های خروجی پروتکل ---
OUTPUT_FILENAME_MIX: str = "POORIA-MIX.txt" # نام قبلی POORIAJavidanIran.txt بود
OUTPUT_FILENAME_VLESS: str = "POORIA-VLESS.txt"
OUTPUT_FILENAME_VMESS: str = "POORIA-VMESS.txt"
OUTPUT_FILENAME_TROJAN: str = "POORIA-TROJAN.txt"
OUTPUT_FILENAME_HYSTERIA: str = "POORIA-HYSTERIA.txt"
OUTPUT_FILENAME_SS: str = "POORIA-SS.txt"
OUTPUT_FILENAME_OTHER: str = "POORIA-OTHER.txt"

# --- تنظیمات دسته‌بندی لوکیشن ---
# لیست کدهای کشورها برای دسته‌بندی (به راحتی می‌توانید اضافه یا کم کنید)
COUNTRY_CODES: List[str] = ["DE", "US", "NL", "FR", "IR", "CA", "GB", "SG", "JP", "FI", "PL", "SE", "CH"]

# مپینگ نام کامل کشورها به کد (برای تشخیص بهتر)
COUNTRY_NAME_MAP: Dict[str, str] = {
    "GERMANY": "DE", "ALMAN": "DE",
    "UNITED-STATES": "US", "USA": "US",
    "NETHERLANDS": "NL", "HOLAND": "NL",
    "FRANCE": "FR",
    "IRAN": "IR",
    "CANADA": "CA",
    "UNITED-KINGDOM": "GB", "UK": "GB", "ENGLAND": "GB",
    "SINGAPORE": "SG",
    "JAPAN": "JP",
    "FINLAND": "FI",
    "POLAND": "PL",
    "SWEDEN": "SE",
    "SWITZERLAND": "CH"
}

# هدر درخواست
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_configs_from_sub(url: str) -> List[str]:
    """کانفیگ‌ها را از یک لینک سابسکریپشن دانلود و استخراج می‌کند."""
    try:
        print(f"در حال دریافت کانفیگ از: {url}")
        response = requests.get(url, timeout=20, headers=HEADERS)
        response.raise_for_status()
        content = response.text
        decoded_content = ""
        try:
            missing_padding = len(content) % 4
            if missing_padding: content += '=' * (4 - missing_padding)
            decoded_content = base64.b64decode(content).decode('utf-8')
        except Exception: decoded_content = content
        configs = [line.strip() for line in decoded_content.splitlines() if line.strip()]
        print(f"تعداد {len(configs)} کانفیگ از این لینک پیدا شد.")
        return configs
    except requests.exceptions.RequestException as e:
        print(f"خطا در دریافت لینک {url}: {e}")
        return []
    except Exception as e:
        print(f"خطایی ناشناخته در پردازش لینک {url}: {e}")
        return []

def process_and_save(config_list: List[str], filename: str, names_list: List[str]):
    """
    لیستی از کانفیگ‌ها را دریافت، نام‌گذاری کرده و در فایل خروجی Base64 ذخیره می‌کند.
    """
    if not config_list:
        print(f"هیچ کانفیگی برای فایل {filename} پیدا نشد. فایل ساخته نمی‌شود.")
        return

    sorted_configs = sorted(config_list)
    renamed_configs: List[str] = []
    
    for i, config in enumerate(sorted_configs):
        base_link = config.split('#')[0]
        name_index = i % len(names_list)
        javid_nam = names_list[name_index]
        name_without_spaces = javid_nam.replace(" ", "-")
        
        # --- فرمت جدید نام‌گذاری ---
        # اگر فایل لوکیشن است، لوکیشن را هم اضافه می‌کنیم
        if "LOC-" in filename:
            country_code = filename.split('-')[-1].replace('.txt', '')
            new_name = f"POORIA-{country_code}-{name_without_spaces}"
        else:
             new_name = f"POORIA-{name_without_spaces}"
        
        encoded_name = urllib.parse.quote(new_name)
        new_link = f"{base_link}#{encoded_name}"
        renamed_configs.append(new_link)
        
    final_config_str = "\n".join(renamed_configs)
    final_b64_config = base64.b64encode(final_config_str.encode('utf-8')).decode('utf-8')
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(final_b64_config)
        print(f"یادشان گرامی. فایل '{filename}' با {len(renamed_configs)} کانفیگ ذخیره شد.")
    except IOError as e:
        print(f"خطا در نوشتن فایل خروجی {filename}: {e}")

def get_country_code(config_name: str) -> str:
    """
    نام کانفیگ را تجزیه و تحلیل می‌کند تا کد کشور (DE, US, ...) را پیدا کند.
    """
    if not config_name:
        return "OTHER"
        
    # نام را استاندارد می‌کنیم: حروف بزرگ، جایگزینی _ با -
    name = config_name.upper().replace("_", "-") 
    
    # 1. چک کردن کدهای دو حرفی در ابتدای نام (e.g., "DE-Frankfurt", "[DE]Server")
    for code in COUNTRY_CODES:
        if name.startswith(f"{code}-") or name.startswith(f"({code})") or name.startswith(f"[{code}]"):
            return code
    
    # 2. چک کردن نام کامل کشورها (e.g., "Server-Germany")
    for name_key, code in COUNTRY_NAME_MAP.items():
        if name_key in name:
            return code

    # 3. چک کردن کدهای دو حرفی در وسط نام (e.g., "My-DE-Server")
    for code in COUNTRY_CODES:
         if f"-{code}-" in name or f" {code} " in name:
            return code

    return "OTHER"

def main():
    """تابع اصلی برنامه"""
    if not JAVID_NAMAN:
        print("لیست نام‌ها خالی است. برنامه متوقف شد.")
        return

    # 1. نام‌ها یک بار در ابتدا به هم ریخته می‌شوند
    shuffled_names = JAVID_NAMAN[:]
    random.shuffle(shuffled_names)
    print("\nترتیب نام‌ها به صورت تصادفی برای این اجرا مشخص شد.")
    
    # 2. دریافت تمام کانفیگ‌ها
    all_configs: List[str] = []
    for link in SUB_LINKS:
        all_configs.extend(get_configs_from_sub(link))
    
    print(f"\nمجموعاً {len(all_configs)} کانفیگ (با احتساب موارد تکراری) پیدا شد.")
    
    # 3. حذف تکراری‌ها
    unique_configs: Set[str] = set(all_configs)
    print(f"تعداد {len(unique_configs)} کانفیگ منحصر به فرد یافت شد.")
    
    if not unique_configs:
        print("هیچ کانفیگی برای پردازش وجود ندارد. خروج.")
        return

    # --- بخش ۱: دسته‌بندی بر اساس پروتکل ---
    print("\n--- شروع دسته‌بندی بر اساس پروتکل ---")
    vless_list = []
    vmess_list = []
    trojan_list = []
    ss_list = []
    hysteria_list = [] # شامل hy2 و hysteria
    other_list = []

    for config in unique_configs:
        if config.startswith('vless://'): vless_list.append(config)
        elif config.startswith('vmess://'): vmess_list.append(config)
        elif config.startswith('trojan://'): trojan_list.append(config)
        elif config.startswith('ss://'): ss_list.append(config)
        elif config.startswith('hysteria://') or config.startswith('hy2://'): hysteria_list.append(config)
        else: other_list.append(config)
            
    # ذخیره فایل‌های پروتکل
    process_and_save(list(unique_configs), OUTPUT_FILENAME_MIX, shuffled_names)
    process_and_save(vless_list, OUTPUT_FILENAME_VLESS, shuffled_names)
    process_and_save(vmess_list, OUTPUT_FILENAME_VMESS, shuffled_names)
    process_and_save(trojan_list, OUTPUT_FILENAME_TROJAN, shuffled_names)
    process_and_save(hysteria_list, OUTPUT_FILENAME_HYSTERIA, shuffled_names)
    process_and_save(ss_list, OUTPUT_FILENAME_SS, shuffled_names)
    process_and_save(other_list, OUTPUT_FILENAME_OTHER, shuffled_names)

    # --- بخش ۲: دسته‌بندی بر اساس لوکیشن ---
    print("\n--- شروع دسته‌بندی بر اساس لوکیشن ---")
    
    # ساخت دیکشنری برای نگهداری لیست کانفیگ‌های هر کشور
    location_lists: Dict[str, List] = {code: [] for code in COUNTRY_CODES}
    location_lists["OTHER"] = [] # برای کانفیگ‌های ناشناس

    for config in unique_configs:
        config_name = ""
        try:
            # نام کانفیگ (بعد از #) را استخراج می‌کنیم
            config_name = urllib.parse.unquote(config.split('#')[1])
        except IndexError:
            config_name = "" # کانفیگ‌هایی که نام ندارند
        
        country_code = get_country_code(config_name)
        location_lists[country_code].append(config)

    # گزارش و ذخیره فایل‌های لوکیشن
    print("-" * 30)
    print("گزارش تفکیک لوکیشن‌ها:")
    for code, configs in location_lists.items():
        if len(configs) > 0:
            print(f"لوکیشن {code}: {len(configs)} کانفیگ")
            filename = f"POORIA-LOC-{code}.txt"
            process_and_save(configs, filename, shuffled_names)
    print("-" * 30)
    
    print("\n--- پردازش و ساخت تمام فایل‌ها با موفقیت انجام شد ---")

if __name__ == "__main__":
    main()

