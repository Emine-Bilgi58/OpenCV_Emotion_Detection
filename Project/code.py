import cv2
import dlib
from math import hypot
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import sqlite3
import time
import datetime

cap = cv2.VideoCapture(0)

con = sqlite3.connect('hasta_bilgisi.db')
c = con.cursor()

face_detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
font = cv2.FONT_HERSHEY_SIMPLEX

while 1:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray)
    cv2.putText(frame, "Lutfen Kameraya Bakiniz", (10, 50), font, 1, (0, 0, 250), 1)

    for face in faces:

        landmarks = predictor(gray, face)

        left_point = (landmarks.part(48).x, landmarks.part(48).y)
        right_point = (landmarks.part(64).x, landmarks.part(64).y)

        up_point = (landmarks.part(62).x, landmarks.part(62).y)
        down_point = (landmarks.part(66).x, landmarks.part(66).y)

        eyebrow1_point = (landmarks.part(21).x, landmarks.part(21).y)
        eyebrow2_point = (landmarks.part(22).x, landmarks.part(22).y)

        nose_point = (landmarks.part(27).x, landmarks.part(27).y)

        nose_point1 = (landmarks.part(31).x, landmarks.part(31).y)
        nose_point2 = (landmarks.part(35).x, landmarks.part(35).y)

        eye_down_point = (landmarks.part(37).x, landmarks.part(37).y)
        eye_up_point = (landmarks.part(41).x, landmarks.part(41).y)

        eye_right_point = (landmarks.part(36).x, landmarks.part(36).y)
        eye_left_point = (landmarks.part(39).x, landmarks.part(39).y)

        hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        vertical_line_lenght = hypot((up_point[0] - down_point[0]), (up_point[1] - down_point[1]))
        eyebrow1_nose_line_lenght = hypot((eyebrow1_point[0] - nose_point[0]), (eyebrow1_point[1] - nose_point1[1]))
        eyebrow1_eyebrow2_line_lenght = hypot((eyebrow1_point[0] - eyebrow2_point[0]), (eyebrow1_point[1] - eyebrow2_point[1]))
        nose_lip_right_line_lenght = hypot((nose_point1[0] - left_point[0]), (nose_point1[1] - left_point[1]))
        eye_vertical_line_lenght = hypot((eye_down_point[0] - eye_up_point[0]), (eye_down_point[1] - eye_up_point[1]))
        eye_hor_line_lenght = hypot((eye_right_point[0] - eye_left_point[0]), (eye_right_point[1] - eye_left_point[1]))

        ratio1 = (hor_line_lenght / (vertical_line_lenght + 1))
        ratio2 = (eyebrow1_nose_line_lenght / (eyebrow1_eyebrow2_line_lenght + 1))
        ratio3 = (nose_lip_right_line_lenght / (hor_line_lenght + 1))
        ratio4 = (eye_hor_line_lenght / (eye_vertical_line_lenght + 1))

        veri = ""

        if 2 < ratio1 and ratio3 < 0.5:
            cv2.putText(frame, "Iyi gorunuyorsun", (10,100), font, 1, (255, 0, 0), 1)
            veri += "İyi görünüyorsun."

        elif (3 >= ratio4 >= 2) :
            cv2.putText(frame, "Normal gorunuyorsun", (10,100), font, 1, (255, 0, 0), 1)
            veri += "Normal görünüyorsun. Böyle devam et!"

        elif 3.1 <= ratio4:
            cv2.putText(frame, "Halsiz gorunuyorsun", (10,100), font, 1, (255, 0, 0), 1)
            veri += "Halsiz görünüyorsun. Bir yerin ağrıyor ya da gerçekten halsiz misin?"


    cv2.imshow("frame",frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        if veri == "Normal görünüyorsun. Böyle devam et!" or veri == "İyi görünüyorsun.":
            messagebox.showinfo("Kayıt", veri)
        else:
            Msgbox = messagebox.askquestion("Önemli", veri, icon='warning')

            if Msgbox == 'yes':
                def tabloolustur():
                    c.execute("CREATE TABLE IF NOT EXISTS hasta(ad TEXT, bilgi TEXT, tarih TEXT)")

                pencere = Tk()
                pencere.title("BİLGİ")
                pencere.state('zoomed')

                ad_label = Label(pencere, text='Adınız ve Soyadınız:',font="Verdana 10 bold", bg='#add8e6')
                ad_label.pack(padx=10, pady=10, anchor=N)

                ad = tk.StringVar()
                ad_entry = Entry(pencere, textvariable=ad)
                ad_entry.pack(padx=10, pady=15)

                uyari = Label(pencere, text='Lütfen aşağıdaki alana rahatsızlıklarınızı giriniz:', font="Verdana 10 bold",bg='#add8e6')
                uyari.pack(padx=10, pady=20, anchor=N)

                bilgi = tk.StringVar()
                bilgi_entry = Entry(pencere, textvariable=bilgi)
                bilgi_entry.pack(padx=10, pady=25)

                def gonder():
                    print(dir(ad_entry))
                    con = sqlite3.connect('hasta_bilgisi.db')
                    c = con.cursor()
                    zaman = time.time()
                    tarih = str(datetime.datetime.fromtimestamp(zaman).strftime("%Y-%m-%d %H-%M-%S"))
                    c.execute("INSERT INTO hasta(ad, bilgi, tarih) VALUES(?,?,?)", (ad_entry.get(), bilgi_entry.get(), tarih))
                    con.commit()

                gonder_butonu = Button(pencere, text="Gönder", command=gonder)
                gonder_butonu.pack(padx=10, pady=30, anchor=S)

                tabloolustur()
                pencere.mainloop()

        break

con.close()
cap.release()
cv2.destroyAllWindows()