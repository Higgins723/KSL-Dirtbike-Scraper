from lxml import html
from smtplib import SMTP
import requests
import smtplib
import string
import time
starttime = time.time()

# get the information from the website
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/58.0.3029.110 Chrome/58.0.3029.110 Safari/537.36"}
url = "https://www.ksl.com/classifieds/search?category[]=Recreational%20Vehicles&subCategory[]=Motorcycles%2C%20Dirt%20Bikes%20Used&keyword=kawasaki%20klx&zip=&marketType[]=Sale&miles=25&hasPhotos[]=&postedTimeFQ[]=&priceFrom=&priceTo=&sellerType[]="

# grab the digits from str
all = string.maketrans('', '')
nodigs = all.translate(all, string.digits)

# starts the connection to gmail server
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()

# loads the from email, to email, and from email password
toandfrom = open('toandfrom.txt', 'r')
username = toandfrom.readline()
password = toandfrom.readline()
phoneAddress = toandfrom.readline()
toandfrom.close()

smtpObj.login(username, password)

while True:
  print "Loading page..."
  page = requests.get(url, headers=headers)
  # grabs the data from the website
  tree = html.fromstring(page.content)
  titles = tree.cssselect("h2.title a.link")
  location = tree.cssselect("span.address")
  price = tree.cssselect("h3.listing-detail-line")
  urls = tree.xpath("//h2/a[contains(@href, 'classifieds/listing/')]//@href")

  if price != '':
      for i in range(len(price)):
        history = open('history.txt', 'r+')
        message = "Title - %s\nLocation - %s\nPrice - %s\nURL - ksl.com%s" % (titles[i].text_content().strip(), location[i].text_content().strip(), price[i].text_content().strip(), urls[i])
        listing_key = urls[i].translate(all, nodigs) + "\n"
        if listing_key in history:
          print "Already sent listing!"
          pass
        else:
          print "Sending new listing!"
          history.write(listing_key)
          smtpObj.sendmail(username, phoneAddress, message)
  history.close()

  time.sleep(60.0 - ((time.time() - starttime) % 60.0))
