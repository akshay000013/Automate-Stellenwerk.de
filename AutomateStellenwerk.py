#! python3 

# Standard Library imports
from datetime import date

# Third party imports
import bs4, requests, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


getPage = requests.get('https://www.stellenwerk-darmstadt.de/') # returns the page
getPage.raise_for_status() # if error it will stop the program

list = bs4.BeautifulSoup(getPage.text, 'html.parser') # Parse text for jobs

today = date.today() # today's date
d1 = today.strftime("%d.%m.%Y") # assigns today's date in the required format to d1
the_one = d1 # checks if a posting with today's date has been added
flength = len(the_one)
available = False # is set to true if the_one is found anywhere

same = 0
count=0 # counter to determine how many new listings are available
myList = [] # a list to  save the text from scraped content
allListings = list.find_all("li",{"class": "SearchList-item"}) # returns all the listings

# create the file beforehand and then read the file and store the content into data
with open('testfile.txt') as file:  
    data = file.read() 

# goess through all the listings and appends to a list and saves into a file only if the searched listing matches today's date and if it does not exist in the file
for todaysListing in allListings:
    for i in range(len(todaysListing.text)):
        chunk = todaysListing.text[i:i+flength].lower()
        if chunk == the_one:
            if data.find("https://www.stellenwerk-darmstadt.de"+todaysListing.find('a')['href']) != -1:
                same = same + 1
            else:
                available = True
                myList.append(str(todaysListing.text.strip())) # appends the text content to list
                myList.append("https://www.stellenwerk-darmstadt.de"+todaysListing.find('a')['href'])
                count+=1 # counter increments by 1
                with open('testfile.txt', 'a') as file: 
                    file.write(str(myList))
  
if same >= 0:
    print("No. of same listings - "+str(same))
				
consoleList = [x.replace('\n', '') for x in myList]            
print(count, "New Listings\n")
print(*consoleList, sep = "\n\n")
count = str(count)
#text = count

# Email initialisation
sender = "example@gmail.com"
reciever = "example@gmail.com"
subject = 'Attention! New Listings - '+count

message = MIMEMultipart('')
message['Subject'] = subject
message['From'] = sender
message['To'] = reciever

# elements from the list into rows
html = """\
<html>
  <body>
    <table>
      <tbody>
        {}
      </tbody>
    </table>
  </body>
</html>
"""

rows = ""
for article in myList:
    rows = rows + "<tr><td>"+str(article)+"<td></tr>"
html = html.format(rows)

#part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

#message.attach(part1)
message.attach(part2)

# sends an email if available is true
if available == True:
    conn = smtplib.SMTP('smtp.gmail.com', 587) # smtp address and port
    conn.ehlo() # call this to start the connection
    conn.starttls() # starts tls encryption. When we send our password it will be encrypted.
    conn.login('example@gmail.com', 'pass')
    conn.sendmail(sender, reciever, message.as_string())
    conn.quit()
    print('\nSent notificaton e-mails for the following recipients:')
    #for i in range(len(toAddress)):
    print(reciever)
    #print('')
else:
    print('No new listing is available for now.')
