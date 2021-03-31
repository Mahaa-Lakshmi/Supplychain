from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            psw = request.form['psw']
            u_id = request.form['u_id']
            company = request.form['company']
            location = request.form['location']

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO DBtable(name,email,password,uniqueid,company,location) VALUES(?, ?, ?, ?,?,?)",(name,email,psw,u_id,company,location) )

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("index.html")
            con.close()


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from DBtable")

    rows = cur.fetchall();
    return render_template("result1.html", rows=rows)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
            con = sql.connect("medicine.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from medicinetb")
            rows = cur.fetchall();
            return render_template("index.html", rows=rows)
            con.close()
            uname = request.form['username']
            pwd = request.form['password']
            with sql.connect("database.db") as con:
                cur = con.cursor()
                query = "SELECT * FROM DBtable WHERE email = '" + uname + "' AND password = '" + pwd + "'"
                #cur.execute('SELECT email,password FROM DBtable WHERE email=? and password=?', (uname,pwd))
                cur.execute(query)
                checkUsername = cur.fetchone()
                if checkUsername != 0:
                    return render_template("index.html")

                else:
                    con.rollback()
                    return render_template("homepage.html")



@app.route('/verify', methods=['POST', 'GET'])
def verify():

    if request.method == 'POST':
        try:

            name = request.form['nameofmedicine']
            fname = request.form['details']
            type = request.form['typeofmedicine']
            manufacturer = request.form['manufacturer']

            with sql.connect("medicine.db") as con:
                cur = con.cursor()


                cur.execute("INSERT INTO medicinetb(med_name,type,composition,manufacturer) VALUES(?, ?, ?,?)",(name,type,fname,manufacturer) )
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            con = sql.connect("medicine.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("select * from medicinetb")
            rows = cur.fetchall();
            return render_template("index.html", rows=rows)
            con.close()



if __name__ == '__main__':
    app.run(debug=True)