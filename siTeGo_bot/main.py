# God bless you, {Pain}
import datetime
# import chreeypy
import mysql.connector as db
import telebot
from telebot import types

import constants

# Get started
"""
WEBHOOK_HOST = '127.0.0.1'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '127.0.0.1'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % constants.token
"""
bot = telebot.TeleBot(constants.token)
keyboard = types.ReplyKeyboardMarkup(True)
keyboard.row('Так')

remove = types.ReplyKeyboardRemove()
phone = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_phone = types.KeyboardButton(text="Відправити номер телефона", request_contact=True)
phone.add(button_phone)

db = db.connect(
    host="localhost",
    user="root",
    passwd="",
    database='bot'
)
print(db)
cursor = db.cursor()

"""
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

# Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))
"""


@bot.message_handler(content_types=['contact'])
def contact_get(message):
    cursor.execute("SELECT status FROM main WHERE id=" + str(message.from_user.id))
    for x in cursor:
        if x[0] == 4:
            cursor.execute(
                "UPDATE brief SET phone='" + str(message.contact.phone_number) + "' WHERE id=" + str(message.chat.id))
            cursor.execute("UPDATE main SET status=5 WHERE id=" + str(message.from_user.id))
            db.commit()
            bot.send_message(message.from_user.id, 'Вкажіть, будь-ласка, ваш e-mail.', reply_markup=remove)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        cursor.execute("INSERT INTO main(id,status,username) VALUES ('" + str(message.from_user.id) + "','1','" + str(
            message.from_user.username) + "')")
        db.commit()
        bot.send_message(message.from_user.id, "Вітаю. Готові заповнити бриф?", reply_markup=keyboard)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'U already registred, folk.')


# YOLO MAIN CONTENT

@bot.message_handler(content_types=['text'])
def text_handler(message):
    date = datetime.date.today()
    print(date)
    cursor.execute('SELECT status FROM main WHERE id=' + str(message.from_user.id))
    for x in cursor:
        print(x)
        if x[0] == 1:
            if message.text == 'Так':
                bot.send_message(message.from_user.id, 'Добре. Почнемо заповнення брифу.\n'
                                                       'Як Вас звуть?', reply_markup=remove)
                cursor.execute('UPDATE main SET status=2 WHERE id=' + str(message.from_user.id))
                db.commit()
        if x[0] == 2:
            bot.send_message(message.from_user.id, 'Вкажіть контактну особу.')
            cursor.execute("UPDATE main SET status=3 WHERE id=" + str(message.from_user.id))
            cursor.execute("INSERT INTO brief(id,client_name,date) VALUES('" + str(message.from_user.id) + "','" + str(
                message.text) + "','" + str(date) + "')")
            db.commit()
        if x[0] == 3:
            bot.send_message(message.from_user.id, 'Відправте, будь-ласка, номер по якому з вами можна звязатися.',
                             reply_markup=phone)
            cursor.execute("UPDATE main SET status=4 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET contact='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 5:
            print(message.text)
            bot.send_message(message.from_user.id, 'Почнемо детально заповнювати бриф.\n'
                                                   'Просто відповідайте на питання, які ми Вам задамо.\n'
                                                   '<b>1. Інформація про компанію</b>\n'
                                                   '1.1 Повна назва компанії.', parse_mode="HTML")
            cursor.execute("UPDATE main SET status=6 WHERE id=" + str(message.from_user.id))
            db.commit()
            # noinspection PyBroadException
            try:
                cursor.execute(
                    "UPDATE brief SET e_mail='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
                db.commit()
            except Exception as e:
                print(e)
                cursor.execute("UPDATE brief SET e_mail='EXCEPTION' WHERE id=" + str(message.from_user.id))
        if x[0] == 6:
            bot.send_message(message.from_user.id, '1.2 Опис основних послуг/продукції.')
            cursor.execute("UPDATE main SET status=7 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 1_1='" + str(message.text) + "' WHERE id =" + str(message.from_user.id))
            db.commit()
        if x[0] == 7:
            bot.send_message(message.from_user.id, '1.3 Як давно Ви працюєте в даній сфері?')
            cursor.execute("UPDATE main SET status=8 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 1_2='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 8:
            bot.send_message(message.from_user.id, '1.4 Конкурентні переваги')
            cursor.execute("UPDATE main SET status=9 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 1_3='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 9:
            bot.send_message(message.from_user.id, '1.5 Географія бізнесу компанії')
            cursor.execute("UPDATE main SET status=10 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 1_4='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 10:
            bot.send_message(message.from_user.id, '1.6 Основні клієнти та партнери')
            cursor.execute("UPDATE main SET status=11 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 1_5='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 11:
            bot.send_message(message.from_user.id, '1.7 Маркетингові завдання компанії на найближчий час (1- 2 роки)')
            cursor.execute("UPDATE main SET status=12 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 1_6='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 12:
            bot.send_message(message.from_user.id, '2. <b>Конкуренти</b>\n'
                                                   '2.1 Прямі конкуренти \n'
                                                   'Необхідно вказати прямих конкурентів у Вашому цінновому сегменті.\n'
                                                   'При можливості охарактеризуйте їх сильні і слабкі сторони, '
                                                   'вкажіть адреси сайтів.', parse_mode='HTML')
            cursor.execute("UPDATE main SET status=13 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 1_7='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 13:
            bot.send_message(message.from_user.id, '3. <b>Цільова аудиторія</b>\n'
                                                   '3.1 Покупець продукту / послуги. \n'
                                                   'Хто приймає рішення про покупку продукту або послуги?\n'
                                                   'Його соціально-демографічні характеристики '
                                                   '(стать, вік, дохід, освіту, стиль життя)', parse_mode='HTML')
            cursor.execute("UPDATE main SET status=14 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 2_1='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 14:
            bot.send_message(message.from_user.id, '3.2 Унікальна торгова пропозиція (переваги Вашого продукту)')
            cursor.execute("UPDATE main SET status=15 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 3_1='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 15:
            bot.send_message(message.from_user.id, '4. <b>Інформація про інтернет-проект</b>.\n'
                                                   '4.1 Мета створення або розвитку сайту', parse_mode='HTML')
            cursor.execute("UPDATE main SET status=16 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 3_2='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 16:
            bot.send_message(message.from_user.id, '4.2 Яких цілей Ви хочете досягти за допомогою створення сайту?')
            cursor.execute("UPDATE main SET status=17 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 4_1='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 17:
            bot.send_message(message.from_user.id, '4.3 Напишіть попередню структуру сайту: '
                                                   'основні розділи, підрозділи. '
                                                   'Коротко опишіть їх функціональне призначення'
                                                   ' і дайте характеристику змісту кожного з розділів.')
            cursor.execute("UPDATE main SET status=18 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 4_2='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 18:
            bot.send_message(message.from_user.id, '4.4 Яка кількість товарів або послуг буде розміщена на сайті?')
            cursor.execute("UPDATE main SET status=19 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 4_3='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 19:
            bot.send_message(message.from_user.id, '4.5 Які розділи на сайті будуть особливо '
                                                   'актуальними для Вашої цільової аудиторії?')
            cursor.execute("UPDATE main SET status=20 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 4_4='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 20:
            bot.send_message(message.from_user.id,
                             '4.6 Напишіть, яка інформація буде змінюватися на Вашому сайті найбільш часто?')
            cursor.execute("UPDATE main SET status=21 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 4_5='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 21:
            bot.send_message(message.from_user.id, '4.7 Бажані терміни розробки сайту')
            cursor.execute("UPDATE main SET status=22 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 4_6='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 22:
            bot.send_message(message.from_user.id, '4.8 Бюджет проекту (можливі орієнтовні рамки від і до):')
            cursor.execute("UPDATE main SET status=23 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 4_7='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 23:
            bot.send_message(message.from_user.id, '5. <b>Вихідні матеріали</b>\n'
                                                   '5.1 Чи є у Вашій компанії розроблений фірмовий стиль (логотип, '
                                                   'знак, фірмовий колір, фірмовий шрифт і т. д.)?',
                             parse_mode='HTML')
            cursor.execute("UPDATE main SET status=24 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 4_8='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 24:
            bot.send_message(message.from_user.id,
                             '5.2 Які графічні матеріали у Вас у є (фотографії, матеріали, які використовуються при '
                             'розробці іншої рекламної продукції і т. д.)?')
            cursor.execute("UPDATE main SET status=25 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 5_1='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 25:
            bot.send_message(message.from_user.id,
                             '5.3 Чи згодні ви на додаткові витрати, такі як: послуги копірайтера, фотозйомка, '
                             'розробка ілюстрацій і т. д.? ')
            cursor.execute("UPDATE main SET status=26 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 5_2='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 26:
            bot.send_message(message.from_user.id, "6. <b>Основні вимоги і побажання по дизайну</b>\n"
                                                   "6.1 Вимоги до дизайну. Напишіть вимоги до дизайну, які є "
                                                   "обов'язковими для виконання.  Побажання до дизайну сайту.",
                             parse_mode='HTML')
            cursor.execute("UPDATE main SET status=27 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 5_3='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 27:
            bot.send_message(message.from_user.id, '6.2 Близькі до бажаного результату по стилю сайти інших компаній?\n'
                                                   'Напишіть адреси кількох сайтів, які Вам подобаються. Що саме Вам '
                                                   'подобається в цих сайтах (стильний дизайн, зручна навігація і т. '
                                                   'д.)?')
            cursor.execute("UPDATE main SET status=28 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 6_1='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 28:
            bot.send_message(message.from_user.id, '7. <b>Додаткова інформація</b>\n'
                                                   '7.1 Будь-яка корисна в роботі над проектом інформація',
                             parse_mode="HTML")
            cursor.execute("UPDATE main SET status=29 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 6_2='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
        if x[0] == 29:
            bot.send_message(message.from_user.id,
                             'Дякуємо за заповнення брифу. Наш менеджер звяжется з вами найближчим часом.\n'
                             'Можливо ви хочете заповнити ще один?', reply_markup=keyboard)
            cursor.execute("UPDATE main SET status=1 WHERE id=" + str(message.from_user.id))
            cursor.execute("UPDATE brief SET 7_1='" + str(message.text) + "' WHERE id=" + str(message.from_user.id))
            db.commit()
            cursor.execute("SELECT * FROM brief WHERE id=" + str(message.from_user.id))
            # noinspection PyAssignmentToLoopOrWithParameter
            for x in cursor:
                print(x)
                bot.send_message(constants.admins, "Новий бриф."
                                                   "\nID юзера - " + str(x[0]) +
                                 "\nІм'я - " + str(x[1]) +
                                 "\nКонтактне обличчя - " + str(x[3]) +
                                 "\nТелефон - " + str(x[4]) +
                                 "\nЕ-мейл - " + str(x[5]))
                bot.send_message(constants.admins, "1.1 - " + str(x[6]) +
                                 "\n1.2 - " + str(x[7]) +
                                 "\n1.3 - " + str(x[8]) +
                                 "\n1.4 - " + str(x[9]) +
                                 "\n1.5 - " + str(x[10]) +
                                 "\n1.6 - " + str(x[11]) +
                                 "\n1.7 - " + str(x[12]))
                bot.send_message(constants.admins, "2.1 - " + str(x[13]) +
                                 "\n3.1 - " + str(x[14]) +
                                 "\n3.2 - " + str(x[15]) +
                                 "\n4.1 - " + str(x[16]) +
                                 "\n4.2 - " + str(x[17]) +
                                 "\n4.3 - " + str(x[18]) +
                                 "\n4.4 - " + str(x[19]))
                bot.send_message(constants.admins, "4.5 - " + str(x[20]) +
                                 "\n4.6 - " + str(x[21]) +
                                 "\n4.7 - " + str(x[22]) +
                                 "\n4.8 - " + str(x[23]) +
                                 "\n5.1 - " + str(x[24]) +
                                 "\n5.2 - " + str(x[25]) +
                                 "\n5.3 - " + str(x[26]) +
                                 "\n6.1 - " + str(x[27]) +
                                 "\n6.2 - " + str(x[28]) +
                                 "\n7.1 - " + str(x[29]))


bot.polling(none_stop=True)
