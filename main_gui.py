import speech_recognition as sr
import pyautogui
import time
import pyperclip
import pyttsx3
import threading
import tkinter as tk
from tkinter import ttk

recognizer = sr.Recognizer()
mic = sr.Microphone()
engine = pyttsx3.init()

# ฟังก์ชันพูด
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ฟังก์ชันอัปเดตสถานะใน GUI
def set_status(text, color):
    status_var.set(text)
    status_label.config(bg=color)
    root.update_idletasks()

# ฟังก์ชันหลักสำหรับรับเสียง
listening = True
running = True

def listen_loop():
    global listening, running
    while running:
        try:
            with mic as source:
                set_status("กำลังฟัง...", "#ffe066")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language='th-TH')
            except sr.UnknownValueError:
                try:
                    text = recognizer.recognize_google(audio, language='en-US')
                except sr.UnknownValueError:
                    set_status("ไม่เข้าใจเสียงพูด ลองใหม่อีกครั้ง", "#ff6666")
                    text_var.set("")
                    time.sleep(1)
                    continue
            print(f"ข้อความ: {text}")
            text_var.set(text)
            if listening:
                if text.strip() == "หยุดการพิมพ์":
                    set_status("หยุดรับคำสั่งแล้ว", "#ff6666")
                    speak("หยุดรับคำสั่งแล้ว")
                    listening = False
                    continue
                pyperclip.copy(text)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.press('enter')
                set_status("พร้อมรับคำสั่งเสียง", "#66ff66")
                time.sleep(0.5)
            else:
                if text.strip() == "เริ่มการพิมพ์":
                    set_status("พร้อมรับคำสั่งเสียง", "#66ff66")
                    speak("คีย์บอร์ดคำสั่งเสียงพร้อมรับคำสั่ง กรุณาพูดคำสั่งได้เลย")
                    listening = True
                # ไม่ paste อะไรถ้าอยู่ในโหมดหยุด
        except Exception as e:
            print(f"Error: {e}")
            set_status("เกิดข้อผิดพลาด", "#ff6666")
            text_var.set("")
            time.sleep(1)

# สร้าง GUI
root = tk.Tk()
root.title("Speed to Tech Keyboard - Voice Command Status")
root.geometry("400x150")
root.resizable(False, False)

status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, font=("TH Sarabun New", 24), width=30, height=2)
status_label.pack(pady=(20, 5))

# เพิ่ม label สำหรับแสดงข้อความที่แปลงได้
text_var = tk.StringVar()
text_label = tk.Label(root, textvariable=text_var, font=("TH Sarabun New", 28), fg="#222222")
text_label.pack(pady=(0, 10))

set_status("พร้อมรับคำสั่งเสียง", "#66ff66")
speak("คีย์บอร์ดคำสั่งเสียงพร้อมรับคำสั่ง กรุณาพูดคำสั่งได้เลย")

def on_close():
    global running
    running = False
    root.destroy()

close_btn = ttk.Button(root, text="ปิดโปรแกรม", command=on_close)
close_btn.pack(pady=5)

# รัน listen_loop ใน thread แยก
threading.Thread(target=listen_loop, daemon=True).start()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop() 