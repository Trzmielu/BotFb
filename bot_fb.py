from fbchat import log, Client
from fbchat.models import *
from bs4 import BeautifulSoup
import requests

r = requests.get('http://mpk.wroc.pl/kontrole-biletow',auth=('user', 'pass'))

soup = BeautifulSoup(r.text, 'html.parser')
tabela = soup.tbody

a = []
for tr in soup.find_all('tr'):
    td = tr.find_all('td')
    for element in td:
      a.append(element.get_text())
lista_info = []
for x in a:
  lista_info.append(x.strip())

from datetime import date
today = date.today()
dzien = str(today.day)
miesiac = str(today.month)
if(today.day<10):
  dzien = "0"+str(today.day)
if(today.month<10):
  miesiac = "0"+str(today.month)
data = dzien+"."+miesiac+"."+str(today.year)

komunikat = ""
for i in range(0,len(lista_info)-1):
  if(data==lista_info[i]):
    komunikat = komunikat+"Mo¿liwe kontrole dzisiaj: "+lista_info[i+2]+" ("+lista_info[i+1]+")"
    # print("Mo¿liwe kontrole dzisiaj:",end=" ")
    # print(lista_info[i+2],"(",lista_info[i+1],")")
    y = i
  
del lista_info[y]
del lista_info[y]
del lista_info[y]
print()
komunikat += "\n\nPrzewidywane kontrole w kolejnych dniach:"
# print("Przewidywane kontrole w kolejnych dniach:")
x = 0
for i in range(0,len(lista_info)-1):
    if(i%3==0):
      komunikat += "\n*"+lista_info[i]+": "
      # print("*",lista_info[i],end=": ")
      x = 1
    if(x == 1):
      komunikat += lista_info[i+2]
      # print(lista_info[i+2])
      x = 0
print(komunikat)


class EchoBot(Client):
    def onMessage(self, message_object, author_id, **kwargs):
        self.wyslijWiadomosc("Czesc", author_id)

    def onInbox(self, **kwargs):
        threads = (self.fetchThreadList(thread_location=ThreadLocation.PENDING)
                   + self.fetchThreadList(thread_location=ThreadLocation.OTHER)
                   )

        for node in threads:
            self.moveThreads(ThreadLocation.INBOX, node.uid)
            msgs = self.fetchThreadMessages(thread_id=node.uid, limit=1)
            last_msgs = msgs[0]
            self.wyslijWiadomosc("Czesc", node.uid)

    def wyslijWiadomosc(self, tresc, ident):
        if ident != self.uid:
            self.send(Message(text=tresc), ident)

client = EchoBot("mail", "haslo")
client.listen()
