import tkinter as tk
from tkinter import ttk
from datetime import datetime
import pygame

# Initializing audio mixer and setting the wav alarm files
pygame.mixer.init(42050, -16, 2, 2048)
alarm_sound1 = pygame.mixer.Sound("MyAlarm.wav")
alarm_sound3 = pygame.mixer.Sound("MyAlarm2.mp3")
alarm_sound2 = pygame.mixer.Sound("Kesariya.wav.mp3")
# alarm_sound4 = pygame.mixer.Sound("illahi.mp3")


# Setting initial global values
start_printed = False
stop_printed = True
done = False
finished = False
stop_clicked = False

class AlarmApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Alarm Clock")
        self.resizable(width=False, height=False)

        # Variables for hour, minute, AM/PM, and selected alarm sound
        self.hr = tk.IntVar(self)
        self.min = tk.IntVar(self)
        self.ampm = tk.StringVar(self)
        self.alarm_sound_var = tk.StringVar(self)  # Variable to store selected alarm sound

        # Initial values for dropdown lists
        self.hr.set('12')
        self.min.set("00")
        self.ampm.set("AM")
        self.alarm_sound_var.set("Ringtone")

        # Lists for dropdown menu options
        hours = [x for x in range(1, 13)]
        minutes = ["%02d" % y for y in range(0, 60)]
        ampmlist = ["AM", "PM"]
        alarm_sounds = ["MyAlarm1", "MyAlarm2","Kesariya"] #"llahi"

        # Creating dropdown menus
        self.popmenuhours = tk.OptionMenu(self, self.hr, *hours)
        self.thing = tk.Label(text=":").pack(side="left")
        self.popmenuminutes = tk.OptionMenu(self, self.min, *minutes)
        self.popmenuAMPM = tk.OptionMenu(self, self.ampm, *ampmlist)
        self.popmenuAlarms = tk.OptionMenu(self, self.alarm_sound_var, *alarm_sounds)

        # Placing dropdown menus on the window
        self.popmenuhours.pack(side="left")
        self.thing = tk.Label(text=":").pack(side="left")
        self.popmenuminutes.pack(side="left")
        self.popmenuAMPM.pack(side="left")
        self.popmenuAlarms.pack(side="left")

        # Buttons for controlling the alarm
        self.alarmbutton = tk.Button(self, text="Set Alarm", command=self.start_clock)
        self.cancelbutton = tk.Button(self, text="Cancel Alarm", command=self.stop_clock, state="disabled")
        self.stopalarmbutton = tk.Button(self, text="Stop Alarm", command=self.stop_audio, state="disabled")

        # Placing buttons on the window
        self.alarmbutton.pack()
        self.cancelbutton.pack()
        self.stopalarmbutton.pack()

    def start_clock(self):
        global done, start_printed, stop_printed, stop_clicked
        if done == False:
            self.cancelbutton.config(state="active")
            self.alarmbutton.config(state="disabled")
            if start_printed == False:
                print(f"Alarm set for {self.hr.get()}:{'%02d' % self.min.get()}{self.ampm.get()}. Using {self.alarm_sound_var.get()} as the alarm sound.")
                start_printed = True
                stop_printed = False

            if self.ampm.get() == "AM":
                hour_value = self.hr.get() if 1 <= self.hr.get() <= 11 else self.hr.get() - 12
            else:  # PM
                hour_value = self.hr.get() + 12 if 1 <= self.hr.get() <= 11 else self.hr.get()

            alarm_sound = alarm_sound1 if self.alarm_sound_var.get() == "MyAlarm1" else alarm_sound2
            self.Alarm("%02d" % hour_value, "%02d" % self.min.get(), alarm_sound)

        if stop_clicked == True:
            done = False
            start_printed = False
            stop_clicked = False

    def stop_clock(self):
        global done, stop_clicked
        print(f"Alarm set for {self.hr.get()}:{'%02d' % self.min.get()}{self.ampm.get()} has been cancelled.")
        stop_clicked = True
        done = True
        self.cancelbutton.config(state="disabled")
        self.alarmbutton.config(state="active")

    def stop_audio(self):
        pygame.mixer.Sound.stop(alarm_sound1)
        pygame.mixer.Sound.stop(alarm_sound3)
        pygame.mixer.Sound.stop(alarm_sound2)
        self.stopalarmbutton.config(state="disabled")
        self.alarmbutton.config(state="active")

    def Alarm(self, myhour, myminute, alarm_sound):
        global done, start_printed, finished
        if done == False:
            myhour, myminute = str(myhour), str(myminute)
            a = str(datetime.now())
            b = a.split(" ")[1].split(":")
            hour = b[0]
            minute = b[1]

            if hour == myhour and minute == myminute:
                pygame.mixer.Sound.play(alarm_sound, loops=-1)
                print(f"Alarm is ringing! Using {self.alarm_sound_var.get()} as the alarm sound.")
                done = True
                finished = True
                self.cancelbutton.config(state="disabled")
                self.stopalarmbutton.config(state="active")
            else:
                self.after(1000, self.start_clock)
            done = False

        if finished == True:
            start_printed = False
            finished = False

app = AlarmApp()
app.mainloop()

