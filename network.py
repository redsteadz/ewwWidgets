import subprocess
import time
import threading


def loadCommand():
    output = subprocess.check_output(['nmcli', '-f', 'SSID', 'device', 'wifi','list'], universal_newlines=True)

    return output.split("\n")

output = loadCommand()
names = []
for i in output:
    # print(i.strip())
    names.append(i.strip())


# template = f"""
#           (button :class "navButton netButton"
#                   :onclick "eww -c . update selectedItem='{names[i]}'" :timeout "500ms" :valign "center" :halign "center" :width 200 :height 30 
#             "{names[i]}")
# """

namesInformat = "["

stack = ""

for i in range(1,len(names)):
    if names[i] != "--" and names[i] != "":
        # print(names[i])
        template = f"""
                  (button :class "navButton netButton"
                          :onclick "eww -c . update selectedItem='{names[i]}'" :timeout "500ms" :valign "center" :halign "center" :width 200 :height 30 
                    "{names[i]}")
        """
        # template += "\n"
        stack += template
        # print(template)
# print(stack)
stack = fr"""(box :orientation 'vertical' {stack or ''})"""
shit = subprocess.run(["eww", "-c", ".", "update", f"networks={stack}"])
print(shit)


