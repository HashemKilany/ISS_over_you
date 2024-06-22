import requests as rq
from datetime import datetime as dt
import smtplib
import time

MY_LAT = 30.034808
MY_LNG = 31.484757
MY_EMAIL = "hashemgiza717@gmail.com"
PS = "lzolqlpatcjisgzh"


def is_iss_overhead():
    iss = rq.get(url="http://api.open-notify.org/iss-now.json")
    iss.raise_for_status()
    iss_data = iss.json()
    iss_long = float(iss_data["iss_position"]["longitude"])
    iss_lat = float(iss_data["iss_position"]["latitude"])

    if MY_LNG - 5 <= iss_long <= MY_LNG + 5 and MY_LAT - 5 < iss_lat <= MY_LAT + 5:
        return True


def is_night():
    parameters = {"lat": MY_LAT,
                  "lng": MY_LNG,
                  "formatted": 0,
                  "tzid": "Africa/Cairo"}
    response = rq.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    print(sunset,sunrise)
    now = dt.now().hour
    if sunset <= now or now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_night() and is_iss_overhead():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PS)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                                msg="Subject:ISS IS OVER YOU!\n\nLook at the sky now!")
            print("Done!")
