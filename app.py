from flask import Flask, render_template, request,redirect
import requests

import mysql.connector

try:
    mydb = mysql.connector.connect(
        host="ballast.proxy.rlwy.net",
        user="root",
        password="TDjjolWKyuFyinnbaEjlvVAkvJdRjQgs",
        database="railway",
        port=18353
    )
    db_cursor=mydb.cursor()
except Exception as e:
    print(e)


app = Flask(__name__)
api_key = "2e65ce041ce915f57b7a7a26da610fec"

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None  # initialize
    error=None
    if request.method == 'POST':
        city = request.form.get('city')  # lowercase same as HTML nam
        if not city or city.strip() == "":
            error = "Please enter a city name!"
        else:
            db_cursor.execute("INSERT INTO HistoryData (city) VALUES (%s)", (city,))
            mydb.commit()
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url).json()
        
            if response.get("main"):
                weather_data = {
                    "city": city,
                    "temp": response["main"]["temp"],
                    "description": response["weather"][0]["description"]
                }
            else:
                weather_data = {"error": "City not found!"}
    db_cursor.execute("SELECT id, city FROM HistoryData ORDER BY id DESC")
    history = db_cursor.fetchall()
    print(history)
    return render_template('home.html',weather=weather_data,history=history,error=error)


@app.route('/delete/<int:id>')
def delete(id):
    db_cursor.execute("DELETE FROM HistoryData WHERE id = %s", (id,))
    mydb.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run()