import psutil
from win10toast import ToastNotifier
import chime

chime.theme("material")
show_notification = False
battery_life_percent = 0


def batteryNotification(message):
    toaster = ToastNotifier()
    toaster.show_toast("Battery Life", message, duration=10)


def checkBatteryPercent(battery):
    if battery.percent == 100 and battery.power_plugged:
        batteryNotification("Full Battery")
        print("Full Battery")
    elif battery.percent <= 20 and battery.percent > 10 and not battery.power_plugged:
        batteryNotification("Battery Saver On")
        print("Battery Saver On")
    elif battery.percent <= 10 and battery.percent > 5 and not battery.power_plugged:
        batteryNotification("Low Battery")
        print("Low Battery")
    elif battery.percent <= 5 and battery.percent > 1 and not battery.power_plugged:
        batteryNotification("Critical Battery")
        print("Critical Battery")


def getBatteryLife():
    global show_notification, battery_life_percent
    battery = psutil.sensors_battery()

    if (battery_life_percent != battery.percent):
        battery_life_percent = battery.percent
        print("Battery Percent:", battery_life_percent)

    if battery.power_plugged:
        if show_notification == False:
            batteryNotification("Charging Laptop")
            print("Charging Laptop")
            show_notification = True
    else:
        show_notification = False

    checkBatteryPercent(battery)


chime.success()
print("Battery Life App starting...")
batteryNotification("App starting...")

while True:
    getBatteryLife()
