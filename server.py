from socket import *
from flask import *
from flask_socketio import *
from flask_session import Session
import os
import DBManage


#Starting the flask + session
app = Flask(__name__ , template_folder='template')
app.debug = True
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False)

#All routes
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/About')
def about():
    return render_template('About.html')

@app.route('/NewRoom')
def new_room():
    return render_template('NewRoom.html')

#When a user creates a new room
@app.route('/chat',methods=['GET','POST'])
def create_room():
    if(request.method !='POST'):
        return render_template('NewRoom.html')
    username = request.form['username'].lower()
    username = username[:5].strip()
    room = request.form['room'].lower()
    exist_room = DBManage.exist_room(room)
    user_appear = DBManage.user_appear(username)
    error = "YOU TYPED ROOM THAT ALREADY EXISTS"
    #Check if the room does not exist in the database 
    if exist_room:
        if(DBManage.exist_user(room,username)):
            all_messages = DBManage.all_messages(room)
            return render_template('chat.html', session = session,all_messages = all_messages)
        return render_template('NewRoom.html', error=error)
    #Check if user does not exist in database
    if user_appear:
        error = "THE USERNAME YOU TYPED ALREADY EXISTS"
        return render_template('NewRoom.html', error=error)
    #Check if user typed a limit 0/00/000/0000 or typed nothing, set a limit to unlimited
    limit = request.form['limit']
    starts_zero = True
    if limit == '' or int(limit) == 0:
        limit = 'UNLIMITED'
        starts_zero = False
    else:
        for char in limit:
            if starts_zero and int(char) == 0:
                limit = limit.replace("0", "")
            else:
                starts_zero = False
    session['limit'] = limit 
    if request.form['Choose_Avatar'] == 'Women':
        session['image'] = 'static/WomenAvatar.jpg'

    elif request.form.get('Choose_Avatar') == 'Men':
        session['image'] = 'static/ManAvatar.jpg'

    elif request.form.get('Choose_Avatar') == 'Own':
        image = request.files['getFile']
        file_name = image.filename
        if file_name.lower().endswith(('.png')):
            end_with = ".png"
        elif file_name.lower().endswith(('.jpg')):
            end_with = ".jpg"
        elif file_name.lower().endswith(('.jpeg')):
            end_with = ".jpeg"
        elif file_name.lower().endswith(('.webp')):
            end_with = ".webp"
        else:
            wrong_image = "There is something wrong with the photo you uploaded, please try another image"
            return render_template('NewRoom.html', error=wrong_image)
        session['image'] = 'static/images/' + username + end_with
        new_image = open("static/images/" + username + end_with,"wb")
        new_image.write(image.read())
        new_image.close()
    else:
        session['image'] = 'static/unknown.png'
    image = session['image']
    room = room[:5].strip()
    DBManage.new_room(room,limit)
    DBManage.new_person(username,room,image)
    #Store the data in session
    session['username'] = username
    session['room'] = room
    return render_template('chat.html', session = session)
        
#When a user joins an existing room
@app.route('/joinedchat', methods=['GET', 'POST'])
def join_chat():
    if(request.method !='POST'):
        if(session.get('username') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))
    not_exist = "The room you typed does not exist Would you like to open a room?"
    username = request.form['username'].lower() 
    username = username[:5].strip()
    room = request.form['room'].lower()
    room = room[:5].strip()
    session['username'] = username
    session['room'] = room
    room_exist = DBManage.exist_room(room)
    user_exist = DBManage.exist_user(room,username)
    user_appear = DBManage.user_appear(username)
    #Check if room exists in database        
    if not room_exist:
        return render_template('index.html', not_exist=not_exist)
    #Check if user does not exist in room to check if it is'nt a page refresh
    if user_exist:
        #When user refresh the page
        data = DBManage.all_messages(room)
        return render_template('chat.html', session = session,all_messages = data)
    #Check if user does not appear in database to enable the username
    if user_appear:
        not_exist = "THE USERNAME YOU TYPED ALREADY EXISTS"
        return render_template('index.html', not_exist=not_exist)
    is_not_full = DBManage.users_cap(room)
    if is_not_full != True:
        #If the room is full raise a message
        not_exist = is_not_full
        return render_template('index.html', not_exist=not_exist)
    #Set session to the image selected by the user
    if request.form['Choose_Avatar'] == 'Women':
        session['image'] = 'static/WomenAvatar.jpg'

    elif request.form.get('Choose_Avatar') == 'Men':
        session['image'] = 'static/ManAvatar.jpg'

    elif request.form.get('Choose_Avatar') == 'Own':
        image = request.files['getFile']
        file_name = image.filename
        if file_name.lower().endswith(('.png')):
            end_with = ".png"
        elif file_name.lower().endswith(('.jpg')):
            end_with = ".jpg"
        elif file_name.lower().endswith(('.jpeg')):
            end_with = ".jpeg"
        elif file_name.lower().endswith(('.webp')):
            end_with = ".webp"
        else:
            wrong_image = "There is something wrong with the photo you uploaded, please try another image"
            return render_template('index.html', not_exist=wrong_image)
        session['image'] = 'static/images/' + username + end_with
        new_image = open("static/images/" + username + end_with,"wb")
        new_image.write(image.read())
        new_image.close()
    #If user didn't choose any photo/upload photo set image to unknown
    else:
        session['image'] = 'static/unknown.png'
    image = session['image']
    DBManage.new_person(username,room,image)
    limit = DBManage.limit(room)
    session["limit"] = limit
    return render_template('chat.html', session = session)

#When user join to chat
@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)
    emit('newUser', {'username': session.get('username'),'image':session.get('image')}, room=room)

#Send users data (image,username)
@socketio.on('users', namespace='/chat')
def users():
    users = DBManage.room_users(session.get('room'))
    emit('usersData', {'data': users ,'len':len(users)}, room=session.get('room'))

#Send message to all users when user send message 
@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    DBManage.new_message(room,message,session.get('username'))
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)

#Send to all users when user left the chat
@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    if os.path.exists("static/images/" + username +".jpg"):
        os.remove("static/images/" + username +".jpg")
    elif os.path.exists("static/images/" + username +".jpeg"):
        os.remove("static/images/" + username +".jpeg")
    elif os.path.exists("static/images/" + username +".png"):
        os.remove("static/images/" + username +".png")
    elif os.path.exists("static/images/" + username +".webp"):
        os.remove("static/images/" + username +".webp")
    DBManage.left_user(room,username)
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)
    #Update users
    users = DBManage.room_users(room)
    users_num = len(users)
    emit('usersData', {'data': users ,'len':users_num}, room=room)
    if users_num == 0:
        DBManage.close_room(room)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0')
