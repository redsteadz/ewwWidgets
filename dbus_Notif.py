import gi.repository.GLib
import time
import threading
import dbus
from dbus.mainloop.glib import DBusGMainLoop

class Notification:
    def __init__(self, summary, body, icon):
        self.summary = summary
        self.body = body
        self.icon = icon

notifications = []

def remove_object(notif):
    time.sleep(10)
    notifications.remove(notif)
    print_state()

def add_object(notif):
    notifications.insert(0, notif)
    print_state()
    timer_thread = threading.Thread(target=remove_object, args=(notif,))
    timer_thread.start()

def print_state():
    string = ""
    for item in notifications:
        string = string + f"""
      (button :class 'notif' :width 300
       (box :orientation 'horizontal' :space-evenly false
          (image :image-width 80 :image-height 80 :path '{item.icon or ''}')
          (box :orientation 'vertical'
            (label :width "100%" :limit-width 20 :wrap true :class 'title' :text '{item.summary or ''}')
            (label :width "100%" :limit-width 20 :wrap true :class 'body' :text '{item.body or ''}')
      )))
                  """
    string = string.replace('\n', ' ')
    print(fr"""(box :orientation 'vertical' {string or ''})""", flush=True)


def notif(bus, message):
    if message.get_member() == 'Notify':
        # Extract relevant information from the message
        args = message.get_args_list()
        title = args[3]
        body = args[4]
        img = args[2][7:]

        add_object(Notification(title, body, img))
        # print(f"Title: {title}")
        # print(f"Body: {body}")
        print(f"Img: {img[7:]}")
        




DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
bus.add_message_filter(notif)

mainloop = gi.repository.GLib.MainLoop()
mainloop.run()
