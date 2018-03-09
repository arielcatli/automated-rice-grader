import tkinter as tk
from tkinter import ttk
import led


class GUI:
    def __init__(self):
        self.__led = led.LED()
        self.__root = tk.Tk()
        self.__root.title("GUI")
        self.__main_frame = ttk.Frame(self.__root, padding=50)
        self.__main_frame.pack(fill=tk.BOTH, expand=True)
        self.__root.attributes("-fullscreen", True)
        
        
        self.__btn_capture = tk.Button(self.__main_frame, text="CAPTURE", width = 50, height=3)
        self.__btn_capture.pack()
        self.__btn_view_grains = tk.Button(self.__main_frame,  text="VIEW GRAINS", width = 50, height=3, state=tk.DISABLED)
        self.__btn_view_grains.pack()
        self.__btn_grade = tk.Button(self.__main_frame, state=tk.DISABLED, text="GRADE", width = 50, height=3)
        self.__btn_grade.pack()
        self.__btn_log = tk.Button(self.__main_frame, text="LOG", width = 50, height=3)
        self.__btn_log.pack()
        self.__btn_LED_ON = tk.Button(self.__main_frame, text="LED ON", width = 50, height=3, command=self.__led_on)
        self.__btn_LED_ON.pack()
        self.__btn_LED_OFF = tk.Button(self.__main_frame, text="LED OFF", width = 50, height=3, command=self.__led_off, state=tk.DISABLED)
        self.__btn_LED_OFF.pack()
        self.__btn_shutdown = tk.Button(self.__main_frame, text="SHUTDOWN", width = 50, height=3, command=self.__exit)
        self.__btn_shutdown.pack()
        
        
        self.__root.mainloop()
        
    def __led_on(self):
        self.__btn_LED_OFF.config(state=tk.NORMAL)
        self.__btn_LED_ON.config(state=tk.DISABLED)
        self.__led.on()
    
    def __led_off(self):
        self.__btn_LED_ON.config(state=tk.NORMAL)
        self.__btn_LED_OFF.config(state=tk.DISABLED)
        self.__led.off()

    def __exit(self):
        self.__close(self.__root)
        
    def __close(self, window):
        window.destroy()
if __name__ == "__main__":
    gui = GUI()
