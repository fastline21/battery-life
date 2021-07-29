import psutil
from win10toast import ToastNotifier
import chime
import pyttsx3
import os

# Config settings
chime.theme("material")
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 150)

# Default value
show_notification = False
battery_life_percent = 0
warning_battery = 0


def batteryNotification(message):
    engine.say(message)
    engine.runAndWait()
    chime.success()
    print(message)

    toaster = ToastNotifier()
    toaster.show_toast("Battery Life", message, duration=10)


def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)


def checkBatteryPercent(battery):
    global warning_battery
    if battery.percent == 100 and battery.power_plugged:
        batteryNotification("Full Battery")
    elif battery.percent <= 20 and battery.percent > 10 and not battery.power_plugged:
        batteryNotification("Battery Saver On")
    elif battery.percent <= 10 and battery.percent > 5 and not battery.power_plugged:
        if warning_battery >= 5:
            os.system("shutdown /h")
            quit()

        warning_battery += 1
        batteryNotification("Low Battery")
    elif battery.percent <= 5 and battery.percent > 1 and not battery.power_plugged:
        batteryNotification("Critical Battery")


def getBatteryLife():
    global show_notification, battery_life_percent
    battery = psutil.sensors_battery()

    if (battery_life_percent != battery.percent):
        battery_life_percent = battery.percent
        print(
            f"Battery Percent: {battery_life_percent}, Battery Time: {secs2hours(battery.secsleft)}")

    if battery.power_plugged:
        if show_notification == False:
            batteryNotification("Charging Laptop")
            show_notification = True
    else:
        if show_notification == True:
            batteryNotification("Discharging Laptop")
            show_notification = False

    checkBatteryPercent(battery)


# Startup notification
batteryNotification("App starting...")

while True:
    getBatteryLife()
