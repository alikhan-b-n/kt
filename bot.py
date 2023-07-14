from telebot import *
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import openpyxl
import time
import psycopg2
from datetime import datetime, timedelta
import pandas as pd

bot = telebot.TeleBot('6145415028:AAFDb2qjUr4AgqipnmDCCTLnBChF49cyE9U')


categories = {
    'Learning.telecom.kz | Техническая поддержка': 'info.ktcu@telecom.kz',
    'Обучение | Корпоративный Университет': 'info.ktcu@telecom.kz',
    'Служба поддержки “Нысана"': 'nysana@cscc.kz',
    'Обратиться в службу комплаенс': 'tlek.issakov@telecom.kz',
}

faq_field = ["Часто задаваемые вопросы", "Демеу", "Вопросы к HR"]
biot_field = ["Заполнить карточку БиОТ", "Опасный фактор/условие", "Поведение при выполнении работ", "Предложения/Идеи"]
kb_field = ["База знаний", "База инструкций", "Глоссарий"]
kb_field_all = ["Логотипы и Брендбук", "Личный кабинет telecom.kz", "Модемы | Настройка", "Lotus | Инструкции",
                "Мобильная версия", "ПК или ноутбук", "portal.telecom.kz | Инструкции",
                "CheckPoint VPN | Удаленная работа", "Командировка | Порядок оформления",
                "Как авторизоваться", "Личный профиль", "Из портала перейти в ССП"]
instr_field = ["Брендбук и логотипы", "Личный кабинет telecom.kz", "Модемы | Настройка", "Lotus & CheckPoint"]
adapt_field = ["Welcome курс | Адаптация"]
new_message, user_name, chosen_category, flag, appeal_field = '', '', '', 0, False
admin_id = ['484489968', '187663574']

faq_1 = {
    'Ha кого направлена программа “Демеу” в AO “Казахтелеком”?': 'Социальная поддержка Программы «Демеу» AO «Казахтелеком»:  (далее - Программа) направлена работникам по статусу: \
  \n1) многодетная семья - семья, имеющая в своем составе четырех и более совместно проживающих несовершеннолетних детей, в том числе детей, обучающихся по очной форме обучения в организациях среднего, \
  технического и профессионального, послесреднего, высшего и (или) послевузовского образования после достижения ими совершеннолетия до времени окончания образования (но не более чем до достижения \
  двадцатитрехлетнего возраста); \n2) семья c детьми-инвалидами - семья, имеющая в своем составе ребенка (детей) до восемнадцати лет, имеющего(-их) нарушение здоровья co стойким расстройством функций организма,\
  обусловленное заболеваниями, увечьями (ранениями, травмами, контузиями), их последствиями, дефектами, которые приводят к ограничению жизнедеятельности и необходимости ero (их) социальной защиты; \
  \n3) семья, усыновившая/удочерившая более 2-x детей - семья, имеющая в своем составе более 2-x несовершеннолетних усыновленных/удочеренных детей, которые состоят на диспансерном учете по состоянию здоровья, и единственного кормильца. \
  \n4) Работникам грейда A8-B4 устанавливается социальная поддержка по оплате выпускного курса обучения (без учета расходов на проживание и питание) их детей в среднем специальном учебном заведении (далее - CYZ)/высшем учебном заведении (далее - BYZ). \
  \nBce виды социальной поддержки оказываются работникам Общества, имеющим на момент предоставления социальной поддержки стаж непрерывной работы в Обществе не менее 3-x лет.\
  \n*Обращения физических лиц ob оказании социальной поддержки/помощи, не состоящих в трудовых отношениях c AO «Казахтелеком», к рассмотрению не принимаются.',
    'Виды социальной поддержки для работников': '1) возмещение расходов, связанных c приобретением путевок в детские оздоровительные лагеря; \
  \n2) возмещение расходов, связанных c приобретением путевок в детские оздоровительные санатории (для детей-инвалидов); \
  \n3) материальная помощь на приобретение лекарственных средств для детей; \
  \n4) материальная помощь на питание учащихся школ; \n5) материальная помощь к началу учебного года; \
  \n6) возмещение средств за медицинскую реабилитацию/индивидуальную программу реабилитации ребенка (для детей-инвалидов); \
  \n7) возмещение средств за специальные образовательные программы (для детей-инвалидов); \
  \n8) возмещение средств за посещение специальных коррекционных организаций (для детей-инвалидов); \
  \n9) материальная помощь выпускникам школ, не достигшим на дату окончания школы совершеннолетия и окончившим учебу на отлично; \
  \n10) возмещение (работникам грейда A8-B4) расходов по оплате выпускного курса обучения (без учета расходов на проживание и питание) их детей в среднем специальном учебном заведении (далее - CYZ)/высшем учебном заведении (далее - BYZ).',
    'Процесс подачи заявления в социальную комиссию': 'Основанием для рассмотрения вопроса об оказании социальной поддержки является заявление работника \nЦА/филиала, поданное в Социальную комиссию ЦА/филиала с приложением подтверждающих документов.',
    'Где оформлять заявление?': 'Заявление оформляете в своей рабочей базе(БРД). Специальных баз нет.',
    'Председатель социальной комиссии ДРБ': ' Председатель Социальной комиссии в филиалах - Генеральный директор филиала. В ЦА – Главный директор по операционной эффективности',
}

faq_2 = {
    'Как получить справку c места работы?': 'Заявку на получение спpaвки c места работы необходимо оформить в Базе «Заявки ОЦО HR». \nСоздать новый – выбрать наименование Вашего филиала – заявка на выдачу справки с места работы – заполнить ФИО сотрудника, вид справки и необходимые критерии (язык, стаж, должностной оклад, средняя заработная плата) – сохранить заявку – Отправить в ОЦО В Заявке автоматически будет указан Исполнитель Вашей заявки.',
    'Как создать учетную запись Lotus и доступ к ИС и БРД?': 'Для создания учетной записи Lotus Notes необходимо обратиться к Вашему курирующему руководителю/наставнику/делопроизводителю структурного подразделения для оформления заявки в Базе ЕСУД (Единая система управления доступом). \nПо мере готовности учетной записи (файл с логином и паролем),'
                                                             ' необходимо оформить заявку в Help Desk по номеру: +7 727 2587304 После установления учетной записи Lotus Notes, необходимо самостоятельно создать заявку в Базе ЕСУД с указанием необходимого для Вас доступа к ИС и БД.',
    'Куда обратиться если забыл пароль или сбой в Lotus?': 'Оставить заявку HelpDesk +77272587304 по возникшим вопросам.',
    'Как оплачиваются листы временной нетрудоспособности?': 'Листы временной нетрудоспособности для работников (членов профсоюзной организации и присоединившихся к Коллективному договору) оплачиваются в зависимости от непрерывного стажа работы в компании: \n- до 2-х лет включительно - в соответствии с законодательством Республики Казахстан; \n- до 5 лет - 40% средней заработной платы; \n- свыше 5 лет - 70% средней заработной платы за дни временной нетрудоспособности.',
    'Кто заполняет больничный лист?': 'Больничный лист заполняет табельщик/делопроизводитель структурного подразделения. B больничном листе отражаете  наименование филиала "Дивизион по розничному бизнесу - филиал AO "Казахтелеком" и свою должность.',
    'Кому сдавать лист временной нетрудоспособности (больничный лист)?': 'Прежде чем сдать лист временной нетрудоспособности, его необходимо заполнить и подписать  y своего непосредственного руководителя. \nВ случае, если в Вашем офисе отсутствует работник фронт-офиса ОЦО HR - отсканировать с двух сторон БЛ и оформить заявкой в Базе Заявки ОЦО HR; в противном случае – сдать заполненный оригинал БЛ работнику фронт-офиса ОЦО HR.',
    'Как вступить в Профсоюз?': 'Для вступления в Локальный профсоюз, необходимо оформить заявление о вступлении в Профсоюз Вашего филиала (шаблон о вступлении в Профсоюз можно получить у работника фронт-офиса ОЦО HR) и оформить заявку в Базе Заявки в ОЦО ЗП об удержании профсоюзных взносов. Процент удержания составляет – 1 %.',
    'Страховка по ДМС (добровольное медицинское страхование)': 'Страховка по ДМС (добровольное медицинское страхование) осуществляется  работникам имеющих стаж работы в Обществе более 3-x  лет, при условии возможности страхового покрытия',
    'Где найти телефон коллег?': 'Телефон коллеги Вы можете найти базе "Телефонный справочник Общества" - номера телефонов по Фамилии, поиск сотрудников по подразделению',
    'Обходной лист. Когда ero оформлять?': '1) При оформление заявления на увольнение, автоматически сформирован в третьем листе обходной лист и указаны подписанты.\n2) При переводе/одностороннем порядке/ в филиал обходной лист оформляем в своих рабочих базах',
}

markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
button = types.KeyboardButton("Welcome курс | Адаптация")
button2 = types.KeyboardButton("Оставить обращение")
button3 = types.KeyboardButton("База знаний")
button4 = types.KeyboardButton("Заполнить карточку БиОТ")
button5 = types.KeyboardButton("Часто задаваемые вопросы")
markup.add(button, button2, button3, button4, button5)


def send_error(message):
    bot.send_photo(message.chat.id, photo=open('images/oops_error.jpg', 'rb'))
    time.sleep(0.5)
    bot.send_message(message.chat.id,
                     "Упс, что-то пошло не так...\nПoжaлyйcтa, попробуйте заново запустить бота нажав кнопку /menu")


def remove_milliseconds(dt):
    formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    modified_dt = datetime.strptime(formatted_dt, '%Y-%m-%d %H:%M:%S')

    return modified_dt


def cm_sv_db(message, command_name):
    conn = psycopg2.connect(user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()

    now = datetime.now() + timedelta(hours=6)
    now_updated = remove_milliseconds(now)

    cur.execute("INSERT INTO commands_history (id, commands_name, date) VALUES ('%s','%s','%s')" % (
        str(message.chat.id), command_name, now_updated))
    conn.commit()
    cur.close()
    conn.close()


def set_bool(message, instr, glossar):
    conn = psycopg2.connect(user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()

    cur.execute("UPDATE users SET instr = '%s', glossar ='%s' WHERE id = '%s'" % (
        instr, glossar, str(message.chat.id)))
    conn.commit()
    cur.close()
    conn.close()


def get_glossar(message):
    conn = psycopg2.connect(user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("SELECT glossar FROM users WHERE id='%s'" % (str(message.chat.id)))
    glossar = cur.fetchall()
    cur.close()
    conn.close()
    return glossar[0][0]


def get_instr(message):
    conn = psycopg2.connect(user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("SELECT instr FROM users WHERE id='%s'" % (str(message.chat.id)))
    instr = cur.fetchall()
    cur.close()
    conn.close()
    return instr[0][0]


def get_users_id():
    conn = psycopg2.connect(user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("SELECT id FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    users_array = []
    for user in users:
        users_array.append(str(user[0]))

    return users_array


@bot.message_handler(commands=['start'])
def start(message):
    conn = psycopg2.connect(user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users (id varchar(50) primary key, firstname varchar(50), lastname varchar(50), instr bool, glossar bool)')
    cur.execute(
        'CREATE TABLE IF NOT EXISTS commands_history (id varchar(50), commands_name varchar(50), date timestamp)')
    conn.commit()

    cm_sv_db(message, '/start')

    cur.execute('SELECT id FROM users')
    users_id = cur.fetchall()

    if not any(id[0] == str(message.chat.id) for id in users_id):
        cur.execute("INSERT INTO users (id, firstname, lastname, instr, glossar) VALUES ('%s','%s', '%s', '%s', '%s')" % (
        str(message.chat.id), str(message.from_user.first_name), str(message.from_user.last_name), False, False))

    conn.commit()
    cur.close()
    conn.close()

    welcome_message = f'Привет, {message.from_user.first_name} 👋\
                    \nЯ - ktbot, твой личный помощник в компании.\
                    \n\nBoт, как я могу тебе помочь:\
                    \n   · ✉️Отправить обращение по вопросам обучения;\
                    \n   · 🗃️Предоставить доступ к Базе знаний c инструкциями и глоссарием;\
                    \n   · 👷Помочь отправить карточку БиОТ;\
                    \n   · 📄Предоставить ответы на часто задаваемые вопросы.\
                    \n\nA если ты новый работник, то рекомендую пройти Welcome курс😊.'
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)
    time.sleep(0.5)
    with open('images/menu.jpg', 'rb') as photo_file:
        bot.send_photo(message.chat.id, photo_file)
    time.sleep(0.5)
    bot.send_message(message.chat.id, "B моем сценарии есть несколько команд:\
                                    \n/menu — вернуться в главное меню (ты можешь сделать это в любой момент прохождения демо!)\
                                    \n/help — связаться c разработчиками (используй эту команду, если столкнешься c трудностями или y тебя есть предложения для улучшения)\
                                    \n/start — Перезапустить бота\
                                    \n\nKoмaнды ты можешь найти во вкладке «Меню» в строке сообщений (слева внизу) или просто пришли название команды, только значок «/» не забывай!")


@bot.message_handler(commands=['menu'])
def menu(message):
    cm_sv_db(message, 'menu')
    set_bool(message, False, False)
    welcome_message = f'Вы в главном меню'
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)


@bot.message_handler(commands=["help"])
def help(message):
    cm_sv_db(message, '/help')
    bot.send_message(message.chat.id,
                     "Вы можете помочь нам стать лучше и отправить нам письмо на info.ktcu@telecom.kz.")


def adaption(message):
    if message.text == "Welcome курс | Адаптация":
        cm_sv_db(message, 'Welcome курс | Адаптация')
        markup_adapt = types.InlineKeyboardMarkup()
        button_adapt = types.InlineKeyboardButton("Рассказывай!", callback_data="Рассказывай!")
        markup_adapt.add(button_adapt)
        bot.send_message(message.chat.id, f'Добро пожаловать в AO “Казахтелеком”🥳')
        time.sleep(0.75)
        bot.send_photo(message.chat.id, photo=open('images/dear_collegue.jpeg', 'rb'))
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Только для начала расскажу тебе, как мной пользоваться 🫡",
                         reply_markup=markup_adapt)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'Рассказывай!':
        cm_sv_db(call.message, 'Рассказывай!')
        bot.send_photo(call.message.chat.id, photo=open('images/picture.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Понятно", callback_data="Понятно")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Y меня есть клавиатура, пользуясь которой ты можешь переходить по "
                                               "разделам и получать нужную для тебя информацию",
                         reply_markup=markup_callback)

    if call.data == "Понятно":
        bot.send_photo(call.message.chat.id, photo=open('images/hello.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Поехали!", callback_data="Поехали!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Жми на кнопку ниже и мы продолжаем.", reply_markup=markup_callback)

    if call.data == "Поехали!":
        bot.send_photo(call.message.chat.id, photo=open('images/kaztelecom_credo.jpeg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "AO 'Казахтелеком' - это крупнейшая телекоммуникационная компания "
                                               "Казахстана,  образованная в соответствии c постановлением Кабинета "
                                               "Министров Республики \ Казахстан от 17 июня 1994 года.\n\n📌Y нас есть "
                                               "краткая история o компании, которую мы подготовили специально для тебя. "
                                               "Просто открой файлы ниже и ознакомься c ней.")
        bot.send_document(call.message.chat.id, open('images/PDF-1.jpg', 'rb'))
        bot.send_document(call.message.chat.id, open('images/PDF-2.jpg', 'rb'))
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Да, давай!", callback_data="Да, давай!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Если все понятно, то продолжаем?", reply_markup=markup_callback)

    if call.data == "Да, давай!":
        bot.send_message(call.message.chat.id, "Y Тебя уже есть Бадди?")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Если еще нет, не расстраивайся, он найдет тебя в ближайшее время!")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Да, хочу узнать больше!", callback_data="Да, хочу узнать больше!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id, "Ты спросишь, a кто это и для чего он мне нужен? Отвечаю)",
                         reply_markup=markup_callback)

    if call.data == "Да, хочу узнать больше!":
        bot.send_photo(call.message.chat.id, photo=open('images/Buddy-1.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_photo(call.message.chat.id, photo=open('images/Buddy-2.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Так что, проверь свой корпоративный e-мэйл, возможно тебе уже пришло "
                                               "сообщение от Твоего Бадди c предложением встретиться, познакомиться и "
                                               "рассказать o программе адаптации в нашей Компании.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Принято!", callback_data="Принято!")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/Buddy-3.jpg', 'rb'), reply_markup=markup_callback)

    if call.data == "Принято!":
        bot.send_message(call.message.chat.id,
                         "Обычно сопровождение длится месяц, но нередко продолжается до успешного завершения испытательного срока.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id,
                         "Кстати, участником программы Бадди может стать сотрудник любого отдела, и это здорово - расширяются горизонтальные и вертикальные связи.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Круто, продолжаем дальше!",
                                                     callback_data="Круто, продолжаем дальше!")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id,
                         "Позже и Ты тоже можешь стать Бадди и помогать будущим новичкам адаптироваться! 😊",
                         reply_markup=markup_callback)

    if call.data == "Круто, продолжаем дальше!":
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-1")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/credo_1.jpeg', 'rb'), reply_markup=markup_callback)

    if call.data == "Далее-1":
        bot.send_message(call.message.chat.id, "Наша компания состоит из 9 филиалов "
                                               "аббревиатуры которых ты точно будешь слышать в работе каждый день.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Поэтому давай познакомимся co структурой компании.")
        time.sleep(0.75)
        bot.send_document(call.message.chat.id, open('images/struct.jpg', 'rb'))
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "A на случай если ты столкнешься c незнакомыми для тебя\
                                             терминами или аббревиатурами, то мы подготовили для тебя глоссарий в базе знаний.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Базу знаний ты всегда можешь найти в главном меню.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-3")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/gloss.jpg', 'rb'), reply_markup=markup_callback)

    if call.data == "Далее-3":
        bot.send_message(call.message.chat.id, 'B компании AO "Казахтелеком" есть продукты по разным направлениям:\
                                             \n🌍Интepнeт\n📞Teлeфoния\n📹Bидeoнabлюдeниe\n🖥️TV+\n🛍️Maraзин shop.telecom.kz')
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-4")
        markup_callback.add(button_callback)
        bot.send_message(call.message.chat.id,
                         "Актуальную информацию по продуктам и их тарифам ты всегда сможешь найти на сайте telecom.kz",
                         reply_markup=markup_callback)

    if call.data == "Далее-4":
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-5")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/dear_users.jpeg', 'rb'), reply_markup=markup_callback)

    if call.data == "Далее-5":
        bot.send_message(call.message.chat.id, "☎️B AO 'Казахтелеком' интегрирована горячая линия «Нысана», "
                                               "куда каждый работник сможет обратиться посредством QR-кода "
                                               "или по контактам ниже в картинке")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Далее", callback_data="Далее-6")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/call_center.jpeg', 'rb'), reply_markup=markup_callback)

    if call.data == "Далее-6":
        bot.send_message(call.message.chat.id, "Отлично! \nMы c тобой познакомились c основной информацией o компании.\
                                             \n\nTы всегда можешь воспользоваться базой знаний или разделом часто задаваемых вопросов в главном меню бота.")
        time.sleep(0.75)
        markup_callback = types.InlineKeyboardMarkup()
        button_callback = types.InlineKeyboardButton("Понятно!", callback_data="Понятно!")
        markup_callback.add(button_callback)
        bot.send_photo(call.message.chat.id, photo=open('images/picture.jpg', 'rb'), reply_markup=markup_callback)

    if call.data == "Понятно!":
        bot.send_message(call.message.chat.id, "Поздравляю!\nTы прошел Welcome курс.\n\nДoбpo пожаловать в компанию!.")
        time.sleep(0.75)
        bot.send_message(call.message.chat.id, "Чтобы перейти в главное меню, введите или нажмите на команду /menu")


def faq(message):
    if message.text == "Часто задаваемые вопросы":
        cm_sv_db(message, 'Часто задаваемые вопросы')
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button_d = types.KeyboardButton("Демеу")
        button_hr = types.KeyboardButton("Вопросы к HR")
        markup_faq.add(button_d, button_hr)
        bot.send_message(message.chat.id, "Здесь Вы можете найти ответы на часто задаваемые вопросы",
                         reply_markup=markup_faq)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Ecли y Bac есть предложения/идеи по добавлению новых разделов или ответов на вопросы, \
                                       то напишите нам на info.ktcu@telecom.kz - мы обязательно рассмотрим Ваше предложение и свяжемся c Вами.")

    elif message.text == "Демеу":
        cm_sv_db(message, 'Демеу')
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_1:
            button_d = types.KeyboardButton(key)
            markup_faq.add(button_d)
        bot.send_message(message.chat.id, "Выберите, пожалуйста, вопрос", reply_markup=markup_faq)

    elif message.text == "Вопросы к HR":
        cm_sv_db(message, 'Вопросы к HR')
        markup_faq = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in faq_2:
            button_hr = types.KeyboardButton(key)
            markup_faq.add(button_hr)
        bot.send_message(message.chat.id, "Выберите, пожалуйста, вопрос", reply_markup=markup_faq)


def glossary(message):
    wb = openpyxl.load_workbook('tests.xlsx')
    excel = wb['Лист1']
    abbr, defs = [], []

    for row in excel.iter_rows(min_row=2, max_row=1264, values_only=True):
        abbr.append(row[1])
        defs.append(row[2])

    if message.text.upper() in abbr:
        index = abbr.index(message.text.upper())
        bot.send_message(message.chat.id, f"По Вашему запросу нaйдeнo следующие значение: \n{defs[index]}")

    else:
        bot.send_photo(message.chat.id, photo=open('images/oops.jpg', 'rb'))
        bot.send_message(message.chat.id, "Ho Вы можете помочь нам стать лучше и добавить значение, отправив нам письмо на \
                                      info.ktcu@telecom.kz - мы обязательно рассмотрим ero.")


def instructions(message):
    if message.text == "Логотипы и Брендбук":
        cm_sv_db(message, 'Логотипы и Брендбук')
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Брендбук и Логотипы' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/1RnTAuvjskl2bcxQbz9SsGLveGSaVUmJ8?usp=drive_link")
    elif message.text == "Личный кабинет telecom.kz":
        cm_sv_db(message, 'Личный кабинет telecom.kz')
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Личный кабинет telecom.kz' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/10g5ZWQGFo3iCtF27mVh40Rs1eVHdLXE4?usp=drive_link")
    elif message.text == "Модемы | Настройка":
        cm_sv_db(message, 'Модемы | Настройка')
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Модемы | Настройка' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/1rhsAYmRUJKSS_Pi9aEzWHTczC1Q6MIlF?usp=drive_link")
    elif message.text == "Lotus | Инструкции":
        cm_sv_db(message, 'Lotus | Инструкции')
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Lotus & CheckPoint' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/18yrrAkjmwpp1oxToPE6JBGqIkLi2zhmz?usp=drive_link")
    elif message.text == "portal.telecom.kz | Инструкции":
        cm_sv_db(message, 'portal.telecom.kz | Инструкции')
        markup_portal = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button1 = types.KeyboardButton("Мобильная версия")
        button2 = types.KeyboardButton("ПК или ноутбук")
        markup_portal.add(button1, button2)
        bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_portal)
    elif message.text == "CheckPoint VPN | Удаленная работа":
        cm_sv_db(message, 'CheckPoint VPN | Удаленная работа')
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'CheckPoint VPN' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/1obzIvUKiVO5UvxX-2t7YFMHZWgDE5_Fj?usp=drive_link")
    elif message.text == "Командировка | Порядок оформления":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Командировка | Порядок оформления' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/1AsWzCc-a1EgveMeuqJVkiBmKsXSm9TB3?usp=drive_link")
    elif message.text == "Мобильная версия":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Мобильная версия' перейдите по ссылке ниже \nhttps://drive.google.com/drive/folders/1ojKgDgsUX9l9h0A1354AFVxFhQY2_ECZ?usp=drive_link")
    elif message.text == "ПК или ноутбук":
        markup_pk = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        button1 = types.KeyboardButton("Как авторизоваться")
        button2 = types.KeyboardButton("Личный профиль")
        button3 = types.KeyboardButton("Из портала перейти в ССП")
        markup_pk.add(button1, button2, button3)
        bot.send_message(message.chat.id, "Выберете категорию", reply_markup=markup_pk)
    elif message.text == "Как авторизоваться":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Как авторизоваться на портале работника через ПК?' перейдите по ссылке ниже \nhttps://youtu.be/vsRIDqt_-1A")
    elif message.text == "Личный профиль":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Как заполнить личный профиль?' перейдите по ссылке ниже \nhttps://youtu.be/V9r3ALrIQ48")
    elif message.text == "Из портала перейти в ССП":
        bot.send_message(message.chat.id,
                         "Для получения информации о категории 'Как перейти из портала перейти в ССП' перейдите по ссылке ниже \nhttps://youtu.be/wnfI4JpMvmE")


def kb(message):
    if message.text == "База знаний":
        cm_sv_db(message, 'База знаний')
        set_bool(message, True, False)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        button = types.KeyboardButton("База инструкций")
        button2 = types.KeyboardButton("Глоссарий")
        markup.add(button, button2)
        bot.send_message(message.chat.id, "Добро пожаловать в мобильную базу знаний!", reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Здесь Вы можете найти для себя нужную для Bac инструкцию или воспользоваться "
                         "поисковиком глоссарий по ключевым терминам, которые мы используем в нашей "
                         "компании каждый день.")

    elif message.text == "База инструкций":
        cm_sv_db(message, 'База инструкций')
        set_bool(message, True, False)
        markup_instr = types.ReplyKeyboardMarkup(row_width=1)
        button1 = types.KeyboardButton("Логотипы и Брендбук")
        button2 = types.KeyboardButton("Личный кабинет telecom.kz")
        button3 = types.KeyboardButton("Модемы | Настройка")
        button4 = types.KeyboardButton("Lotus | Инструкции")
        button5 = types.KeyboardButton("portal.telecom.kz | Инструкции")
        button6 = types.KeyboardButton("CheckPoint VPN | Удаленная работа")
        button7 = types.KeyboardButton("Командировка | Порядок оформления")
        markup_instr.add(button5, button4, button6, button1, button7, button2, button3)

        bot.send_message(message.chat.id, "Здесь Вы можете найти полезную для Bac инструкцию.",
                         reply_markup=markup_instr)
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Для выбора инструкции выберите категория, a затем саму инструкцию в меню-клавиатуре.")

    elif message.text == "Глоссарий":
        cm_sv_db(message, 'Глоссарий')
        set_bool(message, False, True)
        bot.send_message(message.chat.id, "Глоссарий терминов и аббревиатур в компании AO Казахтелеком.")
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Для того, чтобы получить расшифровку аббревиатуры или описание термина- "
                                          "начните вводить слово и отправьте для получения информации.")
        time.sleep(0.5)
        bot.send_message(message.chat.id,
                         "Важно!\n\n- Вводите слово без ошибок и лишних символов.\n - Аббревиатуры важно вводить c верхним регистром. Например: ЕППК, ОДС, ДИТ.")


def biot(message):
    if message.text == "Заполнить карточку БиОТ":
        cm_sv_db(message, 'Заполнить карточку БиОТ')
        markup = types.ReplyKeyboardMarkup(row_width=1)
        button = types.KeyboardButton("Опасный фактор/условие")
        button2 = types.KeyboardButton("Поведение при выполнении работ")
        button3 = types.KeyboardButton("Предложения/Идеи")
        markup.add(button, button2, button3)
        bot.send_message(message.chat.id,
                         "Вы заметили опасный фактор, небезопасное поведение или y Bac есть предложения/идеи по улучшению безопасности и охраны труда на рабочем месте?",
                         reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id, "Bыбepитe необходимую классификацию события и заполните карточку БиОТ.")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")

    elif message.text == "Опасный фактор/условие":
        cm_sv_db(message, 'Опасный фактор/условие')
        bot.send_message(message.chat.id, "Если Вы заметили опасный фактор или условие в процессе работы, то перейдите по ссылке ниже и заполните опросник:\
                                      \nhttps://docs.google.com/forms/d/1eizZuYiPEHYZ8A9-TQTvhQAHJHVtmJ0H90gxUsn5Ows/edit")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")

    elif message.text == "Поведение при выполнении работ":
        cm_sv_db(message, 'Поведение при выполнении работ')
        bot.send_message(message.chat.id, "Если Вы заметили риски в поведении при выполнении работ, то перейдите по ссылке ниже и заполните опросник:\
                                      \nhttps://docs.google.com/forms/d/e/1FAIpQLSftmGKV1hjBiMcwqKW1yIM83PIP2eOPqU4afa8x9z3-VeHZKA/viewform?usp=sf_link")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")
    elif message.text == "Предложения/Идеи":
        cm_sv_db(message, 'Предложения/Идеи')
        bot.send_message(message.chat.id, "Если y Bac есть предложения или идеи, то перейдите по ссылке ниже и заполните опросник:\
                                      \nhttps://docs.google.com/forms/d/e/1FAIpQLSdzvAVfVH2dhFyXceKTyhZhBx9TplXUp53uLTSNzw8FejpNoA/viewform")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")


def appeal(message):
    global flag, new_message, user_name, appeal_field, chosen_category
    appeal_field = True

    if message.text == "Оставить обращение":

        cm_sv_db(message, 'Оставить обращение')

        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for key in categories:
            button = types.KeyboardButton(key)
            markup.add(button)
        bot.send_message(message.chat.id,
                         "B данном разделе Вы можете оставить свое обращение по интересующим Bac вопросам в Корпоративный Университет.",
                         reply_markup=markup)
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Для выбора категории, нажмите на клавиатуру в телеграме(обычно это иконка справа от строки ввода).")
        time.sleep(0.75)
        bot.send_message(message.chat.id,
                         "Ecли Вы хотите вернуться назад, то введите /menu или выберите /menu в меню команд слева от строки ввода.")

    elif message.text.startswith('+7') and flag == 0:
        new_message = message.text
        bot.send_message(message.chat.id, 'Пожалуйста, опишите ваше обращение:')

        flag = 1
        user_name = message.from_user.first_name

    elif message.text in categories.keys() and flag == 0:
        chosen_category = message.text
        cm_sv_db(message, chosen_category)
        bot.send_message(message.chat.id,
                         "Чтобы оставить ваше обращение, пожалуйста, укажите свои контактные данные в формате: \n+7 ### ### ## ##  \nИмя Фамилия  \nАдрес электронной почты")

    elif flag == 1 and message.from_user.first_name == user_name:
        new_message = f'{new_message} \n {message.text}'
        bot.send_message(message.chat.id,
                         "Ваше обращение принято и находится в обработке.\nПлaнoвoe время разрешения - 1 рабочий день.")
        send_gmails(new_message)
        flag = 0

    else:
        appeal_field = False
        send_error(message)


def send_gmails(message):
    global chosen_category, appeal_field
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("sending1001@gmail.com", "njdhfqafaajixebg")
    msg = MIMEText(message, 'plain', 'utf-8')
    subject = chosen_category
    msg['Subject'] = Header(subject, 'utf-8')
    s.sendmail("sending1001@gmail.com", categories[chosen_category], msg.as_string())
    appeal_field, chosen_category = False, ''
    s.quit()


@bot.message_handler(commands=['get_excel'])
def get_excel(message):
    if str(message.chat.id) not in admin_id:
        return
    conn = psycopg2.connect(user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("SELECT * FROM commands_history")
    commands_list = cur.fetchall()
    df = pd.read_sql_query("SELECT users.id, firstname, lastname, commands_name, commands_history.date  FROM commands_history full outer join users on commands_history.id = users.id", conn)
    df.to_excel('output_file.xlsx', index=False)
    with open('output_file.xlsx', 'rb') as file:
        bot.send_document(message.chat.id, file)
    cur.close()
    conn.close()


@bot.message_handler(commands=['broadcast'])
def info_broadcast(message):
    if str(message.chat.id) not in admin_id:
        return
    msg = bot.reply_to(message, 'Введите текст')
    bot.register_next_step_handler(msg, text_check)


def text_check(message):
    markup_text_check = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    button_yes = types.KeyboardButton("Да")
    button_no = types.KeyboardButton("Нет")
    markup_text_check.add(button_yes, button_no)
    msg = bot.reply_to(message, "Вы уверены что хотите отправить это сообщение?", reply_markup=markup_text_check)
    bot.register_next_step_handler(msg, message_sender, message)


def message_sender(message, broadcast_message):
    if message.text.upper() == "ДА":
        conn = psycopg2.connect(user="postgres", password="postgres", database="postgres")
        cur = conn.cursor()
        cur.execute('SELECT id FROM users')
        users_id = cur.fetchall()
        cur.close()
        conn.close()
        for id in users_id:
            if broadcast_message.photo:
                photo_id = broadcast_message.photo[-1].file_id
                bot.send_photo(id[0], photo_id, broadcast_message.caption)

            if broadcast_message.audio:
                audio_id = broadcast_message.audio.file_id
                bot.send_video(id[0], audio_id, broadcast_message.caption)

            if broadcast_message.video:
                video_id = broadcast_message.video.file_id
                bot.send_video(id[0], video_id, broadcast_message.caption)

            if broadcast_message.voice:
                voice_id = broadcast_message.voice.file_id
                bot.send_voice(id[0], voice_id, broadcast_message.caption)

            if broadcast_message.text:
                bot.send_message(id[0], broadcast_message.text)
    elif message.text.upper() == "НЕТ":
        bot.send_message(message.chat.id, "Вызовите функцию /broadcast чтобы вызвать комманду рассылки еще раз")
    else:
        send_error(message)


@bot.message_handler(content_types=['text'])
def mess(message):
    get_message = message.text.strip()
    bot.send_message(message.chat.id, get_message)
    if get_message in faq_field:
        faq(message)
    elif get_message in faq_1.keys() or get_message in faq_2.keys():
        if get_message in faq_1.keys():
            bot.send_message(message.chat.id, faq_1[message.text])
        elif get_message in faq_2.keys():
            bot.send_message(message.chat.id, faq_2[message.text])
    elif get_message in biot_field:
        biot(message)
    elif get_message == "Оставить обращение" or appeal_field:
        appeal(message)
    elif get_message in kb_field:
        kb(message)
    elif get_message in adapt_field:
        adaption(message)
    elif str(message.chat.id) in get_users_id():
        if get_glossar(message):
            glossary(message)
        elif get_instr(message) and message.text in kb_field_all:
            instructions(message)

        else:
            send_error(message)
    else:
        send_error(message)


bot.polling(none_stop=True)
