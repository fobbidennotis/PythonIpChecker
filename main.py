from customtkinter import *
from portscanner import *
from tkintermapview import TkinterMapView

set_appearance_mode("dark")  # Modes: system (default), light, dark
set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = CTk()
app.geometry("465x355")
app.title('Ip Checker')
app.resizable(False, False)

welcome_message = """[+] This is read-only!
[+] Ignore the start marker.
[+] Map accuracy: +-100m!"""

def display_slider_ports(amount):
    label1.configure(text=f'Scan {round(amount)} ports.')
    return amount

def ip_info(ip='127.0.0.1'):
    (ip, city, country, timezone), geoinfo = get_ip_info(ip)
    return f"""
[INFO]
[IP] : {ip}
[Country] : {country}
[City] : {city}
[TZ] : {timezone} """, geoinfo

def display_data():
    target_ip = entry0.get()
    ip_data, geoinfo = ip_info(target_ip)
    txt0.insert(END, ip_data)
    set_map_postition(geoinfo[0], geoinfo[1])
    app.update()
    app.after(1, showports)

def showports():
    target_ip = entry0.get()
    txt0.insert(END, '\n[OPEN PORTS]\n')
    max_port = round(prgbar.get())
    extracted_ports = scan_ports(target_ip, port_range=f'1-{max_port}')

    if len(extracted_ports):
        txt0.insert(END, ''.join([
            f'[+] {port} {service}\n'
            for port, service in extracted_ports
        ]))
    else:
        txt0.insert(END, '[ - ] No ports found.\n')

def set_map_postition(lat, lon):
    global marker
    marker.delete()
    marker = map0.set_position(lat, lon, marker=True)
    map0.set_zoom(10)

frame0 = CTkFrame(master= app,border_width=2, width=225, height=340)
frame0.grid(column = 0, row= 0, padx = 5, pady = 5)

frame1 = CTkFrame(master=app, border_width=2, width=225, height=340)
frame1.grid(column = 1, row =0, padx= 0, pady = 5)

entry0 = CTkEntry(master=frame0, height=20, width=150)
entry0.place(x = 40, y = 45)

label0 = CTkLabel(master=frame0, font=('Helvetica', 17), text='Put the IP Adress here : ')
label0.place(x = 30, y = 10)

prgbar = CTkSlider(master=frame0, from_=2, to=1024, width=175, height=15, command=display_slider_ports, number_of_steps=512)
prgbar.place(x = 25, y = 80)

label1 = CTkLabel(master=frame0, font=('Helvetica', 16), text = 'Scan 2 ports')
label1.place(x = 60, y = 100)

txt0 = CTkTextbox(master=frame0, font=('Helvetica', 15), width=200, height= 175, state= NORMAL)
txt0.place(x = 12, y = 155)
txt0.insert(END, welcome_message)

btn0 = CTkButton(master=frame0, font=('Helvetica', 16), width= 150, height=15, text='Check', command=display_data)
btn0.place(x = 35, y = 125)

map0 = TkinterMapView(master = frame1, width = 205, height = 320)
map0.place(x = 10, y = 10)

marker = map0.set_position(0, 0, marker= True)
prgbar.set(2)

app.mainloop()