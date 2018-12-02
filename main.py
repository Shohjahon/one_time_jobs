import telebot
import  random
import db_helper
import requests

bot = telebot.TeleBot('732891656:AAF0DFMBNE37B2ZNIETIxeS8x3Hcj4AkocY')
categories = ["Yengil ishlar","Og'ir ishlar","Ofis ishlari"]
names = ["C# dasturlash", "Malyarka", "Yuk tashish", "Shudgorlash"]
job_abouts = ["Oddiy ish", "Oddiy ish", "Oddiy ish"]
prices = ["10$", "30$", "100 ming so'm"]
job_dates = ["10/12/18", "11/12/18", "21/12/18"]
job_owner_phones = ["991112233", "991112233", "991112233", "1234343"]
job_addresses = ["Tosh, Yunusobod", "Tosh, Chilonzor", "Tosh, Qibray"]

job_region = ''
job_district = ''


regions = ["🏭 Tashkent", "🏡 Fergana",
           "🏡 Andijan", "🏡 Namangan",
           "🏔 Jizzakh", "🕌 Samarkand",
           "🏔 Kashkadarya", "🏔 Surhondarya",
           "🕌 Bukhara", "🏜 Navoi", "🏢 Sirdaryo",
           "🕌 Khorezm", "🌅 Karakalpakistan"]


#ish beruvchi ma'lumotlari
job_category_name = ''
job_name = ''
job_about = ''
job_price = ''
job_date = ''
job_owner_phone = ''
job_address = ''

page_count = 0

#regionlar
#regions = ["Toshkent sh.", "Toshkent vil.", "Xorazm", "Samarqand", "Andijon"]
#didtricts
districts = ["Yunsobod", "Forish", "Paxtakor", "Mirzacho'l"]

#current job information
current_region = ''
current_district = ''
current_jobs = []
current_address = ["17/7", "7/8", "8/8"]

#jobs
jobs_from_db = []

global handle_start
global callback_category

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_role_markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_recruiter = telebot.types.KeyboardButton(text="👨‍🏫 Ish beruvchi")
    btn_user = telebot.types.KeyboardButton(text="👨🏻‍🏭 Ish qidiruvchi")
    user_role_markup.add(btn_recruiter,btn_user)
    bot.send_message(message.chat.id,"Iltimos foydalanuvchi turini tanlang!",reply_markup=user_role_markup)

@bot.message_handler(content_types=['text'])
def handle_job_category(message):
    if message.text == '👨‍🏫 Ish beruvchi':
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(*[telebot.types.InlineKeyboardButton(text=cat,
                                                          callback_data=cat) for cat in categories])
        bot.send_message(message.chat.id, "Iltimos ish kategoriyalaridan birini tanlang!",
                         reply_markup=keyboard)
    else:
        if message.text == '👨🏻‍🏭 Ish qidiruvchi':
            one_or_many_job_markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            btn_one = telebot.types.KeyboardButton(text="🏫 Bir martalik ish")
            btn_many = telebot.types.KeyboardButton(text="🏭 Doimiy ish")
            one_or_many_job_markup.add(btn_one, btn_many)
            bot.send_message(message.chat.id, "Iltimos ish turini tanlang!",
                             reply_markup=one_or_many_job_markup)
            bot.register_next_step_handler(message, handle_one_or_many_job)

def handle_one_or_many_job(message):
    if message.text == "🏫 Bir martalik ish":
        global jobs_from_db
        jobs_from_db = db_helper.get_spots()
        job_regions_markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        job_regions_markup.add(*[telebot.types.KeyboardButton(text=region) for region in regions])
        bot.send_message(message.chat.id, "Iltimos ish izlayotgan viloyat yoki shaharni tanlang!",
                         reply_markup=job_regions_markup)
        bot.register_next_step_handler(message, handle_region)
    elif message.text == "🏭 Doimiy ish":
        url = "http://data.gov.uz/uz/api/v1/json/dataset/3397/version/12561?access_key=10448a8848f8a88633a4961c0e6e19a8"
        respons = requests.get(url=url, verify = False)
        global jobs_from_net
        global page_count
        jobs_from_net = respons.json()
        print(jobs_from_net)
        for item in jobs_from_net[page_count:5]:
            offer = '''
                     🤔 Ish turi: {} \n
                     💼 Nomi: {} \n
                     🗣 Haqida: {}\n
                     💵 Narx: {}\n
                     📞 Telefon: {}\n
                     🔔 Manzili: {} \n'''.format(item['G3'], item['G2'], item['G1'], item['G5'], item['G6'], item['G6'])
            page_keyboard = telebot.types.InlineKeyboardMarkup()
            prev_btn = telebot.types.InlineKeyboardButton(text="Oldingi ishlar",callback_data='back#{}'.format(page_count))
            next_btn = telebot.types.InlineKeyboardButton(text="Keyingi ishlar",callback_data='next#{}'.format(page_count))
            page_keyboard.add(next_btn,prev_btn)
            bot.send_message(message.chat.id, offer,reply_markup=page_keyboard)


def handle_region(message):
    global current_region
    current_region = str(message.text)[2:]
    if message.text == "🏭 Tashkent":
        job_districs_markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        job_districs_markup.add(*[telebot.types.KeyboardButton(text=dist) for dist in districts])
        bot.send_message(message.chat.id, "Iltimos ish izlayotgan tumanni tanlang!",
                         reply_markup=job_districs_markup)
        bot.register_next_step_handler(message,handle_district)
def handle_district(message):
    print(message.text)
    global current_district
    current_district = message.text
    current_jobs = db_helper.getByRegionDistrict(current_region, current_district)
    print(current_jobs)
    for item in current_jobs:
        offer = '''
                 🤔 Ish turi: {} \n
                 💼 Nomi: {} \n
                 🗣 Haqida: {}\n
                 💵 Narx: {}\n
                 📆 Qachon: {} \n
                 📞 Telefon: {}\n
                 🔔 Manzili: {} \n'''.format(item[3], item[1], item[2], item[4], item[5], item[6], item[7])
        bot.send_message(message.chat.id, offer)

@bot.callback_query_handler(func=lambda call: True)
def callback_category(call):
    if call.message:
        if call.data in categories:
            global job_category_name
            job_category_name = call.data
            job_name = bot.send_message(call.from_user.id, "Iltimos ish nomini kiriting:")
            bot.register_next_step_handler(job_name, job_name_set_after)

    page_data = call.data
    page_status = str(page_data).split('#')




def job_name_set_after(message):
    global job_name
    job_name = message.text
    job_about = bot.send_message(message.chat.id, "Iltimos bu ish haqida to'liqroq ma'lumot bering:")
    bot.register_next_step_handler(job_about, job_about_set_after)

def job_about_set_after(message):
    global job_about
    job_about = message.text
    job_price = bot.send_message(message.chat.id, "Iltimos ish haqini kiriting:")
    bot.register_next_step_handler(job_price, job_price_set_after)

def job_price_set_after(message):
    global job_price
    job_price = message.text
    job_date = bot.send_message(message.chat.id, "Iltimos ish sanasi kiriting(kun/oy/yil):")
    bot.register_next_step_handler(job_date, job_date_set_after)

def job_date_set_after(message):
    global job_date
    job_date = message.text
    job_owner_phone = bot.send_message(message.chat.id, "Iltimos telefon raqamingizni kiriting:")
    bot.register_next_step_handler(job_owner_phone, job_owner_phone_set_after)

def job_owner_phone_set_after(message):
    global job_owner_phone
    job_owner_phone = message.text
   # job_address =  bot.send_message(message.chat.id, "Iltimos taklif qilayotgan ishingizni adresini kiriting(Vil/Shah, tum, ko'cha, xonadon):")
    region_markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_tashkent = telebot.types.KeyboardButton(text="🏭 Tashkent")
    btn_fergana = telebot.types.KeyboardButton(text="🏡 Fergana")
    btn_andijan = telebot.types.KeyboardButton(text="🏡 Andijan")
    btn_namangan = telebot.types.KeyboardButton(text="🏡 Namangan")
    btn_jizzakh = telebot.types.KeyboardButton(text="🏔 Jizzakh")
    btn_samarkand = telebot.types.KeyboardButton(text="🕌 Samarkand")
    btn_kashka = telebot.types.KeyboardButton(text="🏔 Kashkadarya")
    btn_surhan = telebot.types.KeyboardButton(text="🏔 Surhondarya")
    btn_buhara = telebot.types.KeyboardButton(text="🕌 Bukhara")
    btn_navoi = telebot.types.KeyboardButton(text="🏜 Navoi")
    btn_sirdaryo = telebot.types.KeyboardButton(text="🏢 Sirdaryo")
    btn_kherzm = telebot.types.KeyboardButton(text="🕌 Khorezm")
    btn_karak = telebot.types.KeyboardButton(text="🌅 Karakalpakistan")
    region_markup.add(btn_tashkent, btn_fergana, btn_andijan, btn_namangan, btn_jizzakh, btn_samarkand, btn_kashka,
                      btn_surhan, btn_buhara, btn_navoi, btn_sirdaryo, btn_kherzm, btn_karak)
    bot.send_message(message.chat.id,
                     "Ish joylashgan viloyatni tanlang!",
                     reply_markup=region_markup)
    bot.register_next_step_handler(message, job_district_in_region)

def job_district_in_region(message):
    global job_region
    job_region = str(message.text)[2:]
    if message.text == "🏭 Tashkent":
        district_markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        district_markup.add(*[telebot.types.KeyboardButton(text=dist) for dist in districts])
        bot.send_message(message.chat.id,
                         "Ish joylashgan tumanni tanlang!",
                         reply_markup=district_markup)
        bot.register_next_step_handler(message, job_address_set_after)

def job_address_set_after(message):
    global job_district
    job_district = message.text
    global job_address
    job_address = job_region + "," + job_district
    offer = '''
        🏛 Siz taklif qilayotgan ish: \n
         🤔 Ish turi: {}\n
         💼 Nomi: {} \n
         🗣 Haqida: {}\n
         💵 Narx: {}\n
         📆 Qachon: {} \n
         📞 Telefon: {}\n
         🔔 Manzili: {} \n'''.format(job_category_name, job_name, job_about, job_price, job_date, job_owner_phone, job_address)
    bot.send_message(message.chat.id, offer)
    confirm_job_markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    confirm_job_yes = telebot.types.KeyboardButton(text="Ha")
    confirm_job_no = telebot.types.KeyboardButton(text="Yo'q")
    confirm_job_markup.add(confirm_job_yes, confirm_job_no)
    bot.send_message(message.chat.id, "Ish haqida ma'lumotlar to'g'rimi?", reply_markup=confirm_job_markup)
    bot.register_next_step_handler(message, handle_confirm_job)

def handle_confirm_job(message):
    if message.text == "Ha":
        db_helper.add_spot(job_name, job_about, job_category_name, job_price, job_date, job_owner_phone, job_address,
                           "coordinate")

        bot.send_message(message.chat.id, "🎇🎇🎉🎉 Siz taklif qilayotgan ish ro'yhatga olindi",reply_markup=generation_markup())
    elif message.text == "Yo'q":
        bot.send_message(message.chat.id, "Ma'lumotlar saqlanmadi. Qayta urinib ko'rishingiz mumkin",
                         reply_markup=generation_markup())

def generation_markup():
    user_role_markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_recruiter = telebot.types.KeyboardButton(text="👨‍🏫 Ish beruvchi")
    btn_user = telebot.types.KeyboardButton(text="👨🏻‍🏭 Ish qidiruvchi")
    user_role_markup.add(btn_recruiter, btn_user)
    return  user_role_markup

bot.polling()