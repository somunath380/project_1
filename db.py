import sqlite3

conn = sqlite3.connect('cars.db')

#_sql = """create table if not exists log (id integer primary key autoincrement, ts timestamp default current_timestamp, ip text  not null, browser_string text not null, car_name text default '', km_driven text deafult '', max_power text default '', seats text default '', mileage_num text default '', engine_num text default '', torque_NM text default '', torque_rpm text default '', no_year text default '', fuel text default '', seller_type text default '', transmission text default '', owner text default '', estimated_price text default '');"""

curr = conn.cursor()

# _sql = """insert into log (ip, browser_string, car_name, km_driven, max_power, seats, mileage_num, engine_num, torque_NM, torque_rpm, no_year, fuel, seller_type, transmission, owner, estimated_price) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

# curr.execute(_sql, ('localhost', 'chrome', 'maruti suzuki', '0','0','0','0','0','0','0','0','0','0','0','0','0'))





_sql="""delete from log;"""

curr.execute(_sql)
conn.commit()

# res = curr.fetchall()

# print(res)

curr.close()
conn.close()
