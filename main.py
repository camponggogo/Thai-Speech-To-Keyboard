import speech_recognition as sr
import pyautogui
import time
import pyperclip
import pyttsx3

recognizer = sr.Recognizer()
mic = sr.Microphone()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

print("พูดข้อความ (ไทย/อังกฤษ) แล้วข้อความจะถูกวางลงในตำแหน่งที่โฟกัสคีย์บอร์ดอยู่\nหยุดโปรแกรมด้วย Ctrl+C")

listening = True

# พูดเมื่อเริ่มต้นรับคำสั่งเสียง
speak("คีย์บอร์ดคำสั่งเสียงพร้อมรับคำสั่ง กรุณาพูดคำสั่งได้เลย")

while True:
    try:
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            if listening:
                print("กำลังฟัง... (พูด 'หยุดการพิมพ์' เพื่อหยุดรับเสียง)")
            else:
                print("หยุดรับเสียงชั่วคราว (พูด 'เริ่มการพิมพ์' เพื่อเริ่มใหม่)")
            audio = recognizer.listen(source)
        try:
            # แปลงเสียงเป็นข้อความภาษาไทย
            text = recognizer.recognize_google(audio, language='th-TH')
        except sr.UnknownValueError:
            # ถ้าไม่เข้าใจภาษาไทย ลองอังกฤษ
            try:
                text = recognizer.recognize_google(audio, language='en-US')
            except sr.UnknownValueError:
                print("ไม่เข้าใจเสียงพูด ลองใหม่อีกครั้ง")
                continue
        print(f"ข้อความ: {text}")
        if listening:
            if text.strip() == "หยุดการพิมพ์":
                print("\n*** หยุดรับเสียงชั่วคราว ***\n")
                speak("หยุดรับคำสั่งแล้ว")
                listening = False
                continue
            # ใส่ข้อความลง clipboard
            pyperclip.copy(text)
            # Paste (Ctrl+V) ข้อความลงในตำแหน่งที่โฟกัสคีย์บอร์ดอยู่
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            time.sleep(0.5)
        else:
            if text.strip() == "เริ่มการพิมพ์":
                print("\n*** เริ่มรับเสียงใหม่ ***\n")
                speak("คีย์บอร์ดคำสั่งเสียงพร้อมรับคำสั่ง กรุณาพูดคำสั่งได้เลย")
                listening = True
            # ไม่ paste อะไรถ้าอยู่ในโหมดหยุด
    except KeyboardInterrupt:
        print("\nหยุดโปรแกรมแล้ว")
        break 