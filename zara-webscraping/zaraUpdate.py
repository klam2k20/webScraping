import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib, ssl
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

'''
Kenny Lam
Last Update: 4/30
Scrapes data from zara's many webpages, allowing users to filter through the many items
based on priced. Before emailing users a table with all items that fall below the maximum
price set.
'''
#---------------------------------Website Dictionary------------------------------------
zaraMen = {
    1 : "https://www.zara.com/us/en/man-jackets-l640.html?v1=1445065",
    2 : "https://www.zara.com/us/en/man-blazers-l608.html?v1=1445073",
    3 : "https://www.zara.com/us/en/man-knitwear-l681.html?v1=1445118",
    4 : "https://www.zara.com/us/en/man-trousers-l838.html?v1=1445268",
    5 : "https://www.zara.com/us/en/man-jeans-l659.html?v1=1445083",
    6 : "https://www.zara.com/us/en/man-shirts-l737.html?v1=1445099",
    7 : "https://www.zara.com/us/en/man-sweatshirts-l821.html?v1=1445292",
    8 : "https://www.zara.com/us/en/man-special-prices-l806.html?v1=1445161",
    9 : "https://www.zara.com/us/en/man-recommended-for-you-l1801.html?v1=726002",
    } 

#-------------------------------User Output/Input-----------------------------
print("Which website would you like to search through? \n 1. Zara")
answer = input()

#-------------------------------Zara Men-------------------------------------
if answer == "1":
    print("Men Categories:\n 1. Jackets\n 2. Blazers\n 3. Knitwear\n 4. Pants\n 5. Jeans\n 6. Shirts\n 7. Sweatshirts\n 8. Special Prices\n 9. Best Sellers")
    category = input()
    page = requests.get(zaraMen[int(category)])
    zaraContent = BeautifulSoup(page.content, 'html.parser')
    item = zaraContent.find_all(class_="name _item")
    price = zaraContent.find_all(class_="price _product-price")

    item = [i.get_text() for i in item]
    
    for p in range(0, len(item)):
        if "sale" in str(price[p]):
            price[p] = float(str(price[p]).split('sale" data-price="')[-1].split(" ")[0]) 
        else:
            price[p] = float(str(price[p]).split('main-price" data-price="')[-1].split(" ")[0])

    table = pd.DataFrame(
    {
        'Item' : item,
        'Price' : price,
        }
        )   
#-------------------------------Filtering-------------------------------------  
    print("Filter results by price?\n 1.Yes\n 2.No")
    answer = input()
    if answer == "1":
        print("Max price?")
        answer = input()
        table = table[table['Price'] < float(answer)]

#-----------------------------------Email------------------------------------- 
print("Enter your email\n")
email_receive = input()
print("Sending file to email....")
email_send = 'rtesting708@gmail.com'
#password = getpass.getpass()
password = "Poohbear1!"

subject = "Zara Items"
msg = MIMEMultipart()
msg['From'] = email_send
msg['To'] = email_receive
msg['Subject'] = subject

body = "Here are the zara items you were looking at."
msg.attach(MIMEText(body, 'plain'))

filename = 'zara.csv'
tableFile = table.to_csv(filename, index=False)

attachment = open(filename, 'rb')
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header(
    "Content-Disposition",
    "attachment; filename= zara.csv",
)
msg.attach(part)
text = msg.as_string()

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(email_send, password)
server.sendmail(email_send, email_receive, text)
server.close()

    