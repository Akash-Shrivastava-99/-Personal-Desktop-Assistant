from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtGui import QMovie
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import pyttsx3
import speech_recognition as sr
import os
import time
import webbrowser
import datetime
import wikipedia 
import speedtest
import smtplib
import requests 
from bs4 import BeautifulSoup 
import PyPDF2
import wolframalpha 
try:
    client=wolframalpha.Client()
except:
    print("some this was wrong with wolframalpha")



flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)



engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',120)

class mainT(QThread):

    contacts={'akash':'akash.sh560@gmail.com'}
    status=pyqtSignal(str)
    nova=pyqtSignal(str)
    user=pyqtSignal(str)

    def __init__(self):
        super(mainT,self).__init__()


    def speak(self,audio):
        self.nova.emit("NOVA :- "+audio)
        engine.say(audio)
        engine.runAndWait()

    def wish(self):
        hour = int(datetime.datetime.now().hour)
        
        if hour>=0 and hour <12:
            self.speak("Good morning")
        elif hour>=12 and hour<18:
            self.speak("Good Afternoon")
        else:
            self.speak("Good evening")

        self.speak(" I am Nova , and i will be your personal assistant. what can i do for you.  ")
        
    
    def sendEmail(self,mail, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('akash.shriv.testing590@gmail.com', 'Veena@123')
        server.sendmail('akash.shriv.testing590@gmail.com', mail, content)
        server.close()

    def pdf_reader(self):
        book=open("akash.pdf","rb")
        pdfReader=PyPDF2.PdfFileReader(book)
        pages= pdfReader.numPages
        self.speak("Total number of pages in this book is "+str(pages))
        
        page=pdfReader.getPage(0)
        text=page.extractText()
        self.speak(text) 

    def run(self):
        self.commands()
    
    def STT(self):
        R = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listning...........")
            self.status.emit("Listening...........")
          

            audio = R.listen(source)
        try:
            print("Recog......")
            self.status.emit("Recog......")
          
            text = R.recognize_google(audio,language='en-in')
            print(">> ",text)
        except Exception:
            self.speak("Sorry Speak Again")
            return "None"
        text = text.lower()
        self.user.emit("User :- "+text)
        return text
    def tellDay(self):
          
        day = datetime.datetime.today().weekday() + 1
    
        Day_dict = {1: 'Monday', 2: 'Tuesday', 
                    3: 'Wednesday', 4: 'Thursday', 
                    5: 'Friday', 6: 'Saturday',
                    7: 'Sunday'}
        
        if day in Day_dict.keys():
            day_of_the_week = Day_dict[day]
            self.speak("The day is " + day_of_the_week)

    def tellTime(self):
        time = str(datetime.datetime.now())
        hour = time[11:13]
        min = time[14:16]
        self.speak(self, "The time is sir" + hour + "Hours and" + min + "Minutes")

    def commands(self):
        self.wish()
        
        while True:
            self.query = self.STT()
            #speak("Did you say "+self.query)
            
            print(self.query)
            if 'goodbye' in self.query:
                self.speak("OK sir, goodbye ! ")
                sys.exit()
            
            
            elif ('read pdf' in self.query) or ('read book' in self.query):
                self.pdf_reader()

            elif ("play music" in self.query) or ("play song" in self.query):
                self.speak("Sure sir , here we go.")
                music_dir = 'C:\\Users\\Akash\\Desktop\\Major Project\\songs'
                songs = os.listdir(music_dir)    
                os.startfile(os.path.join(music_dir, songs[0]))

            elif "open a website" in self.query:
                self.speak("Sure sir, which website should i open?")
                web=self.STT().lower()
                self.speak("opening "+web)
                url= "https://www."+web+".com"
                webbrowser.open(url)

            elif 'open google' in self.query:
                
                self.speak("Sure sir, what should i search on google?")
                sc=self.STT().lower()
                self.speak("Searching google for "+sc)
                url= "https://www.google.com/search?q="+sc
                webbrowser.open(url)
                self.speak("opening google")

            elif 'wikipedia' in self.query:
                self.speak("Sure Sir, what should i search?")
                wiki=1
                while wiki==1:
                    wikiSc=self.STT().lower()
                    print(wikiSc)
                    try:
                        result=wikipedia.summary(wikiSc,sentences=4)
                        speak(result)
                        wiki=0
                    except:
                        self.speak("Something is wrong, Can you speak again")

            elif "check temperature" in self.query:
                self.speak("Sure Sir, checking current temperature ")
                try: 
                    search= "temperature in bhopal"
                    url= "https://www.google.com/search?q={"+search+"}"
                    r=requests.get(url)
                    data=BeautifulSoup(r.text,"html.parser")
                    temp=data.find("div",class_="BNeawe").text 
                    self.speak("It's "+temp + "  in Bhopal, Madhya Pradesh")
                except:
                    self.speak("Someting went wrong, Please try again after sometime ")

            elif "tell me your name" in self.query:
                speak("I am Nova. Your deskstop Assistant")

            elif "internet speed" in self.query:
                self.speak("Sure Sir, checking current internet speed ")
                try:
                    st=speedtest.Speedtest()
                    dl=st.download()
                    up=st.upload()
                    dl=dl/1000000
                    up=up/1000000
                    self.speak("Sir we have a downloading speed of "+str(round(dl))+"Mbps and an uploading speed of "+str(round(up))+" Mbps")
                except:
                    self.speak("Someting went wrong, Please try again after sometime ")


            elif ("make a note" in self.query) or ("write a note" in self.query):
                self.speak("what should I write , on the note ?")
                note=self.STT().lower()
                file1 = open("myfile.txt","a")
                file1.write(note)
                file1.close()
                self.speak("I have added this note")

            elif ("calculate" in self.query) or ("calculation" in self.query):
                self.speak("go ahead sir tell me what you want to calculate")
                eq=self.STT().lower()
                try:
                    res=client.query(self.query)
                    self.speak(next(res.results).text) 
                except:
                    self.speak("There is some internet issue please try again after some time")


            elif "send email" in self.query :
        
                try:
                    while True:
                        flage=False
                        self.speak("Sure Sir, whom should i send to ?")
                        to=self.STT() 
                        if to in self.contacts:
                            self.speak("What should I say?")
                            content = self.STT()
                            print(to,self.contacts[to],content) 

                            self.sendEmail(self.contacts[to], content)

                            self.speak("Email has been sent!")
                            break
                        else: 
                            self.speak("Sorry sir ! I am not able to find this person in our contact list")
                            self.speak("do you want add his name or search again ?")
                            while True:
                                ch=self.STT()
                                
                                corr="no"
                                if "add" in ch:
                                    self.speak("tell me his/her Email Id")
                                    
                                    while True:
                                        email=self.STT()
                                        self.speak("Email is "+email+" correct ?")
                                        corr=self.STT()
                                        if corr=="yes":
                                            self.contacts[to]=email
                                            break 
                                        else:
                                            self.speak("Please say it again")
                                    
                                    self.speak("added to contact successfully ")
                                    self.speak("Now what should i say in his/her Mail ?")
                                    content = self.STT()
                                    self.sendEmail(self.contacts[to], content)
                                    self.speak("Email has been sent!")
                                    flage=True
                                    break
                                
                                
                                elif "search" in ch:
                                    break
                                
                                else:
                                    self.speak("beg Pardon ")
                        
                        if flage:
                            break
                        

                            self.contacts[to]
                except Exception as e:
                    print(e)
                    self.speak("Sorry sir. I am not able to send this email")  

            #elif "set alarm" in self.query:
                #self.speak("Do you want me to set alarm for today?")
                #today=self.STT()
                #if "yes" in today:
                    #self.speak("okk sir, ")
                    #today=self.STT()

            elif "which day it is" in self.query:
                self.tellDay()
          
            elif "tell me the time" in self.query:
                self.tellTime()   
            
            
            else:
                #self.speak("again")
                try:
                    res=client.query(self.query)
                    self.speak(next(res.results).text) 
                except:
                    self.speak("There is some issue please try again after some time")
            self.speak("Anything else, I can do for you ? ")  




FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"./AI.ui"))

class Main(QMainWindow,FROM_MAIN):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(1920,1080)

        self.exitB.setStyleSheet("background-image:url(./img/exit - Copy.png);\n"
        "border:none;")
        self.exitB.clicked.connect(self.close)
        self.setWindowFlags(flags)

        self.movie= QMovie("./img/bot")
        self.botL.setMovie(self.movie)
    
        self.movie1= QMovie("./img/floor .gif")
        self.lowerL.setMovie(self.movie1)

        self.movie2= QMovie("./img/animation")
        self.bgL.setMovie(self.movie2)

        self.movie3= QMovie("./img/init")
        self.upperL.setMovie(self.movie3)

        self.startAnimation()
        self.Dspeak=mainT()
        self.startTask()
        self.Dspeak.status.connect(self.statusUpdate)
        self.Dspeak.nova.connect(self.doctorUpdate)
        self.Dspeak.user.connect(self.userUpdate)
        
    def statusUpdate(self,string):
        self.statusL.setText(string)

    def doctorUpdate(self,string):
        self.novaL.setText(string)
    
    def userUpdate(self,string):
        self.userL.setText(string)
        

    def startTask(self):
        self.Dspeak.start()
        

    def startAnimation(self):
        self.movie.start()
        self.movie1.start()
        self.movie2.start()
        self.movie3.start()
  
    # Stop Animation(According to need)
    def stopAnimation(self):
        self.movie.stop()
        self.movie1.stop()
        self.movie2.stop()
        self.movie3.stop()


app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
exit(app.exec_())