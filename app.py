from flask import Flask,render_template,request,flash,session,redirect,url_for
from datetime import timedelta

app=Flask(__name__)
app.secret_key="amazonclone"
app.permanent_session_lifetime=timedelta(minutes=15)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        session.permanent=True
        # flash("Login Successful!")
        email=request.form["email"]
        session["email"]=email
        
        if "@" in email:
            lis=email.split("@")
            session["username"]=lis[0]
        if len(session["username"])>15:
            session["username"]="Undefined user"
            return render_template("username.html")
        
            


        return  render_template("chkPass.html")
    else:
        if "email" in session and "verified" in session and session["verified"]==True:
            
            # flash("You are already logged In.")
            return redirect(url_for("home"))  
        else:
            return render_template("login.html")
@app.route("/username",methods=["GET","POST"])
def username():
    if request.method=="POST" and session["username"]=="Undefined user":
        username=request.form["username"]
        if (len(session["username"])>15):
            return redirect(url_for("username"))
        else:

            session["username"]=username
            return render_template("chkPass.html")
    else:
        return render_template("chkPass.html")


        
@app.route("/verify",methods=["GET","POST"])
def verify():
    
    if "email" not in session or "username" not in session:
        return redirect(url_for("logout"))
    else:
        password=request.form["password"]
        if password=="amazonclone":
            session["verified"]=True
            return render_template("home.html")
        else:
            flash("Wrong Password")
            return render_template("login.html")
    
    
   

    
    

    

    
@app.route("/logout")
def logout():
    
    session.pop("verified",None)
    session.pop("username",None)
    session.pop("email",None)
    return render_template("logout.html")

@app.route("/signUp")
def signUp():
    return render_template("signUp.html")

@app.route("/home")
def home():
    if "verified" in session and session["verified"]==True:
        return render_template("home.html")
    else:
        return redirect(url_for("login"))

@app.route("/details")
def details():
    return render_template("details.html")



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

if __name__=="__main__":
    app.run(debug=True)
    
