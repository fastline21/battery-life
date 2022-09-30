import os
import platform


class PushNotification:
    def __init__(self, title, message) -> None:
        self.title = title
        self.message = message
        pass

    def push(self):
        user_os = platform.system()

        if user_os == 'Darwin':
            command = f'''
            osascript -e 'display notification "{self.message}" with title "{self.title}"'
            '''

        if user_os == "Linux":
            command = f'''
		    notify-send "{self.title}" "{self.message}"
		    '''

        else:
            return

        os.system(command)
