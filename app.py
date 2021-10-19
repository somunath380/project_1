from os import name
from flask import Flask, render_template, url_for, request
import pickle
import sqlite3

app = Flask(__name__)


knn = pickle.load(open('knn.pkl', 'rb'))

def log_data_sqlite(req, res):
    conn = sqlite3.connect('cars.db')
    curr = conn.cursor()
    _sql = """insert into log (ip, browser_string, car_name, km_driven, max_power, seats, mileage_num, engine_num, torque_NM, torque_rpm, no_year, fuel, seller_type, transmission, owner, estimated_price) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
    curr.execute(_sql, (req.remote_addr, req.user_agent.browser, req.form['name'], req.form['km_driven'], req.form['max_power'], req.form['seats'], req.form['mileage_num'], req.form['engine_num'], req.form['torque_NM'], req.form['torque_rpm'], req.form['no_year'], req.form['fuel'], req.form['seller'],req.form['transmission'],req.form['owner'], str(res)))
    conn.commit()
    curr.close()
    conn.close()

@app.route('/')
@app.route('/entry')
def entry_page():
    return render_template('entry.html', the_title='welcome')


@app.route('/admin')
def view_data():
   conn = sqlite3.connect('cars.db')
   curr = conn.cursor()
   _sql = """select * from log"""
   curr.execute(_sql)
   res = curr.fetchall()
   return render_template('database.html', res=res) 


@app.route('/search', methods=['POST'])
def get_data():
    name = str(request.form['name'])
    km_driven = int(request.form['km_driven'])
    max_power = float(request.form['max_power'])
    seats = int(request.form['seats'])
    mileage_num = float(request.form['mileage_num'])
    engine_num = int(request.form['engine_num'])
    torque_NM = float(request.form['torque_NM'])
    torque_rpm = float(request.form['torque_rpm'])
    no_year = int(request.form['no_year'])
    
    # for fuel
    if request.form['fuel']=='petrol':
        fuel_Petrol=1
        fuel_Diesel=0
        fuel_LPG=0
    elif request.form['fuel']=='diesel':
        fuel_Petrol=0
        fuel_Diesel=1
        fuel_LPG=0
    else:
        fuel_Petrol=0
        fuel_Diesel=0
        fuel_LPG=1
    
    # for seller_type
    if request.form['seller']=='individual':
        seller_type_Individual=1
        seller_type_Trustmark_Dealer=0
    else:
        seller_type_Individual=0
        seller_type_Trustmark_Dealer=1

    # for transmission_type
    if request.form['transmission']=='automatic':
        transmission_Manual=0
    else:
        transmission_Manual=1

    # for owner
    if request.form['owner']=='1st':
        owner_Fourth=0
        owner_Second=0
        owner_Test_Drive_Car=0
        owner_Third=0
    elif request.form['owner']=='2nd':
        owner_Fourth=0
        owner_Second=1
        owner_Test_Drive_Car=0
        owner_Third=0
    elif request.form['owner']=='3rd':
        owner_Fourth=0
        owner_Second=0
        owner_Test_Drive_Car=0
        owner_Third=1
    elif request.form['owner']=='4th':
        owner_Fourth=1
        owner_Second=0
        owner_Test_Drive_Car=0
        owner_Third=0
    else:
        owner_Fourth=0
        owner_Second=0
        owner_Test_Drive_Car=1
        owner_Third=0

    the_form_data=request.form
    title="Here are your Results"

    values = [[km_driven, max_power, seats, mileage_num, engine_num, torque_NM, torque_rpm, no_year, fuel_Diesel, fuel_LPG, fuel_Petrol, seller_type_Individual, seller_type_Trustmark_Dealer, transmission_Manual, owner_Fourth, owner_Second, owner_Test_Drive_Car, owner_Third]]
    the_prediction = knn.predict(values)
    log_data_sqlite(request, the_prediction)
    return render_template('results.html',the_title=title,the_form_data=the_form_data,the_prediction=the_prediction)
    

    # form_data = request.form
    # return render_template('results.html', form_data=form_data)


if __name__ == "__main__":
    app.run(debug=True)
