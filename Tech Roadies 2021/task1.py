from bs4 import BeautifulSoup
import requests
import random
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from xlrd import open_workbook

# Function to fetch all events from url
def get_events(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    event = soup.find_all("div", class_="event")
    return event

# Function to fetch "Description"
def get_event_summary(url):
    movie_page = requests.get(url)
    soup = BeautifulSoup(movie_page.text, 'html.parser')
    return soup.find_all("p")[5].contents[0]

# Function to fetch each event details
def get_events_info(event):
    k=0
    l=[1,3,5]
    event_title='title'
    date = 'date'
    time = 'time'
    event_url = event.a['href']
    for i in event.children:
        if k==1:
            event_title = i.b.contents[0]
        if k==3:
            date = i.b.contents[0]
        if k==5:
            time = i.b.contents[0]
        if k==13:
            event_url =i['href']
        k+=1
    return event_title,date,event_url,time


# Function to collect all events details
def event_collector():
    ctr = 0
    print("--------------------------------------------")

    
    for event in get_events('http://www.ieeeuvce.in/events/evold'):
        # Calling a function to fetch each event details
        raw_name,date,url,time = get_events_info(event)
        
        # Calling function to fetch "Description" of the event
        summary = get_event_summary('http://www.ieeeuvce.in'+url)

        # Setting up to write on an image by specifying template-name, color, font style
        image = Image.open('pic.jpg')
        draw = ImageDraw.Draw(image)
        newfont = ImageFont.truetype('Roboto-Regular.ttf', size=25)
        k=''
        name=''

        # Formatting Data
        for i in range(0,len(raw_name)):
            if i %45 ==0 and i!=0:
                name = name+"\n"
            name = name + raw_name[i] 
        for i in range(0,len(summary)):
            if i%40 ==0:
                k = k +'\n'
            k =k+ summary[i]
       
        s = "Name: "+name+"\n\nDate: "+date+"\n\nTime: "+time+"\n\nDescription :"+k

        # Writting on an image
        draw.text((90,100),s, font=newfont,  fill="#006CB3")
        image.save(raw_name+".jpg", resolution=100.0)

        # Printing Details to know what is fetched
        print(s)
        print('-----------------')
        

# Calling an event collector function
event_collector()

# Reading excel from Panadas
df = pd.read_excel('mydata.xlsx')
n = df.shape[1]-1
Name = df['Name'].tolist()
Email = df['Email'].tolist()
event =df['Event Name'].tolist()

# Sending mail to each of them in excel with specified event pic
for i in range(0,n):
    fromaddr = "nimitha1jagadeesha@gmail.com"
    toaddr = Email[i]
    msg = MIMEMultipart()
    
    # Initializing From address, To address and Subject
    msg['From'] = fromaddr 
    msg['To'] = toaddr 
    msg['Subject'] = "TECH ROADIES"

    # Writing Body of the mail
    body = "Hello, "+Name[i]
    msg.attach(MIMEText(body, 'plain'))
    
    filename = event[i]+".jpg"
    attachment = open(event[i]+".jpg", "rb") 
    p = MIMEBase('application', 'octet-stream') 
    p.set_payload((attachment).read()) 
    encoders.encode_base64(p)
    
    #Attaching particular event pic
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
    msg.attach(p)

    
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, "<Password>")
    text = msg.as_string() 
    s.sendmail(fromaddr, toaddr, text) 
    s.quit() 

