import requests
from datetime import datetime
import smtplib

MY_LAT = 36.778259
MY_LONG = -119.417931
MY_EMAIL = "armstrongspycon27@gmail.com"
TO = "zedcurl1@gmail.com"
""" Use your own gmail app password for the "MY_PASSWORD" """
MY_PASSWORD = ""

""" ISSO API"""
def isso():
    res = requests.get(url="http://api.open-notify.org/iss-now.json")
    res.raise_for_status()

    dat = res.json()
    longitude = float(dat["iss_position"]["longitude"])
    latitude = float(dat["iss_position"]["latitude"])
    iss_position = (longitude, latitude)
    return iss_position



def sunrise_and_set():
    """ SUNSET API """
    parameter = {
        "lat": MY_LAT,
         "lng": MY_LONG,
        "formatted": 0
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameter)
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    return sunrise, sunset



now = datetime.now()


def check_isso_position_proximate():
    isso_ = isso()
    if (MY_LONG <= isso_[0] <= MY_LONG) and (MY_LAT - 5 <= isso_[1] <= MY_LAT):
        return True
    return False


sun_rise, sun_set = sunrise_and_set()

if sun_rise >= now.hour >= sun_set and check_isso_position_proximate():
    print("ISSO ALERT SENT")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
        connection.ehlo()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=[TO],
                            msg=f"Subject:International Space Station at your location alert\n\n"
                                f"Raise your head to the skies to see the magnificent International Space Station"
                                f" (ISSO)")






