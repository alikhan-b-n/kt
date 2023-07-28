import psycopg2
from datetime import datetime, timedelta
from email.header import Header
import smtplib
from email.mime.text import MIMEText


def remove_milliseconds(dt):
    formatted_dt = dt.strftime('%Y-%m-%d %H:%M:%S')
    modified_dt = datetime.strptime(formatted_dt, '%Y-%m-%d %H:%M:%S')

    return modified_dt

def cm_sv_db(message, command_name):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()

    now = datetime.now() + timedelta(hours=6)
    now_updated = remove_milliseconds(now)

    cur.execute("INSERT INTO commands_history (id, commands_name, date) VALUES ('%s','%s','%s')" % (
        str(message.chat.id), command_name, now_updated))
    conn.commit()
    cur.close()
    conn.close()


def set_bool(message, instr, glossar):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()

    cur.execute("UPDATE users_info SET instr = '%s', glossar ='%s' WHERE id = '%s'" % (
        instr, glossar, str(message.chat.id)))
    conn.commit()
    cur.close()
    conn.close()


def get_glossar(message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("SELECT glossar FROM users_info WHERE id='%s'" % (str(message.chat.id)))
    glossar = cur.fetchall()
    cur.close()
    conn.close()
    return glossar[0][0]


def get_instr(message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("SELECT instr FROM users_info WHERE id='%s'" % (str(message.chat.id)))
    instr = cur.fetchall()
    cur.close()
    conn.close()
    return instr[0][0]


def get_users_id():
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("SELECT id FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    users_array = []
    for user in users:
        users_array.append(str(user[0]))
    return users_array


def set_appeal_field(message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("UPDATE users_info SET appeal_field = '%s' WHERE id='%s'" % (True, str(message.chat.id)))
    conn.commit()
    cur.close()
    conn.close()


def get_appeal_message(message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("SELECT new_message FROM users_info WHERE id='%s'" % (str(message.chat.id)))
    category = cur.fetchall()
    cur.close()
    conn.close()
    return category[0][0]


def set_appeal_message(message, appeal_message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("UPDATE users_info SET new_message = '%s' WHERE id='%s'" % (appeal_message, str(message.chat.id)))
    conn.commit()
    cur.close()
    conn.close()

def set_chosen_category(message, category):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("UPDATE users_info SET chosen_category = '%s' WHERE id='%s'" % (category, str(message.chat.id)))
    conn.commit()
    cur.close()
    conn.close()

def get_appeal_field(message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("SELECT appeal_field FROM users_info WHERE id='%s'" % (str(message.chat.id)))
    appeal_field = cur.fetchall()
    cur.close()
    conn.close()
    return appeal_field[0][0]

def clear_appeals(message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("UPDATE users_info SET new_message = '%s', chosen_category = '%s', appeal_field = '%s' WHERE id='%s'" %
                ('', '', False, str(message.chat.id)))
    conn.commit()
    cur.close()
    conn.close()

def get_chosen_category(message):
    conn = psycopg2.connect(host='db', user="postgres", password="postgres", database="postgres")
    cur = conn.cursor()
    cur.execute("SELECT chosen_category FROM users_info WHERE id='%s'" % (str(message.chat.id)))
    category = cur.fetchall()
    cur.close()
    conn.close()
    return category[0][0]


def send_gmails(message, categories, chosen_category):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("sending1001@gmail.com", "njdhfqafaajixebg")
    msg = MIMEText(message, 'plain', 'utf-8')
    subject = chosen_category
    msg['Subject'] = Header(subject, 'utf-8')
    s.sendmail("sending1001@gmail.com", categories[chosen_category], msg.as_string())
    s.quit() 


def addIfNotExistUser(message):
    conn = psycopg2.connect(user="postgres", password="j7hPC180")
    cur = conn.cursor()

    cur.execute('SELECT id FROM users')
    users_id = cur.fetchall()

    if not any(id[0] == str(message.chat.id) for id in users_id):
        cur.execute("INSERT INTO users (id, username, lastname, firstname, language) "
                    "VALUES ('%s','%s', '%s', '%s', '%s')" % (str(message.chat.id), str(message.from_user.username),
                                                              str(message.from_user.first_name),
                                                              str(message.from_user.last_name), 'n'))
        cur.execute("INSERT INTO users_info(id , instr , glossar, new_message, chosen_category, appeal_field ) "
                    "VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (str(message.chat.id), False, False, '', '', False))
    conn.commit()
    cur.close()
    conn.close()
