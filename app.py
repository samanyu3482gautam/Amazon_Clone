from flask import Flask,render_template,request,flash,session,redirect,url_for
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



app=Flask(__name__)
app.secret_key="amazonclone"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.permanent_session_lifetime=timedelta(minutes=15)

db=SQLAlchemy(app)

class users(db.Model):
    _id=db.Column("id",db.Integer,primary_key=True)
    password_hash = db.Column(db.String(128))

    name=db.Column("name",db.String(100))
    username=db.Column("username",db.String(100))
    email=db.Column("email",db.String(100))
    number=db.Column("number",db.String(10))
    address=db.Column("address",db.String(100))
    pin=db.Column("pin",db.String(10))

    def __init__(self,name,email,username,number,address,pin,password):
        self.name=name
        self.email=email
        self.username=username
        self.number=number
        self.address=address
        self.pin=pin
        self.password_hash=generate_password_hash(password)

@app.route("/signUp",methods=["POST","GET"])
def signUp():
    if request.method=="POST":
        new_email=request.form["email"]
        session["email"]=new_email
        found_user=users.query.filter_by(email=new_email).first()
        if found_user:
            session["email"]=found_user.email
            flash("user already exists with this email.")
            return redirect(url_for("login"))

        else:
            #if the user do not exists
            usr=users("",new_email,"","","","","noPass")
            db.session.add(usr)
            db.session.commit()
            flash('Enter Your Details Now.')
            return redirect(url_for("details"))


    return render_template("signUp.html")



@app.route("/details",methods=["GET","POST"])
def details():
    found_user=users.query.filter_by(email=session["email"]).first()
    if found_user:
        if request.method=="POST":
            name=request.form["name"]
            number=request.form["number"]
            address=request.form["address"]
            pin=request.form["pin"]
            
            found_user.name=name
            found_user.number=number
            found_user.address=address
            found_user.pin=pin
            db.session.commit()
            # flash('Now Create Your Password!')
            return render_template("createPass.html")
        else:
            return render_template("details.html")  

    else:
        return render_template("signUp.html")

@app.route("/createPass",methods=["GET","POST"])
def createPass():
    email=session.get("email")
    if not email:
        return redirect(url_for("signUp"))
    found_user=users.query.filter_by(email=session["email"]).first()
    if(not found_user):
        return redirect(url_for("signUp"))
    if request.method=="POST":
        p1=request.form["password1"]
        p2=request.form["password2"]
        if p1==p2:
            found_user.password_hash=generate_password_hash(p1)
            db.session.commit()
            flash("Account Created Login!")
            return redirect(url_for('login'))
        else:
            return render_template("createPass.html")
    
    else:
        return render_template("signUp.html")



@app.route("/login",methods=["GET","POST"])
def login():
    
    if request.method=="POST":
        session.permanent=True
        # flash("Login Successful!")
        email=request.form["email"]
        if(not email):
            
            return render_template("login.html")
        session["email"]=email
        found_user=users.query.filter_by(email=email).first()

        if(not found_user):
            flash('User Not Found Plz SignUp!')
            return redirect(url_for('signUp'))
        
       
        if "@" in email:
            lis=email.split("@")
            session["username"]=lis[0]
            found_user.username=session["username"]
            db.session.commit()
            
                
        if len(session["username"])>15:
            session["username"]="Undefined user(long username)"
            found_user.username=""
            db.session.commit()
            flash('Enter Your Username!')
            return redirect(url_for('username'))
        
        flash('Enter Your Password!')
        return  redirect(url_for('verify'))
    else:
        # if "email" in session and "verified" in session and session["verified"]==True:
            
        #     # flash("You are already logged In.")
        #     return redirect(url_for("home"))  
        # else:
            return render_template("login.html")


    
    


@app.route("/deleteAccount",methods=["GET","POST"])
def deleteAccount():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        found_user=users.query.filter_by(email=email).first()
        if found_user:
            if check_password_hash(found_user.password,password):
                db.session.delete(found_user)
                db.session.commit()
                session.clear()
                # flash('Account Deleted','success')
                return redirect(url_for('login'))
            
            else:
                # flash('Enter Correct Password','error')
                return render_template("deleteAccount.html")
        else:
            # flash('User Not Found','error')
            return redirect(url_for('login'))
    else:
        return render_template("deleteAccount.html")

# @app.route("/deleteAccount", methods=["GET", "POST"])
# def deleteAccount():
#     if request.method == "POST":
#         email = request.form.get("email")
#         password = request.form.get("password")
        
        
#         found_user = users.query.filter_by(email=email).first()

#         if found_user:
           
#             if check_password_hash(found_user.password, password):
              
#                 db.session.delete(found_user)
#                 db.session.commit()

                
#                 session.clear()

#                 flash('Account successfully deleted.', 'success')

                
#                 return redirect(url_for('login'))
#             else:
                
#                 flash('Incorrect password. Please try again.', 'error')
#                 return render_template("deleteAccount.html")
#         else:
            
#             # flash('No user found with that email.', 'error')
#             return redirect(url_for('login'))
#     else:
       
#         return render_template("deleteAccount.html")

@app.route("/username",methods=["GET","POST"])
def username():
    if request.method=="POST" and session["username"]=="Undefined user(long username)":
        username=request.form["username"]
        found_user=users.query.filter_by(email=session["email"]).first()
        if (len(session["username"])>15):
            flash('Enter Username Within 15 Characters')
            return redirect(url_for("username"))
        else:

            session["username"]=username
            found_user.username=session["username"]
            db.session.commit()
            flash('Enter Your Password')
            return redirect(url_for('verify'))
    else:
        return render_template("chkPass.html")


        
@app.route("/verify",methods=["GET","POST"])
def verify():
    if request.method=="POST":
    
        if "email" not in session or "username" not in session:
            flash('You Have Been Logged Out!')
            return redirect(url_for("logout"))
        else:
            password=request.form["password"]
            found_user=users.query.filter_by(email=session["email"]).first()
            if found_user and check_password_hash(found_user.password_hash, password):
            
                session["verified"]=True
                db.session.commit()
                return render_template("home.html")
            else:
                # flash("Wrong Password")
                db.session.commit()
                flash('Enter Correct Password')
                return redirect(url_for('login'))
    else:
        return render_template("chkPass.html")
        
    
   

    
    

    

    
@app.route("/logout")
def logout():
    
    session.clear()
    return render_template("logout.html")


@app.context_processor
def inject_user():
    email = session.get("email")
    user = None
    if email:
        user = users.query.filter_by(email=email).first()
   
    return dict(user=user)

@app.route("/home")
def home():
    email=session.get("email")
    found_user=users.query.filter_by(email=email).first()
    if "verified" in session and session["verified"]==True and found_user:
        return render_template("home.html")
    else:
        return redirect(url_for("login"))




@app.route("/cook")
def cook():
    return render_template("cook.html")

@app.route("/electronics")
def electronics():
    return render_template("phone1.html")
@app.route("/shoes")
def shoes():
    return render_template("shoe1.html")
@app.route("/diwali")
def diwali():
    return render_template("diwali1.html")
@app.route("/watches")
def watches():
    return render_template("watch2.html")
@app.route("/fashion")
def fashion():
    return render_template("fashion1.html")
@app.route("/stationary")
def stationary():
    return render_template("stationary1.html")
@app.route("/beauty")
def beauty():
    return render_template("beauty1.html")

with app.app_context():
    db.drop_all()
    db.create_all()

if __name__=="__main__":
    
    app.run(debug=True)
    

