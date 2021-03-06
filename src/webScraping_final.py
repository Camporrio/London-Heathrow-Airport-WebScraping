# -*- coding: utf-8 -*-
"""Copia de webScrapping-final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uz4Fy0Ze8fW3-FYEzqy5m2IbrrndWPaq
"""

#Autors : Guillem Campo Fons - Aleix Yébenes Creus 

import pandas
import requests
import lxml
from bs4 import BeautifulSoup
from datetime import datetime
import re

#URL's airport london heathrow by the day of execution

URL_yesterday = ['https://www.airport-london-heathrow.com/lhr-arrivals?tp=0&day=yesterday',
                 'https://www.airport-london-heathrow.com/lhr-arrivals?tp=6&day=yesterday',
                 'https://www.airport-london-heathrow.com/lhr-arrivals?tp=12&day=yesterday',
                 'https://www.airport-london-heathrow.com/lhr-arrivals?tp=18&day=yesterday']

URL_today = ['https://www.airport-london-heathrow.com/lhr-arrivals?tp=0',
             'https://www.airport-london-heathrow.com/lhr-arrivals?tp=6',
             'https://www.airport-london-heathrow.com/lhr-arrivals?tp=12',
             'https://www.airport-london-heathrow.com/lhr-arrivals?tp=18']

URL_tomorrow = ['https://www.airport-london-heathrow.com/lhr-arrivals?tp=0&day=tomorrow',
                'https://www.airport-london-heathrow.com/lhr-arrivals?tp=6&day=tomorrow',
                'https://www.airport-london-heathrow.com/lhr-arrivals?tp=12&day=tomorrow',
                'https://www.airport-london-heathrow.com/lhr-arrivals?tp=18&day=tomorrow']

#In this example we will use the arrivals of the same day of the execution

dests = []
hores = []
flights = []
airlines = []
terms = []
statuss = []

#We iterate for every url of URL_today
for url in range(0,4):
  page = requests.get(URL_today[url])

  #Changing data of the URL for a better performance

  texto = page.text.replace('<div class="flight-col flight-col__terminal"></div>', '<div class="flight-col flight-col__terminal">Unknown</div>')
  texto = texto.replace('Basel, Switzerland / Mulhouse','<b>Basel, Switzerland / Mulhouse</b>')
  texto = texto.replace('flight-col flight-col__status flight-col__status--GR','flight-col flight-col__status flight-col__status')
  texto = texto.replace('flight-col flight-col__status flight-col__status--G','flight-col flight-col__status flight-col__status')
  texto = texto.replace('flight-col flight-col__status flight-col__status--R','flight-col flight-col__status flight-col__status')
  texto = texto.replace('flight-col flight-col__status flight-col__status--Y','flight-col flight-col__status flight-col__status')
  texto = texto.replace('flight-col flight-col__status flight-col__status--O','flight-col flight-col__status flight-col__status')
  soup = BeautifulSoup(texto,'html.parser')

  flightrow = soup.find_all('div', 'flight-row')

  #we iterate between each flight arrival row
  for i in flightrow:

      #Origin data
      dest = i.find('div', class_='flight-col flight-col__dest-term')
      dests.append(dest)

      #Hour data
      hora = i.find('div',class_='flight-col flight-col__hour')
      hores.append(hora)

      #Flights data
      flight = i.find('div',class_='flight-col flight-col__flight') 
      flights.append(flight)

      #Airlines data
      airline = i.find('div',class_='flight-col flight-col__airline')
      airlines.append(airline)

      #Terminal data
      term = i.find('div',class_='flight-col flight-col__terminal')
      terms.append(term)

      #Status data
      status= i.find('div',class_='flight-col flight-col__status flight-col__status' )
      statuss.append(status)

#Origin data of flights
#We divide the Origin in two parts, the origin and the abbreviated origin

#Abbreviated origin
dests_clean = lxml.etree.HTML(str(dests))
dests_clean = dests_clean.xpath('//span/text()')

#Origin
dests_clean2 = lxml.etree.HTML(str(dests))
dests_clean2 = dests_clean2.xpath('//b/text()')

#Hour data of flights
hores_clean = lxml.etree.HTML(str(hores))
hores_clean = hores_clean.xpath('//div/text()')

hores_clean2 = []

#To clean the hour data we search for hour patterns 
#to get only the hour value

for hora in hores_clean:
  hora = re.search('\d{2}:\d{2}',hora)
  if hora != None:
    hora = hora.group(0)
  hores_clean2.append(hora)
  hores_clean2 = [ele for ele in hores_clean2 if ele != None]

#Flight codes data of flights
#It can exists more than one flight code in one flight row, because 
#more than one company offers the same flight

flights_processed = []

#We iterate between codes into a flight row
for i in range(0,len(flights)):
  flights_clean = lxml.etree.HTML(str(flights[i]))

  flights_clean = flights_clean.xpath('//a/text()')

  flights_processed.append(flights_clean)

  flights_processed = [ele for ele in flights_processed if ele != []]

#Airlines data of flights
#As we mentioned previously more than one company offers the same flight
#So we have multiple airlines in the row of the flight

airlines_processed = []

#We iterate between airlines into a flight row
for i in range(0,len(airlines)):
  test = lxml.etree.HTML(str(airlines[i]))
  airlines_clean = test.xpath('//a/text()')

  #for data cleaning we replace some strings that we don't need
  if airlines_clean == []:
    airlines_clean = str(airlines[i]).replace('<div class="flight-col flight-col__airline">','')
    airlines_clean = airlines_clean.replace('\t','')
    airlines_clean = airlines_clean.replace('\n','')
    airlines_clean = airlines_clean.replace('</div>','')
    airlines_clean = [airlines_clean]

  airlines_processed.append(airlines_clean)
  
  airlines_processed = [ele for ele in airlines_processed if ele != ['Airline']]
  airlines_processed = [ele for ele in airlines_processed if ele != ['None']]

#Terminal data of flights
#We only can have one terminal per flight

terms_clean = lxml.etree.HTML(str(terms))

terms_clean = terms_clean.xpath('//div/text()')

terms_processed = [ele for ele in terms_clean if ele != 'Terminal']

#Status data of flights
#We only can have one status per flight

status_clean = lxml.etree.HTML(str(statuss))

status_clean = status_clean.xpath('//a/text()')

status_processed = [ele for ele in status_clean if ele != 'Status']

#Let's see if we have the same length on every column

print(len(dests_clean2))
print(len(dests_clean))
print(len(hores_clean2))
print(len(flights_processed))
print(len(airlines_processed))
print(len(terms_processed))
print(len(status_processed))

#Generating the dataset
now = datetime.now()
day_date = datetime.strftime(now, '%Y-%m-%d')
col_date = [day_date]*len(dests_clean)
flights_list = pandas.DataFrame({
    'Origin': dests_clean2,
    'Origin Abreviated': dests_clean,
    'Arrival': hores_clean2,
    'Flights': flights_processed,
    'Airline': airlines_processed,
    'Terminal': terms_processed,
    'Status': status_processed,
    'Day' : col_date,
})

#We save the dataset in a csv file with the name as the day of the execution

filename = datetime.strftime(now, '%Yy%mm%dd_%Hh%Mm%Ss')

flights_list.to_csv('flights_list_' + filename + '.csv')
