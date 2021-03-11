import sqlite3
from flask import Flask, request, jsonify
from flask_cors import  CORS


def dic_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def sql_lite_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS Register_Table (id INTEGER PRIMARY KEY AUTOINCREMENT, fname TEXT, passw TEXT, email TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS Subscribe_Table (id INTEGER PRIMARY KEY AUTOINCREMENT, emailad TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS Product_Table (id INTEGER PRIMARY KEY AUTOINCREMENT, car_name TEXT, price INT)')
    print("Table Created Successfully")
    # conn.close()


sql_lite_db()
app = Flask(__name__)
CORS(app)

@app.route('/')
def landing():
    return("<p> To view records add /show-accounts/ to url </p><p> Heroku link: </p>" )

@app.route('/add-new/', methods=['POST'])
def add_new():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            fname = post_data['fname']
            passw = post_data['passw']
            email = post_data['email']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Register_Table (fname, passw, email) VALUES (?, ?, ?)", (fname, passw, email))
                con.commit()
                msg = fname + "Account Successfully Created"
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            con.close()
            return jsonify(msg)

@app.route('/show-accounts/', methods=["GET"])
def show_accounts():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dic_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Register_Table")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching accounts from the database." + str(e))
    finally:
        con.close()
        return jsonify(records)



@app.route('/add-new2/', methods=['POST'])
def add_new2():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            emailad = post_data['emailad']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Subscribe_Table (emailad) VALUES (?)", (emailad,))
                con.commit()
                msg = emailad + "Successfully Subscribed"
        except Exception as e:
            con.rollback()
            msg = "Error occurred: " + str(e)
        finally:
            con.close()
            return jsonify(msg)

@app.route('/show-subs/', methods=["GET"])
def show_subs():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dic_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Subscribe_Table")
            records = cur.fetchall()
    except Exception as x:
        con.rollback()
        print("There was an error." + str(x))
    finally:
        con.close()
        return jsonify(records)


@app.route('/add-car/', methods=['POST'])
def add_car():
    msg = None
    if request.method == "POST":
        try:
            post_data = request.get_json()
            car_name = post_data['car_name']
            price = post_data['price']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Product_Table (car_name, price) VALUES (?,?)", (car_name, price))
                con.commit()
                msg = car_name + "Added To Cart"
        except Exception as e:
            con.rollback()
            msg = "Error occurred: " + str(e)
        finally:
            con.close()
            return jsonify(msg)

@app.route('/show-car/', methods=["GET"])
def show_car():
    records = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dic_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM Product_Table")
            records = cur.fetchall()
    except Exception as x:
        con.rollback()
        print("There was an error." + str(x))
    finally:
        con.close()
        return jsonify(records)



@app.route('/delete-account/<int:customer_id>/', methods=["DELETE"])
def delete_account(customer_id):

    msg = None
    try:
        with sqlite3.connect('database.db') as con:

            cur = con.cursor()
            cur.execute("DELETE FROM Product_Table WHERE  id = " + str(customer_id))

            con.commit()
            msg = "A account was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
        return jsonify(msg)

if __name__ == '__main__':
    app.run(debug=True)