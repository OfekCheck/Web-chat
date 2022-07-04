import sqlite3
import datetime

"""" 
All tables
Messages  , Person  , Rooms
"""
#creates a new room if does not exist  
def new_room(name,is_limit):
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    room_detail = (name,is_limit)
    c.execute("INSERT INTO Rooms(Name,IsLimit) VALUES(?,?);",room_detail)
    conn.commit()
    conn.close()

#Adds a new person to the room
def new_person(user_name,room,photo):
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    room_id = get_room_id(room)
    person_detail = (user_name,room_id,photo)
    c.execute("INSERT INTO Person(userName,IdRoom,Photo) VALUES(?,?,?);",person_detail)
    conn.commit()
    conn.close()

#All messages for specific room
def all_messages(room):
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    room_id = get_room_id(room)
    c.execute("SELECT * FROM Messages WHERE RoomID = (?)",(room_id,))
    data = c.fetchall()
    conn.commit()
    conn.close()
    return data

#Insert message to table when user send new message
def new_message(room,message,username):
    current_time = datetime.datetime.now()
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    room_id = get_room_id(room)
    message_details = (current_time,room_id,message['msg'],username,)
    c.execute("INSERT INTO Messages(Time,RoomID,Message,Username) VALUES(?,?,?,?);", message_details)    
    conn.commit()
    conn.close()

#Check if a room is exists
def exist_room(room):
    room_id = get_room_id(room)
    #RoomNum= c.fetchall()[0][0]
    if room_id == None:
        return False
    else:
        return True

#close room if empty
def close_room(room):
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    room_id = get_room_id(room)
    c.execute("DELETE FROM Rooms WHERE roomId=(?);",(room_id,))
    conn.commit()
    c.execute("DELETE FROM Person WHERE IdRoom=(?);",(room_id,))
    conn.commit()
    conn.close()

#Check if in the room has place to more people
def users_cap(room):
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    room_id = get_room_id(room)
    #Check that the room exists 
    if room_id != None and room_id != '':
        c.execute("SELECT IsLimit FROM Rooms WHERE Name = (?)",(room,))
        room_limit = c.fetchall()[0][0]
        if room_limit == 'UNLIMITED':
            conn.commit()
            conn.close()
            return True
        c.execute("SELECT COUNT (*) FROM Person WHERE IdRoom = (?)",(room_id,))
        count_users = c.fetchall()[0][0]
        room_limit = int(room_limit)
        users_left = room_limit - count_users
        #If usersLeft greater than 0 it means there there is place for more user/users
        if users_left <= 0:
            conn.commit()
            conn.close()
            return "The room is full"
        conn.commit()
        conn.close()        
        return True            
    else:
        conn.commit()
        conn.close()
        return "The room does not exsit"

#Check if username exist in table
def user_appear(username):
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM Person WHERE userName = (?);",(username,))
    if len(c.fetchall()) > 0:
        conn.close()
        return True
    return False

#Delete user after he left the room
def left_user(room,username):
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    room_id = get_room_id(room)
    data = (username,room_id)
    c.execute("DELETE FROM Person WHERE userName=(?) AND IdRoom = (?);",(data))
    conn.commit()
    conn.close()
    
#Return room limit 
def limit(room):
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT IsLimit FROM Rooms WHERE Name = (?)",(room,))
    room_limit = c.fetchall()[0][0]
    conn.commit()
    conn.close()
    return room_limit

#Check if there is user in the room
def exist_user(room,username):
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    room_id = get_room_id(room)
    if room_id != None:
        c.execute("SELECT userName,Photo FROM Person WHERE IdRoom=(?) AND userName = (?)",(room_id,username))
        data = c.fetchall()
        conn.commit()
        conn.close()
    else:
        return False
    if len(data) == 0:
        return False
    return True

#Return all room users
def room_users(room):
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    room_id = get_room_id(room)
    if room_id != None:
        c.execute("SELECT userName,Photo FROM Person WHERE IdRoom=(?)",(room_id,))
        data = c.fetchall()
        conn.commit()
        conn.close()
        return data
    return 'There is a problem, please try again later'

#Return room id by getting the room name
def get_room_id(room):
    conn = sqlite3.connect('Chat.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT roomId FROM Rooms WHERE Name = (?)",(room,))
    room_num = c.fetchone()
    if room_num == None:
        conn.commit()
        conn.close()
        return None
    conn.commit()
    conn.close()
    return room_num[0]

#conn = sqlite3.connect('Chat.db', check_same_thread=False)
#c = conn.cursor()
#c.execute("SELECT * FROM Rooms")
#conn.commit()