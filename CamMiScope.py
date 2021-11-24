import sys
import configparser
import cv2
from PIL import Image, ImageTk
import tkinter as tk


def apply_brightness_contrast(input_img, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    return buf


class SettingWC:
    adj_br = 0
    adj_cn = 0
    prednastroika = 0

    def __init__(self):
        self.SettingW = tk.Tk()

        def on_closing():
            destructor()

        self.SettingW.protocol("WM_DELETE_WINDOW", on_closing)
        self.SettingW.wm_title("Settings")
        PROP_EXPOSURE = tk.Scale(self.SettingW, length=250, from_=-13, to=-1, orient=tk.HORIZONTAL)
        PROP_BRIGHTNESS = tk.Scale(self.SettingW, length=250, from_=1, to=255, orient=tk.HORIZONTAL)
        adj_brightness = tk.Scale(self.SettingW, length=250, from_=-127, to=127, orient=tk.HORIZONTAL)
        adj_contrast = tk.Scale(self.SettingW, length=250, from_=-127, to=127, orient=tk.HORIZONTAL)
        label_EXPOSURE = tk.Label(self.SettingW, text="EXPOSURE")
        label_BRIGHTNESS = tk.Label(self.SettingW, text="BRIGHTNESS")
        label_adj_brightness = tk.Label(self.SettingW, text="adj_brightness")
        label_adj_contrast = tk.Label(self.SettingW, text="adj_contrast")

        label_EXPOSURE.grid(row=0, column=0)
        PROP_EXPOSURE.grid(row=0, column=1)
        label_BRIGHTNESS.grid(row=1, column=0)
        PROP_BRIGHTNESS.grid(row=1, column=1)
        label_adj_brightness.grid(row=2, column=0)
        adj_brightness.grid(row=2, column=1)
        label_adj_contrast.grid(row=3, column=0)
        adj_contrast.grid(row=3, column=1)

        def button_Default_Callback():
            PROP_EXPOSURE.set(-13)
            PROP_BRIGHTNESS.set(1)
            adj_brightness.set(0)
            adj_contrast.set(0)

        def button_Restore_Callback():
            # create configparser object
            config_file = configparser.ConfigParser()
            config_file.read("Settings.ini")
            PROP_EXPOSURE.set(config_file["Settings"]["PROP_EXPOSURE"])
            PROP_BRIGHTNESS.set(config_file["Settings"]["PROP_BRIGHTNESS"])
            adj_brightness.set(config_file["Settings"]["adj_brightness"])
            adj_contrast.set(config_file["Settings"]["adj_contrast"])

        def button_Save_Callback():
            # create configparser object
            config_file = configparser.ConfigParser()
            # define sections and their key and value pairs
            config_file["Settings"] = {
                "PROP_EXPOSURE": PROP_EXPOSURE.get(),
                "PROP_BRIGHTNESS": PROP_BRIGHTNESS.get(),
                "adj_brightness": adj_brightness.get(),
                "adj_contrast": adj_contrast.get()
            }
            # SAVE CONFIG FILE
            with open("Settings.ini", "w") as file_object:
                config_file.write(file_object)

        button_Default = tk.Button(self.SettingW, text="Default", command=button_Default_Callback)
        button_Default.grid(row=4, column=0)
        button_Restore = tk.Button(self.SettingW, text="Restore", command=button_Restore_Callback)
        button_Restore.grid(row=4, column=1)
        button_Save = tk.Button(self.SettingW, text="Save", command=button_Save_Callback)
        button_Save.grid(row=4, column=2)

        def update_setting():
            if (self.SettingW.focus_get() != None) or (SettingWC.prednastroika == 0):
                cap.set(cv2.CAP_PROP_EXPOSURE, PROP_EXPOSURE.get())  # Выдержка -13...-1
                cap.set(cv2.CAP_PROP_BRIGHTNESS, PROP_BRIGHTNESS.get())  # Яркость 1...255
                SettingWC.adj_br = adj_brightness.get()
                SettingWC.adj_cn = adj_contrast.get()
                SettingWC.prednastroika = 1
            self.SettingW.after(500, update_setting)

        button_Restore_Callback()
        update_setting()


if __name__ == '__main__':
    window = tk.Tk()


    def on_closing():
        destructor()


    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.wm_title("Digital Microscope")
    window.attributes('-fullscreen', True)
    window.bind("<F11>", lambda event: window.attributes("-fullscreen", not window.attributes("-fullscreen")))
    window.bind("<Escape>", lambda event: destructor())
    # window.window = tk.Tk()  # Makes main window
    window.config(background="#FFFFFF")
    # Graphics window
    imageFrame = tk.Frame(window, width=1920, height=1080)
    imageFrame.grid(row=0, column=0, padx=0, pady=0)
    # Capture video frames
    lmain = tk.Label(imageFrame)
    lmain.grid(row=0, column=0)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)  # Частота кадров
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Ширина кадров в видеопотоке.
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Высота кадров в видеопотоке.
    cap.set(cv2.CAP_PROP_EXPOSURE, -13)  # Выдержка -13...-1
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 1)  # Яркость 1...255


    def destructor():
        cap.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application
        sys.exit()


    def show_frame():
        _, frame = cap.read()
        frame = apply_brightness_contrast(frame, SWC.adj_br, SWC.adj_cn)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        imgtk = ImageTk.PhotoImage(image=Image.fromarray(cv2image))
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        window.after(6, show_frame)


    SWC = SettingWC();
    show_frame()  # Display
    window.mainloop()
    SWC.mainloop()
