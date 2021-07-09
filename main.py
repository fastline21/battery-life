import psutil
from win10toast import ToastNotifier
import chime
import time

chime.theme("material")
show_notification = False


def batteryNotification(message):
    toaster = ToastNotifier()
    toaster.show_toast("Battery Life", message, duration=10)


def checkBatteryPercent(battery):
    if battery.percent == 100:
        batteryNotification("Full Battery")
    elif battery.percent == 10:
        batteryNotification("Low Battery")
    elif battery.percent == 5:
        batteryNotification("Critical Battery")


def getBatteryLife():
    global show_notification
    battery = psutil.sensors_battery()

    if battery.power_plugged:
        if show_notification == False:
            batteryNotification("Charging Laptop")
            show_notification = True
    else:
        show_notification = False

    checkBatteryPercent(battery)


chime.success()
print("Battery Life starting...")

while True:
    getBatteryLife()
    time.sleep(10)
