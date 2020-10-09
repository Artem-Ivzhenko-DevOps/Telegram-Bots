import pymysql


class Connect(object):

    def __init__(self, bot, server_ip, login, password, database, chat_id,sql):
        self.bot = bot
        self.server_ip = server_ip
        self.login = login
        self.password = password
        self.database = database
        self.chat_id = chat_id
        self.sql = sql

    def connect_to_mysql(self, change_menu):
        db, cursor = self.try_to_connect()
        try:
            cursor.execute("show tables")
            db.commit()
            data = cursor.fetchall()
            for i in data:
                self.bot.send_message(self.chat_id, str(i)[1:-1])
        finally:
            db.close()
        self.bot.send_message(self.chat_id, 'Edit Menu', reply_markup=change_menu)

    def delete_from_table(self, msg, change_menu):
        db, cursor = self.try_to_connect()
        msg_text = msg.text.split(' ')
        table, attribute = msg_text[0], msg_text[1]
        sql = "delete from {0} where id={1}".format(table, attribute)
        try:
            cursor.execute(sql)
            db.commit()
        except pymysql.err.InternalError as e:
            self.bot.send_message(self.chat_id, e.args[1])
        finally:
            db.close()
        self.bot.send_message(self.chat_id, 'Edit Menu', reply_markup=change_menu)

    def insert_into_table(self, msg, change_menu):
        db, cursor = self.try_to_connect()
        msg_text = msg.text.split(' ')
        table = msg_text[0]
        values = msg_text[1:-1]
        sql = "insert into {0} values({1})".format(table, values)
        try:
            with db.cursor() as cursor:
                cursor.execute(sql)
                db.commit()
        except pymysql.err.InternalError as e:
            if e.args[1].startswith("Access denied for"):
                self.bot.send_message(msg.chat.id, e.args[1])
        finally:
            db.close()
        self.bot.send_message(self.chat_id, 'Edit Menu', reply_markup=change_menu)

    def send_command(self, call):
        db, cursor = self.try_to_connect()
        self.bot.edit_message_text(chat_id=self.chat_id,
                                   message_id=call.message.message_id,
                                   text="Input sql command")
        try:
            cursor.execute(self.sql)
        except pymysql.err.ProgrammingError as e:
            if e.args[1].startswith("You have an error in your SQL syntax"):
                self.bot.send_message(id, str(e.args[1]))
        finally:
            db.close()

    def dbname_read(self, msg, step):
        step += 1
        self.database = msg.text
        self.bot.send_message(msg.chat.id,
                              'Connecting...')
        self.connect_to_mysql(msg.chat.id)
        return step

    def login_read(self, msg, step):
        step += 1
        self.login = msg.text
        self.bot.send_message(msg.chat.id,
                              'Input password')
        return step

    def password_read(self, msg, step, menu):
        step += 1
        self.password = msg.text
        self.bot.send_message(msg.chat.id,
                              'Main Menu', reply_markup=menu)

    def try_to_connect(self):
        try:
            db = pymysql.connect(host=self.server_ip,
                                 user=self.login,
                                 password=self.password,
                                 db=self.database,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
            cursor = db.cursor()
            return db, cursor
        except pymysql.err.IntegrityError as e:
            self.bot.send_message(id, e.args[1])
