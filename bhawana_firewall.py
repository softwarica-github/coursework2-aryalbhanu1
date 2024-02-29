#!/usr/bin/env python3

import os
import sys
import sqlite3
from tkinter import *

# Checking permissions
perm = int(os.getuid())
if perm != 0:
    print("You must be a root to use this program.")
    sys.exit(1)

# Initialize SQLite database
conn = sqlite3.connect('firewall.db')
c = conn.cursor()

# Create firewall settings table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS firewall_settings
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              setting_name TEXT,
              setting_value TEXT)''')
conn.commit()

# Function to retrieve a setting from the database
def get_setting(setting_name):
    c.execute("SELECT setting_value FROM firewall_settings WHERE setting_name=?", (setting_name,))
    setting = c.fetchone()
    return setting[0] if setting else None

# Function to update a setting in the database
def update_setting(setting_name, setting_value):
    c.execute("REPLACE INTO firewall_settings (setting_name, setting_value) VALUES (?, ?)", (setting_name, setting_value))
    conn.commit()

# Creating window
window = Tk()
window.geometry("600x400")
window.title("Bhawana Firewall")

# Creating labels and entry widgets
target_port = Label(window, text="Enter port to close: ")
target_port.grid(column=0, row=0)
port = Entry(window, width="15")
port.grid(column=1, row=0)
information = Label(window, text="")
information.grid(column=1, row=2)
info2 = Label(window, text="")
info2.grid(column=1, row=5)
restoree = Label(window, text="Restore firewall rules => ")
restoree.grid(column=0, row=4)
open_port = Label(window, text="Enter port to open: ")
open_port.grid(column=0, row=6)
open_enter = Entry(window, width="15")
open_enter.grid(column=1, row=6)
listen_area = Label(window, text="")
listen_area.grid(column=0, row=7)
blocker_lbl = Label(window, text="Enter IP address to block: ")
blocker_lbl.grid(column=0, row=8)
blocker_ent = Entry(window, width="15")
blocker_ent.grid(column=1, row=8)
blocker_inf = Label(window, text="")
blocker_inf.grid(column=0, row=9)
# Connection window area
conn_lbl = Label(window, text="Interface: ")
conn_lbl.grid(column=0, row=10)
iface_ent = Entry(window, width="15")
iface_ent.grid(column=1, row=10)

# Defining button commands
def closer():
    try:
        killer0 = "iptables -A INPUT -p tcp --destination-port {} -j DROP".format(port.get())
        killer1 = "iptables -A OUTPUT -p tcp --destination-port {} -j DROP".format(port.get())
        os.system(killer0)
        os.system(killer1)
        information.configure(text="Port {} successfully closed.".format(port.get()))
        # Update setting in the database
        update_setting('closed_port', port.get())
    except:
        information.configure(text="An error occurred while closing the port.")

def restore():
    try:
        os.system("sudo iptables -F")
        info2.configure(text="Firewall rules restored.")
        # Update setting in the database
        update_setting('closed_port', '')
    except:
        info2.configure(text="An error occurred while restoring the rules.")

def openn():
    try:
        listen_area.configure(text="Port {}/tcp opened and listening connections.".format(open_enter.get()))
        server = "nc -lvp {} &".format(open_enter.get())
        os.system(server)
        # Update setting in the database
        update_setting('opened_port', open_enter.get())
    except:
        listen_area.configure(text="An error occurred while listening to the server.")

def blocker():
    try:
        block = "iptables -A INPUT -s {} -j DROP".format(blocker_ent.get())
        os.system(block)
        blocker_inf.configure(text="IP Address: {} successfully blocked.".format(blocker_ent.get()))
        # Update setting in the database
        update_setting('blocked_ip', blocker_ent.get())
    except:
        blocker_inf.configure(text="An error occurred while blocking.")

def catcher():
    try:
        interface = str(iface_ent.get())
        monitor = "./netm0n.sh {} &".format(interface)
        os.system(monitor)
    except Exception as e:
        print("An error occurred:", e)
        sys.exit(1)

# Creating buttons for window
buttons = Button(window, text="Close", command=closer)
buttons.grid(column=2, row=0)
buttons2 = Button(window, text="Restore", command=restore)
buttons2.grid(column=1, row=4)
buttons3 = Button(window, text="Open", command=openn)
buttons3.grid(column=2, row=6)
buttons4 = Button(window, text="Block", command=blocker)
buttons4.grid(column=2, row=8)
butt = Button(window, text="Start", command=catcher)
butt.grid(column=1, row=12)

# Load settings from the database
closed_port = get_setting('closed_port')
if closed_port:
    port.insert(0, closed_port)

opened_port = get_setting('opened_port')
if opened_port:
    open_enter.insert(0, opened_port)

blocked_ip = get_setting('blocked_ip')
if blocked_ip:
    blocker_ent.insert(0, blocked_ip)

# Window execution
window.mainloop()

# Close database connection
conn.close()



