# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 16:37:36 2021

@author: sheet
"""

import sqlite3
import tkinter  as tk 
from tkinter import * 
import time
import numpy as np

import os
from PIL import Image # For face recognition we will the the LBPH Face Recognizer 
from PIL import Image , ImageTk  

root = tk.Tk()
#root.geometry('500x500')
#root.title("Login Form")


#------------------------------------------------------

root.configure(background="seashell2")
#root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Online Exam Portal")
#------------------Frame----------------------



#-------function------------------------

def reg():
    
##### tkinter window ######
    
    print("reg")
    from subprocess import call
    call(["python", "face_registration.py"])   



def login():
    
##### tkinter window ######
    
    print("log")
    from subprocess import call
    call(["python", "face_login.py"])   
    
def window():
    root.destroy()

#++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
image2 =Image.open('o3.jpg')
image2 =image2.resize((w,h), Image.ANTIALIAS)

background_image=ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0) #, relwidth=1, relheight=1)


lbl = tk.Label(root, text="College of Engineering, Manjiri", font=('times', 30,' bold '), height=1, width=50,bg="black",fg="white")
lbl.place(x=100, y=5)

lbl = tk.Label(root, text="'Welcome to Online Exam Poratl System' ", font=('times', 25,' bold '), height=1, width=50,bg="black",fg="white")
lbl.place(x=200, y=600)

#framed = tk.LabelFrame(root, text=" --WELCOME-- ", width=500, height=250, bd=5, font=('times', 14, ' bold '),bg="pink")
#framed.grid(row=0, column=0, sticky='nw')
#framed.place(x=450, y=300)
#++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
button1 = tk.Button(root, text='Login Now',width=20,height=2,bg='blue',fg='black',command=login,font='bold').place(x=950,y=60)
button1 = tk.Button(root, text='Register',width=20,height=2,bg='green',fg='black',command=reg,font='bold').place(x=1150,y=60)
button1 = tk.Button(root, text='Exit',width=20,height=2,bg='red',fg='black',command=window,font='bold').place(x=1030,y=130)

root.mainloop()
