import subprocess
import json
import time
import threading

# print(len(json_output))

def fixlen(a_string):
    if len(a_string) > 15:
        return a_string[:15] + '...'
    else:
        return a_string

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
    # notifications.insert(0, notif)
    if len(notifications) < 5:
        notifications.insert(0,notif)
    print_state()
    timer_thread = threading.Thread(target=remove_object, args=(notif,))
    timer_thread.start()

def print_state():
    
    string = ""
    for item in notifications:
        notifSum = fixlen(item.summary["data"])
        notifBody = fixlen(item.body["data"])
        string = string + f"""
                  (button :class 'notif'
                   (box :orientation 'horizontal' :space-evenly false
                      (image :image-width 80 :image-height 80 :path '{item.icon or ''}')
                      (box :orientation 'vertical' :width 30
                        (label :width 100 :limit-width 30 :wrap true :text '{notifSum or ''}')
                        (label :width 100 :wrap true :limit-width 30 :text '{notifBody or ''}')
                  )))
                  """
        # print(notifSum or '', notifBody or '', item.icon or '')
    string = string.replace('\n', ' ')
    print(fr"""(box :orientation 'vertical' {string or ''})""", flush=True)

def loadCommand():
    output = subprocess.check_output(['makoctl', 'history'], universal_newlines=True)
    json_output = json.loads(output)

    return json_output

prev_summary = ""
while(1):
    json_output = loadCommand()
    # if len(json_output['data'][0]) > 0:
    summary = json_output['data'][0][0]["summary"]
    body = json_output['data'][0][0]["body"]
    if prev_summary != summary:
        # print(summary, body)
        add_object(Notification(summary, body, ''))
        prev_summary = summary

    # print(json_output['data'])
    # for i in range(0, 5):
        # print(json_output['data'][0][i]["summary"])
    time.sleep(2)
    
