from flask import Flask, render_template, json, request
import sqlite3

con=sqlite3.connect("names.db", check_same_thread=False)

cur=con.cursor()

def initDB():
    try:
        cur.execute("CREATE TABLE userNames (name text, age int)")
    except:
        print("Table already exists!")

    con.commit()
initDB()

app = Flask(__name__)

myList = ['Chen', 'Noya', 'Ron', 'Bruno']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html", myList=myList)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/addToDb", methods=['GET', 'POST'])
def addToDb():
    if request.method=="POST":
        uName = request.form.get('userName')
        uAge = request.form.get('userAge')
        cur.execute(f"INSERT INTO userNames VALUES('{uName}', {int(uAge)})")
    return render_template("addToDb.html")

@app.route("/removeFromDB", methods=['GET', 'POST'])
def remFromDB():
    if request.method=="POST":
        uName = request.form.get('userName')
        uAge = request.form.get('userAge')
        cur.execute(f"DELETE FROM userNames WHERE name=? and age=? ('{uName}',{uAge})")
    return render_template("removeFromDB.html")

#Sends database to browser
@app.route("/showDB")
def showDB():
    SQL = "SELECT * FROM userNames"
    cur.execute(SQL)
    dbList = []
    for i in cur:
        dbList.append({"Name": i[0], "Age": i[1]})
    return (json.dumps(dbList))
if __name__=='__main__':
    app.run(debug=True)