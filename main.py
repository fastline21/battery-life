import psutil
from win10toast import ToastNotifier
import chime
import pyttsx3
import os
from configparser import ConfigParser

# Config settings
engine = pyttsx3.init()
voices = engine.getProperty("voices")
config = ConfigParser()

# Default value
show_notification = False
battery_life_percent = 0
warning_battery = 0
config_file = "config.ini"
engine.setProperty("rate", 150)

# Current voice
current_voice = engine.getProperty("voice")
for index, value in enumerate(voices):
    if value.id == current_voice:
        current_voice = index
        break

# Current theme
current_theme = chime.theme()

while True:
    if not os.path.exists(config_file):
        print("Creating config file")

        # Head section
        config.add_section("Notification")
        config.add_section("Sound")

        # Input value to the section
        while True:
            theme = input(f"Choose themes {chime.themes()}: ").lower()
            if not theme:
                break
            elif theme not in chime.themes():
                print("Wrong choice")
                continue
            else:
                break

        while True:
            try:
                voice = input(f"Choose voice 0 = Male, 1 = Femaile: ")
                if not voice:
                    break
                elif int(voice) > 1 or int(voice) < 0:
                    print("Wrong choice")
                    continue
            except ValueError:
                print("Wrong choice")
                continue
            else:
                break

        # Added value to section
        config.set("Notification", "theme", theme or current_theme)
        config.set("Sound", "voice", voice or str(current_voice))

        # Create config file with data
        with open(config_file, "w") as file:
            config.write(file)

        print("Success create config file")
        continue
    else:
        print("Loading config file")
        config.read(config_file)
        current_theme = config.get("Notification", "theme")
        current_voice = config.get("Sound", "voice")
        print("Success load config file")
        break

# Set current theme and voice
engine.setProperty("voice", voices[int(current_voice)].id)
chime.theme(current_theme)


def battery_notification(message, is_toast=True):
    print(message)
    engine.say(message)
    engine.runAndWait()

    if is_toast == True:
        chime.success()
        toaster = ToastNotifier()
        toaster.show_toast("Battery Life", message, duration=10)


def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)


def check_battery_percent(battery):
    global warning_battery

    if battery.percent == 100 and battery.power_plugged:
        battery_notification("Full Battery")
    elif battery.percent <= 20 and battery.percent > 10 and not battery.power_plugged:
        battery_notification("Battery Saver On")
    elif battery.percent <= 10 and battery.percent > 5 and not battery.power_plugged:
        if warning_battery >= 5:
            battery_notification(
                "Please charge your laptop or this will shutdown in 5 seconds", False)
            for count in reversed(range(6)):
                battery_notification(count, False)
                if count == 0:
                    battery_notification(
                        "Your laptop is shutting down...", False)
                    os.system("shutdown /h")
                    quit()

        warning_battery += 1
        battery_notification("Low Battery")
    elif battery.percent <= 5 and battery.percent > 1 and not battery.power_plugged:
        battery_notification("Critical Battery")


def get_battery_life():
    global show_notification, battery_life_percent
    battery = psutil.sensors_battery()

    if (battery_life_percent != battery.percent):
        battery_life_percent = battery.percent
        print(
            f"Battery Percent: {battery_life_percent}, Battery Time: {secs2hours(battery.secsleft)}")

    if battery.power_plugged:
        if show_notification == False:
            battery_notification("Charging Laptop")
            show_notification = True
    else:
        if show_notification == True:
            battery_notification("Discharging Laptop")
            show_notification = False

    check_battery_percent(battery)


# Startup notification
battery_notification("App starting...")

while True:
    get_battery_life()
