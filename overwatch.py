import tkinter as tk
import threading
import threading
import os
import requests

PLATFORMS_LIST = ["pc", "psn", "xbl", "nintendo-switch"]


class Application(tk.Frame):
  def __init__(self, master=None):
    tk.Frame.__init__(self)
    self.master = master
    self.pack(padx=40, pady=5)
    self.create_widgets()
    self.timer_enabled = False

  def create_widgets(self):
    #Title
    self.platform_label = tk.Label(self.master,text="OW SR to TXT", font=("Helvetica",18, "bold"), fg="#ecf0f1", bg="#34495e")
    self.platform_label.pack(pady=(0,10))
    #Platform data entry
    self.platform_label = tk.Label(self.master,text="Platform", font=("Helvetica",14, "bold"), fg="#ecf0f1", bg="#34495e")
    self.platform_label.pack()
    self.platform_listbox = tk.Listbox(self.master,font=("Helvetica",12), selectmode=tk.SINGLE, height=len(PLATFORMS_LIST), activestyle=tk.DOTBOX,relief=tk.FLAT)
    self.platform_listbox.pack()
    for item in PLATFORMS_LIST:
      self.platform_listbox.insert(tk.END, item)

    #Battletag data entry
    self.battletag_label = tk.Label(self.master, text="Battletag", font=("Helvetica",14, "bold"), fg="#ecf0f1", bg="#34495e")
    self.battletag_label.pack(pady=(10,0))
    self.battletag_entry = tk.Entry(self.master, borderwidth=5, relief=tk.FLAT,font=("Helvetica",12))
    self.battletag_entry.pack(padx=10, pady=5)

    #Time selection slider
    self.time_slider_label = tk.Label(self.master, text="Checking time interval (in seconds)", font=("Helvetica",14, "bold"), fg="#ecf0f1", bg="#34495e")
    self.time_slider_label.pack(pady=(10,0))
    self.time_slider = tk.Scale(self.master, from_=20, to=120, orient=tk.HORIZONTAL,font=("Helvetica",12), bg="#34495e",fg="#ecf0f1", relief=tk.FLAT, length=200)
    self.time_slider.pack()

    #Searching label
    self.searching_label = tk.Label(self.master, text="Checking SR is disabled",font=("Helvetica",12, "bold"),fg="#e74c3c", bg="#34495e")
    self.searching_label.pack(pady=10)

    #Button 
    self.search_button = tk.Button(text="Enable Search", command=self.button_pressed,relief=tk.FLAT)
    self.search_button.pack()

    #Error label
    self.error_label = tk.Label(self.master, text="", font=("Helvetica",12,"bold"), fg="#e74c3c",bg="#34495e")
    self.error_label.pack()


  def button_pressed(self):
    if self.battletag_entry.get() == "":
      self.error_label["text"] = "Missing battletag"
      return
    self.timer_enabled = not self.timer_enabled
    if self.timer_enabled == True:
      self.search_button["text"] = "Disable Search"
      timer_value = self.time_slider.get()
      self.searching_label["text"] = f"Checking SR every {timer_value} seconds"
      self.searching_label["fg"] = "green"

    else:
      self.searching_label["text"] = "Checking SR is disabled"
      self.search_button["text"] = "Enable Search"
      self.searching_label["fg"] = "red"
    self.error_label["text"] = ""
    self.run_check()

  def search(self):
    battletag = self.battletag_entry.get()
    platform = self.platform_listbox.get(tk.ACTIVE)
    if battletag == "":
      print("No battletag found")
      return
    battletag = battletag.replace('#', '-')
    request_url = f"https://ovrstat.com/stats/{platform}/{battletag}"
    r = requests.get(request_url)
    if r.status_code != 200:
      self.error_label["text"] = r.json()["message"]
      self.search_button["text"] = "Enable Search"
      self.searching_label["text"] = "Checking SR is disabled"
      self.searching_label["fg"] = "#e74c3c"
      self.timer_enabled = False
      return
    result = r.json()
    ratings = result["ratings"]
    for rating in ratings:
      role = rating["role"]
      level = rating["level"]
      filename = f"files/{role}.txt"
      os.makedirs(os.path.dirname(filename), exist_ok=True)
      with open(filename, "w") as f:
        f.write(str(level))
    print("Successfully generated SR files!")

  def run_check(self):
    if self.timer_enabled == False:
      return
    threading.Timer(self.time_slider.get(), self.run_check).start()
    self.search()


root = tk.Tk()
root.geometry("350x430")
root.configure(background='#34495e')
app = Application(master=root)
app.mainloop()