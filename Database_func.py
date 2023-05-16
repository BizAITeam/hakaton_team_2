import psycopg2


def Insert_message(text, date_time, messenger_user_id, messenger_channel_id):
    try:

        conn = psycopg2.connect(database="postgres",user="postgres",password="12345",host="localhost",port=5432)
        cur = conn.cursor()

        cur.execute('''INSERT INTO Messages (text, date_time, user_channel_id)
                       SELECT %s, %s, user_channel_id FROM users_channels INNER JOIN users ON users.user_id = users_channels.user_id
                       WHERE messenger_user_id = %s AND messenger_channel_id = %s;''', ( text, date_time, messenger_user_id, messenger_channel_id))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")
   


def Check_user(messenger_user_id):
    try:    
        conn = psycopg2.connect(database="postgres",user="postgres",password="12345",host="localhost",port=5432)
        cur = conn.cursor()
        cur.execute('''SELECT user_id FROM users WHERE messenger_user_id = %s;''', (messenger_user_id,))
        result = cur.fetchall()
        if result:
            check = True
        else:
            check = False
        cur.close()
        conn.close()
        return check
    except psycopg2.Error as e:
        print(f"Error: {e}")

def Check_user_channel(messenger_user_id, messenger_channel_id):
    try:   
        conn = psycopg2.connect(database="postgres",user="postgres",password="12345",host="localhost",port=5432)
        cur = conn.cursor()
        cur.execute('''SELECT user_channel_id FROM users_channels INNER JOIN users ON users.user_id = users_channels.user_id
                       WHERE messenger_user_id = %s AND messenger_channel_id = %s;''', ( messenger_user_id, messenger_channel_id))
        result = cur.fetchall()
        if result:
            check = True
        else:
            check = False
        cur.close()
        conn.close()
        return check
    except psycopg2.Error as e:
        print(f"Error: {e}")


def Insert_user(messenger_user_id, messenger_user_name, messenger):
    try:   
        conn = psycopg2.connect(database="postgres",user="postgres",password="12345",host="localhost",port=5432)
        cur = conn.cursor()
        cur.execute('''INSERT INTO users (messenger_user_id, messenger_user_name, messenger) VALUES (%s, %s, %s);''', (messenger_user_id, messenger_user_name, messenger))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")

def Insert_user_channel(messenger_user_id, messenger_channel_id, channel_type):
    try:    
        conn = psycopg2.connect(database="postgres",user="postgres",password="12345",host="localhost",port=5432)
        cur = conn.cursor()
        cur.execute('''INSERT INTO users_channels (messenger_channel_id, channel_type, user_id) 
                       SELECT %s, %s, user_id FROM users
                       WHERE messenger_user_id = %s;''', ( messenger_channel_id, channel_type, messenger_user_id))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")


def Delete_messenge(text, messenger_user_id, messenger_channel_id):
    try:
        conn = psycopg2.connect(database="postgres",user="postgres",password="12345",host="localhost",port=5432)
        cur = conn.cursor()
        cur.execute('''DELETE FROM messages
                       USING users, users_channels
                       WHERE users.user_id = users_channels.user_id
                       AND users_channels.user_channel_id = messages.user_channel_id
                       AND text = %s
                       AND messenger_channel_id = %s
                       AND messenger_user_id = %s;''', (text , messenger_channel_id, messenger_user_id))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")

    

def Delete_all_messenges(messenger_channel_id):
    try:
        conn = psycopg2.connect(database="postgres",user="postgres",password="12345",host="localhost",port=5432)
        cur = conn.cursor()
        cur.execute('''DELETE FROM messages
                       USING users, users_channels
                       WHERE users.user_id = users_channels.user_id
                       AND users_channels.user_channel_id = messages.user_channel_id
                       AND messenger_channel_id = %s;''', (messenger_channel_id,))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error: {e}")

    

def history(messenger_channel_id):
    try:
        conn = psycopg2.connect(database="postgres",user="postgres",password="12345",host="localhost",port=5432)
        cur = conn.cursor()
        cur.execute('''SELECT messenger_user_name , text, messenger
                       FROM messages INNER JOIN users_channels ON messages.user_channel_id = users_channels.user_channel_id
                       INNER JOIN users ON users.user_id = users_channels.user_id
                       WHERE messenger_channel_id = %s;''', (messenger_channel_id,))
        rows = cur.fetchall()
        if rows:
            text = ""
            for row in rows:
                text += f"{row[0]}: {row[1]}\n"
            messenger = rows[0][2]
        else:
            cur.execute('''SELECT messenger FROM users_channels INNER JOIN users ON users.user_id = users_channels.user_id
                           WHERE messenger_channel_id = %s;''', (messenger_channel_id,))
            messenger = cur.fetchall()[0][0]
            text = "Channel history does not exist yet"
        cur.close()
        conn.close()
        return text, messenger_channel_id, messenger 
    except psycopg2.Error as e:
        print(f"Error: {e}")
    





    

