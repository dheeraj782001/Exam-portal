import tkinter as tk
from tkinter import ttk, LEFT, END
from tkinter import messagebox as ms

import time
import numpy as np
#from mcq import startquiz as s
import cv2

import os
from PIL import Image , ImageTk     
from PIL import Image # For face recognition we will the the LBPH Face Recognizer 

##############################################+=============================================================



root = tk.Tk()
root.configure(background="white")
#root.geometry("1300x700")
import sqlite3
my_conn = sqlite3.connect('face.db')

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Online Exam Portal System")


#++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
#image2 =Image.open('face.jpg')
#image2 =image2.resize((w,h), Image.ANTIALIAS)

#background_image=ImageTk.PhotoImage(image2)

#background_label = tk.Label(root, image=background_image)

#background_label.image = background_image

#background_label.place(x=0, y=0) #, relwidth=1, relheight=1)


lbl = tk.Label(root, text="Online Exam Portal System", font=('times', 25,' bold '), height=1, width=60,bg="white",fg="black")
lbl.place(x=0, y=0)

img = Image.open('o4.jpg')
img = img.resize((190,150), Image.ANTIALIAS)
logo_image = ImageTk.PhotoImage(img)

logo_label = tk.Label(root, image=logo_image)
logo_label.image = logo_image
logo_label.place(x=620, y=300)

frame_alpr = tk.LabelFrame(root, text=" --Dashboard-- ", width=1300, height=100, bd=5, font=('times', 15, ' bold '),bg="white")
frame_alpr.grid(row=0, column=0, sticky='nw')
frame_alpr.place(x=40, y=40)


################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 


def Create_database():
        
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    cap = cv2.VideoCapture(0)
    
#    id = input('enter user id')
    id=entry2.get()
    
    sampleN=0;
    
    while 1:
    
        ret, img = cap.read()
    
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
        for (x,y,w,h) in faces:
    
            sampleN=sampleN+1;
    
            cv2.imwrite("facesData/User."+str(id)+ "." +str(sampleN)+ ".jpg", gray[y:y+h, x:x+w])
    
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    
            cv2.waitKey(100)
    
        cv2.imshow('img',img)
    
        cv2.waitKey(1)
    
        if sampleN > 40:
    
            break
    
    cap.release()
    entry2.delete(0,'end')
    cv2.destroyAllWindows()



def Train_database():
           
    recognizer =cv2.face.LBPHFaceRecognizer_create();
    
    path="C:/Users/Motti/Desktop/online_exam/facesData"
    
    def getImagesWithID(path):
    
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]   
    
     # print image_path   
    
     #getImagesWithID(path)
    
        faces = []
    
        IDs = []
    
        for imagePath in imagePaths:      
    
      # Read the image and convert to grayscale
    
            facesImg = Image.open(imagePath).convert('L')
    
            faceNP = np.array(facesImg, 'uint8')
    
            # Get the label of the image
    
            ID = int(os.path.split(imagePath)[-1].split(".")[1])
    
             # Detect the face in the image
    
            faces.append(faceNP)
    
            IDs.append(ID)
    
            cv2.imshow("Adding faces for traning",faceNP)
    
            cv2.waitKey(10)
    
        return np.array(IDs), faces
    
    Ids,faces  = getImagesWithID(path)
    
    recognizer.train(faces,Ids)
    
    recognizer.save("trainingdata.yml")
    
    cv2.destroyAllWindows()

    
def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
        #return abc
    
    print("Stored blob data into: ", filename, "\n")
    return filename
def update_label(str_T):
    #clear_img()
    result_label = tk.Label(root, text=str_T, width=40, font=("bold", 25), bg='bisque2', fg='black')
    result_label.place(x=300, y=100)    
def exam():
    from subprocess import call
    call(["python", "mcq.py"]) 

def Test_database():
    flag=0
    recognizer = cv2.face.LBPHFaceRecognizer_create(1, 8, 8, 8, 100)
#    recognizer = cv2.face.FisherFaceRecognizer(0, 3000);
    
    recognizer.read('trainingdata.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    #iniciate id counter
    id = 0
    
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    
    while True:
         ret, img =cam.read()
#        img = cv2.flip(img, -1) # Flip vertically
         gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
         faces=faceCascade.detectMultiScale(gray,1.3,8,minSize = (int(minW), int(minH)))
#        faces = faceCascade.detectMultiScale( 
#            gray,
#            scaleFactor = 1.2,
#            minNeighbors = 5,
#            minSize = (int(minW), int(minH)),
#           )
         for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
            # If confidence is less them 100 ==> "0" : perfect match
            
            if (confidence < 60):
                #print(id)
                #name = names[id]
                id = id
                
                print(type(id))
                
                #
                #id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
               
                         
                cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
                cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(255,255,0),1)
                 
                my_conn = sqlite3.connect('evaluation.db')
               
              
                update_label("Student Identified Successfully !!")
                if(str(id)==str(id)):
                     sqliteConnection = sqlite3.connect('evaluation1.db')
                     cursor = sqliteConnection.cursor()
                     print("Connected to SQLite")
                    
                     sql_fetch_blob_query = cursor.execute("select * from registration where rollno =" + str(id) +"");
                     #cursor.execute(sql_fetch_blob_query, (id,))
                     record = cursor.fetchall()
                     for row in record:
                         print("Roll_No = ", row[0],"Fullname = ", row[1], "address = ", row[2], "Email =", row[3],"Phoneno =", row[4],"Gender =", row[5],"age =", row[6],"photo =", row[7])
                         RollNo= row[0]
                         Fullname = row[1]
                         address = row[2]
                         Email = row[3]
                         Phoneno = row[4]
                         Gender = row[5]
                         age = row[6]
                         photo = row[7]
                         photoPath = "C:/Users/Motti/Desktop/online_exam/profile images" + Fullname + ".jpg"
                         ph=writeTofile(photo, photoPath)
                         load = Image.open(ph)
                         render = ImageTk.PhotoImage(load)
                         
                                        #img.place(x=0, y=0)
                                        #resumeFile = row[3]
                         frame_display = tk.LabelFrame(root, text=" --Display-- ", width=600, height=550, bd=5, font=('times', 14, ' bold '),bg="white")
                         frame_display.grid(row=0, column=0, sticky='nw')
                         frame_display.place(x=730, y=150)
                         l9 = tk.Label(frame_display, text="Roll No :"+str(RollNo),
                                       font=("Times new roman", 18, "bold"), bg="snow")
                         l9.place(x=50, y=50)
                                        
                         l1 = tk.Label(frame_display, text="Fullname :" +str(Fullname), 
                                         font=("Times new roman", 18, "bold"), bg="snow")
                         l1.place(x=50, y=100)
                         l2 = tk.Label(frame_display, text="Address :"+str(address), 
                                                        font=("Times new roman", 18, "bold"), bg="snow")
                         l2.place(x=50, y=150)
                         l3 = tk.Label(frame_display, text="Email :"+str(Email), 
                                                      font=("Times new roman", 18, "bold"), bg="snow")
                         l3.place(x=50, y=200)
                         l4 = tk.Label(frame_display, text=" Phone No :"+str(Phoneno), 
                                                        font=("Times new roman", 18, "bold"), bg="snow")
                         l4.place(x=50, y=250)
                         l5 = tk.Label(frame_display, text=" Gender :"+str(Gender), 
                                                        font=("Times new roman", 18, "bold"), bg="snow")
                         l5.place(x=50, y=300)
                         l6 = tk.Label(frame_display, text=" Age :   "+str(age), 
                                                        font=("Times new roman", 18, "bold"), bg="snow")
                         l6.place(x=50, y=350)
                         l7 = tk.Label(frame_display,text="Profile Photo   ", image=render, 
                                                        font=("Times new roman", 18, "bold"), bg="snow")
                         l7.image = render
                         l7.place(x=400, y=50)
                        # cv2.imshow('camera',img) 
                         button3 = tk.Button(frame_display, text="Start Exam", command=exam, width=20, height=1, font=('times', 15, ' bold '),bg="green",fg="white")
                         button3.place(x=200, y=420)
                         
                         # button3 = tk.Button(frame_display, text="Start Exam", command=exam, width=20, height=1, font=('times', 15, ' bold '),bg="yellow4",fg="white")
                         # button3.place(x=200, y=620)
                         cam.release()
                         cv2.destroyAllWindows() 
                         #cv2.imshow('camera',img)
                              
              
                else:
#                
                    id = "unknown Student Identified"
                    confidence = "  {0}%".format(round(100 - confidence))
                    cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
                    cv2.putText(img,str(confidence),(x+5,y+h-5),font,1,(255,255,0),1)  
                    cam.release() 

def student():
    
##### tkinter window ######
    
    print("Student Registration")
    from subprocess import call
    call(["python", "student_registration.py"]) 


            
        
        
            
    



#################################################################################################################
def window():
    root.destroy()


button1 = tk.Button(root, text="Student Registration", command=student,width=15, height=1, font=('times', 15, ' bold '),bg="grey",fg="black")
button1.place(x=60, y=70)

button1 = tk.Button(root, text="Create Face Data", command=Create_database,width=15, height=1, font=('times', 15, ' bold '),bg="grey",fg="black")
button1.place(x=250, y=70)

entry2=tk.Entry(root,bd=4,width=8)
entry2.place(x=440, y=70)

button2 = tk.Button(root, text="Train Face Data", command=Train_database, width=20, height=1, font=('times', 15, ' bold '),bg="grey",fg="black")
button2.place(x=500, y=70)

button3 = tk.Button(root, text="Exam Portal", command=Test_database, width=20, height=1, font=('times', 15, ' bold '),bg="grey",fg="black")
button3.place(x=750, y=70)

exit = tk.Button(root, text="Exit", command=window, width=20, height=1, font=('times', 15, ' bold '),bg="red",fg="white")
exit.place(x=1000, y=70)

label_l1 = tk.Label(root, text="Project By:",font=("Times New Roman", 20, 'bold'),
                    background="white", fg="black", width=35, height=1)
label_l1.place(x=400, y=440)
label_l1 = tk.Label(root, text="College Of Engineering,Manjiri",font=("Times New Roman", 20, 'bold'),
                    background="white", fg="black", width=40, height=1)
label_l1.place(x=350, y=500)
label_l1 = tk.Label(root, text="DEPARTMENT OF COMPUTER ENGINEERING",font=("Times New Roman", 20, 'bold'),
                    background="white", fg="black", width=40, height=1)
label_l1.place(x=350, y=550)

root.mainloop()