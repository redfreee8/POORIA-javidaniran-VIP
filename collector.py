import requests
import base64
import urllib.parse
import random
import json
import re
import concurrent.futures
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
    "محمد اقبال شهنوازی", "محمد ریگی", "عمر شهنوازی", "سامر هاشم‌زهی", "متین قنberزهی", "جابر شیروزهی",

    # --- جاویدنامان آبان ۹۸ ---
    "پویا بختیاری", "نیکتا اسفندانی", "نوید بهبودی", "فرزاد انصاری‌فر", "ارشام ابراهیمی", "ابراهیم کتابدار",
    "پژمان قلی‌پور", "مهدی نکویی", "آذر میرزاپور", "منوچهر رضایی", "محسن جعفرپناه", "امیررضا عبداللهی",
    "رضا معظمی", "امیرحسین صادقی", "سعید زینبی", "علیره نوری", "محمد حشم‌دار", "مهرداد معین‌فر",
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
OUTPUT_FILENAME_MIX: str = "POORIAred-MIX.txt"
OUTPUT_FILENAME_VLESS: str = "POORIAred-VLESS.txt"
OUTPUT_FILENAME_VMESS: str = "POORIAred-VMESS.txt"
OUTPUT_FILENAME_TROJAN: str = "POORIAred-TROJAN.txt"
OUTPUT_FILENAME_HYSTERIA: str = "POORIAred-HYSTERIA.txt"
OUTPUT_FILENAME_SS: str = "POORIAred-ss.txt"
OUTPUT_FILENAME_OTHER: str = "POORIAred-OTHER.txt"

# --- تنظیمات دسته‌بندی لوکیشن (بهبود یافته) ---
EMOJI_COUNTRY_MAP: Dict[str, str] = {
    "🇦🇱": "AL", "🇦🇷": "AR", "🇦🇺": "AU", "🇦🇹": "AT", "🇧🇩": "BD", "🇧🇪": "BE", "🇧🇷": "BR",
    "🇧🇬": "BG", "🇨🇦": "CA", "🇨🇱": "CL", "🇨🇳": "CN", "🇨🇴": "CO", "🇭🇷": "HR", "🇨🇿": "CZ",
    "🇩🇰": "DK", "🇪🇪": "EE", "🇫🇮": "FI", "🇫🇷": "FR", "🇬🇪": "GE", "🇩🇪": "DE", "🇬🇷": "GR",
    "🇭🇰": "HK", "🇭🇺": "HU", "🇮🇸": "IS", "🇮🇳": "IN", "🇮🇩": "ID", "🇮🇪": "IE", "🇮🇱": "IL",
    "🇮🇹": "IT", "🇯🇵": "JP", "🇰🇿": "KZ", "🇰🇷": "KR", "🇱🇻": "LV", "🇱🇹": "LT", "🇱🇺": "LU",
    "🇲🇾": "MY", "🇲🇽": "MX", "🇲🇩": "MD", "🇳🇱": "NL", "🇳🇿": "NZ", "🇳🇬": "NG", "🇳🇴": "NO",
    "🇵🇰": "PK", "🇵🇭": "PH", "🇵🇱": "PL", "🇵🇹": "PT", "🇷🇴": "RO", "🇷🇺": "RU", "🇷🇸": "RS",
    "🇸🇬": "SG", "🇸🇰": "SK", "🇸🇮": "SI", "🇿🇦": "ZA", "🇪🇸": "ES", "🇸🇪": "SE", "🇨🇭": "CH",
    "🇹🇼": "TW", "🇹🇭": "TH", "🇹🇷": "TR", "🇦🇪": "AE", "🇺🇦": "UA", "🇬🇧": "GB", "🇺🇸": "US",
    "🇻🇳": "VN", "🇮🇷": "IR"
}

# مپینگ نام‌ها و کدهای جایگزین به کد اصلی (اولویت با کدهای اصلی است)
COUNTRY_REGEX_MAP: Dict[str, str] = {
    "DE": r"\b(DE|GERMANY|ALMAN|GER)\b",
    "US": r"\b(US|USA|UNITED-STATES|AMERICA)\b",
    "NL": r"\b(NL|NETHERLANDS|HOLAND)\b",
    "FR": r"\b(FR|FRANCE)\b",
    "IR": r"\b(IR|IRAN)\b",
    "CA": r"\b(CA|CANADA)\b",
    "GB": r"\b(GB|UK|UNITED-KINGDOM|ENGLAND|ENG)\b",
    "SG": r"\b(SG|SINGAPORE)\b",
    "JP": r"\b(JP|JAPAN)\b",
    "FI": r"\b(FI|FINLAND)\b",
    "PL": r"\b(PL|POLAND)\b",
    "SE": r"\b(SE|SWEDEN)\b",
    "CH": r"\b(CH|SWITZERLAND)\b",
    # می‌توانید موارد بیشتر را به این شکل اضافه کنید
    "RU": r"\b(RU|RUSSIA)\b",
    "TR": r"\b(TR|TURKEY)\b",
    "AE": r"\b(AE|UAE|DUBAI)\b",
    "HK": r"\b(HK|HONGKONG)\b",
    "IT": r"\b(IT|ITALY)\b",
    "ES": r"\b(ES|SPAIN)\b",
    "AU": r"\b(AU|AUSTRALIA)\b",
}
# لیست تمام کدهای تعریف شده
COUNTRY_CODES: List[str] = list(COUNTRY_REGEX_MAP.keys())

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
        
        # تلاش برای دیکد کردن Base64
        decoded_content = ""
        try:
            # مدیریت خطای پدینگ Base64
            missing_padding = len(content) % 4
            if missing_padding:
                content += '=' * (4 - missing_padding)
            decoded_content = base64.b64decode(content).decode('utf-8')
        except Exception:
            # اگر Base64 نبود، محتوای خام را در نظر بگیر
            decoded_content = content
            
        configs = [line.strip() for line in decoded_content.splitlines() if line.strip()]
        print(f"  -> {len(configs)} کانفیگ از {url} پیدا شد.")
        return configs
    except requests.exceptions.RequestException as e:
        print(f"  -> خطا در دریافت لینک {url}: {e}")
        return []
    except Exception as e:
        print(f"  -> خطایی ناشناخته در پردازش لینک {url}: {e}")
        return []

def create_info_config(display_name: str, count: int) -> str:
    """
    یک کانفیگ vmess سیاهچاله (blackhole) برای نمایش اطلاعات ساب در کلاینت می‌سازد.
    """
    info_name = f"✅ {display_name} ({count} Configs)"
    
    vmess_json = {
        "v": "2",
        "ps": info_name,
        "add": "127.0.0.1", # آدرس محلی
        "port": 1080, # یک پورت استاندارد
        "id": "00000000-0000-0000-0000-000000000000", # آیدی فیک
        "aid": 0,
        "net": "tcp",
        "type": "http", # تنظیم به http که معمولا بلاک است
        "host": "",
        "path": "/",
        "tls": "",
        "sni": ""
    }
    
    # انکد کردن جیسون به Base64
    json_str = json.dumps(vmess_json)
    b64_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
    return f"vmess://{b64_str}"

def process_and_save(config_list: List[str], filename: str, names_list: List[str], display_name: str):
    """
    لیستی از کانفیگ‌ها را دریافت، نام‌گذاری کرده، هدر اطلاعات اضافه کرده
    و در فایل خروجی Base64 ذخیره می‌کند.
    """
    if not config_list:
        print(f"هیچ کانفیگی برای فایل {filename} پیدا نشد. فایل ساخته نمی‌شود.")
        return

    # مرتب‌سازی برای اطمینان از ترتیب یکسان در هر اجرا
    sorted_configs = sorted(config_list)
    renamed_configs: List[str] = []
    
    # 1. ساخت و اضافه کردن هدر اطلاعات
    info_header = create_info_config(display_name, len(sorted_configs))
    renamed_configs.append(info_header)
    
    # 2. تغییر نام کانفیگ‌های اصلی
    for i, config in enumerate(sorted_configs):
        base_link = config.split('#')[0]
        
        # استفاده از لیست نام‌های جاویدنامان به صورت چرخشی
        name_index = i % len(names_list)
        javid_nam = names_list[name_index]
        name_without_spaces = javid_nam.replace(" ", "-")
        
        # فرمت جدید نام‌گذاری
        if "LOC-" in filename:
            country_code = display_name.split('-')[-1] # از display_name کد کشور را می‌گیریم
            new_name = f"POORIAred-{country_code}-{name_without_spaces}"
        else:
            new_name = f"POORIAred-{name_without_spaces}"
        
        encoded_name = urllib.parse.quote(new_name)
        new_link = f"{base_link}#{encoded_name}"
        renamed_configs.append(new_link)
        
    # 3. ذخیره فایل
    final_config_str = "\n".join(renamed_configs)
    final_b64_config = base64.b64encode(final_config_str.encode('utf-8')).decode('utf-8')
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(final_b64_config)
        # +1 برای هدر اطلاعاتی که اضافه کردیم
        print(f"یادشان گرامی. فایل '{filename}' با {len(renamed_configs) - 1} کانفیگ (و 1 هدر) ذخیره شد.")
    except IOError as e:
        print(f"خطا در نوشتن فایل خروجی {filename}: {e}")

def get_country_code(config_name: str) -> str:
    """
    نام کانفیگ را تجزیه و تحلیل می‌کند تا کد کشور (DE, US, ...) را پیدا کند.
    (نسخه بسیار هوشمندتر)
    """
    if not config_name:
        return "OTHER"
        
    # 1. بررسی ایموجی‌ها (سریع‌ترین روش)
    for emoji, code in EMOJI_COUNTRY_MAP.items():
        if emoji in config_name:
            return code
            
    # 2. پاکسازی و استانداردسازی نام
    # حذف پرانتز، براکت، خط لوله و... و تبدیل به حروف بزرگ
    cleaned_name = re.sub(r"[\[\]\(\)\{\}\|\-_]", " ", config_name.upper())
    # اضافه کردن فاصله در دو طرف برای تطابق بهتر Regex
    cleaned_name = f" {cleaned_name} " 

    # 3. بررسی با Regex
    for code, pattern in COUNTRY_REGEX_MAP.items():
        if re.search(pattern, cleaned_name):
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
    
    # 2. دریافت تمام کانفیگ‌ها (به صورت همزمان)
    all_configs: List[str] = []
    print("\n--- شروع دریافت همزمان کانفیگ‌ها ---")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # ارسال تمام تسک‌ها
        future_to_url = {executor.submit(get_configs_from_sub, url): url for url in SUB_LINKS}
        
        # جمع‌آوری نتایج به محض آماده شدن
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                configs = future.result()
                all_configs.extend(configs)
            except Exception as e:
                print(f"خطای جدی در پردازش یکی از لینک‌ها: {e}")

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
    process_and_save(list(unique_configs), OUTPUT_FILENAME_MIX, shuffled_names, "POORIAred-MIX")
    process_and_save(vless_list, OUTPUT_FILENAME_VLESS, shuffled_names, "POORIAred-VLESS")
    process_and_save(vmess_list, OUTPUT_FILENAME_VMESS, shuffled_names, "POORIAred-VMESS")
    process_and_save(trojan_list, OUTPUT_FILENAME_TROJAN, shuffled_names, "POORIAred-TROJAN")
    process_and_save(hysteria_list, OUTPUT_FILENAME_HYSTERIA, shuffled_names, "POORIAred-HYSTERIA")
    process_and_save(ss_list, OUTPUT_FILENAME_SS, shuffled_names, "POORIAred-SS")
    process_and_save(other_list, OUTPUT_FILENAME_OTHER, shuffled_names, "POORIAred-OTHER")

    # --- بخش ۲: دسته‌بندی بر اساس لوکیشن ---
    print("\n--- شروع دسته‌بندی بر اساس لوکیشن ---")
    
    # ساخت دیکشنری برای نگهداری لیست کانفیگ‌های هر کشور
    location_lists: Dict[str, List] = {code: [] for code in COUNTRY_CODES}
    location_lists["OTHER"] = [] # برای کانفیگ‌های ناشناس

    for config in unique_configs:
        config_name = ""
        try:
            # نام کانفیگ (بعد از #) را استخراج و دیکد می‌کنیم
            config_name = urllib.parse.unquote(config.split('#', 1)[1])
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
            
            # --- !! مهم: این بخش اصلاح شد !! ---
            filename = f"POORIAred-LOC-{code}.txt"
            display_name = f"POORIAred-{code}" # نامی که در کلاینت نمایش داده می‌شود
            process_and_save(configs, filename, shuffled_names, display_name)
            
    print("-" * 30)
    
    print("\n--- پردازش و ساخت تمام فایل‌ها با موفقیت انجام شد ---")

if __name__ == "__main__":
    main()
