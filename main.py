import gi.repository.GLib
import dbus
from dbus.mainloop.glib import DBusGMainLoop

def extract_binary_data(dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dbus.ByteArray):
            return bytes(value)
    return None

def notifications(bus, message):
    if message.get_member() == 'Notify':
        # Extract relevant information from the message
        args = message.get_args_list()
        # print(args)
        title = args[3]
        body = args[4]
        # image_data = args[2] if len(args) > 6 else None
        image_data_dict = args[6] if len(args) > 6 else None

        # Do something with the extracted data
        # args[0] Program 
        # args[1] NotifCount
        # print(f"Program: {args[0]}")
        # print(f"Title: {title}")
        # print(f"Body: {body}")
        # print(f"Img: {type(args[6])}")
        # print(f"Img: {args[6:50]}")
        print(f"Title: {title}")
        print(f"Body: {body}")
        
        if image_data_dict:
            print(f"Image Data Type: {type(image_data_dict)}")

            # Extract binary data from the dictionary
            binary_data = extract_binary_data(image_data_dict)

            if binary_data:
                # Save binary data to a file
                image_file_path = '/path/to/saved_image.png'
                with open(image_file_path, 'wb') as image_file:
                    image_file.write(binary_data)

                print(f"Image saved to: {image_file_path}")

                # Open the image with feh
                import subprocess
                subprocess.run(['feh', image_file_path])
            else:
                print("No binary data found in the dictionary")
        else:
            print("No image data in the notification")


DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
bus.add_message_filter(notifications)

mainloop = gi.repository.GLib.MainLoop()
mainloop.run()
