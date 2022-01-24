from flask import Flask,redirect,render_template,request,session,jsonify
from flask_session import Session
import bcrypt
import database
import random
import string
import encryption

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def create_room():
        id = ''.join([random.choice(string.ascii_letters + string.digits  ) for n in range(8)])
        while database.rooms.find_one({"room_id":id}) != None:
            id = ''.join([random.choice(string.ascii_letters + string.digits  ) for n in range(8)])

        chat = []
        emails = []
        emails.append(session["email"])
        database.rooms.insert_one({ 
                                    "max" : 8,
                                    "emails":emails,
                                    "room_id":id,
                                    "chats": chat  
                                })
        return id


@app.route("/")
def main():
    return redirect("/index")


@app.route("/forgot_pass")
def forgot_pass():
    return render_template('forgot_pass.html')


@app.route("/forgot_pass_post",methods=['POST'])
def forgot_pass_post():
    email = request.form["email"]
    name = request.form["name"]
    password = request.form["password"]

    if not email or not name or not password:
        return jsonify("0")

    user = database.users.find_one({"email": email})
    if user["name"] == name:
        database.users.replace_one({"email" : email},{"key":user["key"],"email":email,"name":name,"password": bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())})
        return jsonify("1")
    
    return jsonify("2")
    

@app.route("/check_password",methods = ['POST'])
def check_password():
    email = request.form["email"]
    user = database.users.find_one({"email": email})

    if user == None:
        return jsonify("1")
    else:
        password = request.form["password"]
        hpassword = user["password"]

        if bcrypt.checkpw(password.encode('utf-8'), hpassword):
            session["name"] = user["name"]
            session["email"] = user["email"]   
            return jsonify("2")
        else:
            return jsonify("3")


@app.route("/index",methods = ['GET'])
def index():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html')
    
@app.route("/create_room",methods = ['POST'])
def create():
        session["key"] = random.randint(1,1000)
        room_id = create_room()
        session["room_id"] = room_id
        return jsonify()


@app.route("/enter_room",methods = ['POST'])
def enter_(): 
        
        session["key"] = random.randint(1,1000)
        entered_id = request.form["room_id"]

        room = database.rooms.find_one({"room_id":entered_id})
        if(room != None):
            session["room_id"] = room["room_id"]
            if room["max"] > 0:
                emails = room["emails"] 
                if session["email"] not in emails:
                    emails.append(session["email"])
                    max = room["max"] - 1
                    chats = room["chats"]  
                    database.rooms.replace_one({"room_id" : session["room_id"]},{"room_id" : session["room_id"],"chats":chats,"max":max,"emails":emails})
                    
                return jsonify("0")
            return jsonify("1")
        return jsonify("2")



@app.route("/site",methods = ['GET'])
def site():
    if session.get("room_id"):
        return render_template('site.html',room_id = session["room_id"],key = session["key"])
    return redirect('/index')    


@app.route("/site_get",methods=['POST'])
def site_get():
    key = int(request.form["key"])
    Chats = database.rooms.find_one({"room_id":session["room_id"]})
    chats = Chats["chats"]

    if chats and key != 0:
        show_message = []
        for chat in chats:
            if len(chat) >= 4 and chat[-4] == ':' :
                msg = chat.split(":")
                dec_msg = encryption.decrypt(key,msg[1])
                overall = msg[0] + ":" + dec_msg + ":" + msg[2]
                show_message.append(overall)
                continue
            show_message.append(chat) 
        return jsonify(show_message)

    return jsonify(chats)


    
@app.route("/site_post",methods=['POST'])
def site_post():

    form_message = request.form['message']
    if(form_message != ""):
        encrypt = request.form["encrypt"]
        message = session["name"] + ":" + form_message + ":"
        
        if encrypt == "yes":
            message += encrypt
        
        database.rooms.update_one({"room_id" : session["room_id"]},{ "$push": { "chats": message } })
        data =  database.rooms.find_one({"room_id":session["room_id"]})

        return jsonify(data["chats"])
    
    return jsonify({'error':"yes"})
   

@app.route("/sign_up",methods = ['GET','POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('signup.html')
    
    email = request.form["email"]
    name = request.form["name"]
    password = request.form["password"]

    if not email or not name or not password:
        return jsonify("0")

    user = database.users.find_one({"email": email})
    if user == None:
        database.users.insert_one({
            'name': name,
            'email' : email,
            'password': bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        })
        return jsonify("1")
    else:
        return jsonify("2")


@app.route('/enc_message',methods = ['POST'])
def enc_message():
    message = request.form["message"]
    encrypt = request.form["encrypt"]

    if message != "" and encrypt == "yes":
        message = encryption.encrypt(session["key"],message)
    
    if message != "" and encrypt == "no":
        message = encryption.decrypt(session["key"],message)

    return jsonify(message)


@app.route("/remove_user",methods=['POST'])
def remove_user():

    print("enter")
    room_id = session["room_id"]
    data = database.rooms.find_one({"room_id":room_id})

    if data["max"] == 0:
        print("delete")
        database.rooms.delete_one({"room_id":room_id})
    else:
        print("remove")
        emails = data["emails"]
        emails.remove(session["email"])
        database.rooms.replace_one({"room_id" : room_id},{"room_id" : room_id,"chats":data["chats"],"max":data[max]-1,"emails":emails})

    



if __name__ == "__main__":
    app.run(debug=True)    
    