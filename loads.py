import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.style.use('fivethirtyeight')
plt.rcParams['axes.facecolor'] = 'white'

import requests
import warnings
warnings.filterwarnings('ignore')


NLnodes = ['PHSISILON2-10','PHSISILON2-11','PHSISILON2-12','PHSISILON2-13','PHSISILON2-14']
Xnodes_4gen = ['PHSISILON2-1','PHSISILON2-2','PHSISILON2-3','PHSISILON2-4','PHSISILON2-7'
               ,'PHSISILON2-8','PHSISILON2-9']
Xnodes_5gen = ['PHSISILON2-15','PHSISILON2-16','PHSISILON2-17']


file = open('\\\\cifs2\\ifs\\data\\Isilon_Support\\scripts\\scripts_output\\loads.txt','r')
file = file.read()
a = file.rstrip().replace(",","").replace(" hrs","").replace(" hr","").replace(" mins","").replace(" min","").replace(" secs","").replace(" sec","").split("\n")


aux = []
for row in a:
    aux.append((' '.join(row.split())).split(' '))

loads = pd.DataFrame(aux)

file = open('\\\\cifs2\\ifs\\data\\Isilon_Support\\scripts\\scripts_output\\loads_dates.txt','r')
file = file.read()
a = file.rstrip().split("\n")
aux=[]
numbernodes = 17
for i in a:
    for j in range(numbernodes):
        aux.append(i)


loads = loads[[0,1,10,11,12]]
loads = loads.rename(columns={0:'Node',1:'time',10:'1min',11:'5min',12:'15min'})
loads["date"] = aux
loads['1min'] = pd.to_numeric(loads['1min'], errors='raise', downcast='integer')
loads['5min'] = pd.to_numeric(loads['5min'], errors='raise', downcast='integer')
loads['15min'] = pd.to_numeric(loads['15min'], errors='raise', downcast='integer')


loads.date = pd.to_datetime(loads.date)
loads['Node'] = loads['Node'].map(lambda x: x.replace(":",""))

loads['hour']=loads['date'].dt.hour
loads['minute']=loads['date'].dt.minute
loads['time'] = str(loads['hour']) + ':' + str(loads['minute'])

# select 24 hours
loads24 = loads.iloc[-1649:]

loadsNL = loads[loads.Node.isin(NLnodes)][["Node","1min","5min","15min","date"]]

loadsNLscale = loadsNL
loadsNLscale["1min"] = loadsNLscale["1min"] / 4
loadsNLscale["5min"] = loadsNLscale["5min"] / 4
loadsNLscale["15min"] = loadsNLscale["15min"] / 4

loadsX4 = loads[loads.Node.isin(Xnodes_4gen)][["Node","1min","5min","15min","date"]]

loadsX4scale = loadsX4
loadsX4scale["1min"] = loadsX4scale["1min"] / 12
loadsX4scale["5min"] = loadsX4scale["5min"] / 12
loadsX4scale["15min"] = loadsX4scale["15min"] / 12

loadsX5 = loads[loads.Node.isin(Xnodes_5gen)][["Node","1min","5min","15min","date"]]

loadsX5scale = loadsX5
loadsX5scale["1min"] = loadsX5scale["1min"] / 16
loadsX5scale["5min"] = loadsX5scale["5min"] / 16
loadsX5scale["15min"] = loadsX5scale["15min"] / 16


# cumulative
import matplotlib.dates as mdates


fig =  plt.figure(figsize=(14,13),facecolor='white')

ax1=plt.subplot2grid((3,1), (0,0))
plt.title("IsilonGP2 [X gen4 nodes] - LOADS Cumulative [SCALED]",
          size=16,
          fontweight = 'bold')

for xnode in Xnodes_4gen:
    aux = loadsX4scale[loadsX4scale["Node"] == xnode]
    v = ax1.plot(aux['date'],aux["15min"],linewidth=1, alpha=0.9)
    
ax1.axhline(y=1,c="orange",linewidth=2,zorder=1) 
ax1.axhline(y=1.2,c="red",linewidth=2,zorder=1)  

xfmt = mdates.DateFormatter('%m/%d')
ax1.xaxis.set_major_formatter(xfmt)

xticks = ax1.xaxis.get_major_ticks()
xticks[-1].label1.set_visible(False)

plt.legend(Xnodes_4gen,
           prop={'size':12},
           loc=0, 
           ncol=3
          )   
plt.ylim([0,1.75])

ax2=plt.subplot2grid((3,1), (1,0))
plt.title("\n\nIsilonGP2 [X gen5 nodes] - LOADS Cumulative [SCALED]",
          size=16,
          fontweight = 'bold')
for xnode in Xnodes_5gen:
    aux = loadsX5scale[loadsX5scale["Node"] == xnode]
    v = ax2.plot(aux['date'],aux["15min"],linewidth=1, alpha=0.9)
    
ax2.axhline(y=1,c="orange",linewidth=2,zorder=1) 
ax2.axhline(y=1.2,c="red",linewidth=2,zorder=1)  

xticks = ax2.xaxis.get_major_ticks()
xticks[-1].label1.set_visible(False)

xfmt = mdates.DateFormatter('%m/%d')
ax2.xaxis.set_major_formatter(xfmt)
    
plt.legend(Xnodes_5gen,
           prop={'size':12},
           loc=0, 
           ncol=3
          )
plt.ylim([0,1.75])
   

ax3=plt.subplot2grid((3,1), (2,0))
plt.title("\n\nIsilonGP2 [NL nodes] - LOADS Cumulative [SCALED]",
          size=16,
          fontweight = 'bold')

for nlnode in NLnodes:
    aux = loadsNLscale[loadsNLscale["Node"] == nlnode]
    v = ax3.plot(aux['date'],aux["15min"],linewidth=1, alpha=0.9)

ax3.axhline(y=1,c="orange",linewidth=2,zorder=1) 
ax3.axhline(y=1.2,c="red",linewidth=2,zorder=1) 

xfmt = mdates.DateFormatter('%m/%d')
ax3.xaxis.set_major_formatter(xfmt)

xticks = ax3.xaxis.get_major_ticks()
xticks[-1].label1.set_visible(False)

plt.legend(NLnodes,
           prop={'size':12},
           loc=0, 
           ncol=3
          )
plt.ylim([0,1.75])

plt.savefig('GP2_loads_cumulative.png', facecolor=fig.get_facecolor(), transparent=True, bbox_inches='tight',)

#24 hours
loadsNL = loads24[loads24.Node.isin(NLnodes)][["Node","1min","5min","15min","date"]]

loadsNLscale = loadsNL
loadsNLscale["1min"] = loadsNLscale["1min"] / 4
loadsNLscale["5min"] = loadsNLscale["5min"] / 4
loadsNLscale["15min"] = loadsNLscale["15min"] / 4

loadsX4 = loads24[loads24.Node.isin(Xnodes_4gen)][["Node","1min","5min","15min","date"]]

loadsX4scale = loadsX4
loadsX4scale["1min"] = loadsX4scale["1min"] / 12
loadsX4scale["5min"] = loadsX4scale["5min"] / 12
loadsX4scale["15min"] = loadsX4scale["15min"] / 12

loadsX5 = loads24[loads24.Node.isin(Xnodes_5gen)][["Node","1min","5min","15min","date"]]

loadsX5scale = loadsX5
loadsX5scale["1min"] = loadsX5scale["1min"] / 16
loadsX5scale["5min"] = loadsX5scale["5min"] / 16
loadsX5scale["15min"] = loadsX5scale["15min"] / 16


import matplotlib.dates as mdates


fig =  plt.figure(figsize=(14,13),facecolor='white')

ax1=plt.subplot2grid((3,1), (0,0))
plt.title("IsilonGP2 [X gen4 nodes] - LOADS 24H [SCALED]",
          size=16,
          fontweight = 'bold')

for xnode in Xnodes_4gen:
    aux = loadsX4scale[loadsX4scale["Node"] == xnode]
    v = ax1.plot(aux['date'],aux["15min"],linewidth=1, alpha=0.9)
    
ax1.axhline(y=1,c="orange",linewidth=2,zorder=1) 
ax1.axhline(y=1.2,c="red",linewidth=2,zorder=1)  

xfmt = mdates.DateFormatter('%H:%M')
ax1.xaxis.set_major_formatter(xfmt)

xticks = ax1.xaxis.get_major_ticks()
#xticks[0].label1.set_visible(False)

plt.legend(Xnodes_4gen,
           prop={'size':12},
           loc=0, 
           ncol=3
          )   
plt.ylim([0,1.75])

ax2=plt.subplot2grid((3,1), (1,0))
plt.title("\n\nIsilonGP2 [X gen5 nodes] - LOADS 24H [SCALED]",
          size=16,
          fontweight = 'bold')
for xnode in Xnodes_5gen:
    aux = loadsX5scale[loadsX5scale["Node"] == xnode]
    v = ax2.plot(aux['date'],aux["15min"],linewidth=1, alpha=0.9)
    
ax2.axhline(y=1,c="orange",linewidth=2,zorder=1) 
ax2.axhline(y=1.2,c="red",linewidth=2,zorder=1)  

xfmt = mdates.DateFormatter('%H:%M')
ax2.xaxis.set_major_formatter(xfmt)

xticks = ax2.xaxis.get_major_ticks()
#xticks[0].label1.set_visible(False)
    
plt.legend(Xnodes_5gen,
           prop={'size':12},
           loc=0, 
           ncol=3
          )
plt.ylim([0,1.75])
   

ax3=plt.subplot2grid((3,1), (2,0))
plt.title("\n\nIsilonGP2 [NL nodes] - LOADS 24H [SCALED]",
          size=16,
          fontweight = 'bold')

for nlnode in NLnodes:
    aux = loadsNLscale[loadsNLscale["Node"] == nlnode]
    v = ax3.plot(aux['date'],aux["15min"],linewidth=1, alpha=0.9)

ax3.axhline(y=1,c="orange",linewidth=2,zorder=1) 
ax3.axhline(y=1.2,c="red",linewidth=2,zorder=1) 

xfmt = mdates.DateFormatter('%H:%M')
ax3.xaxis.set_major_formatter(xfmt)

xticks = ax3.xaxis.get_major_ticks()
#xticks[0].label1.set_visible(False)

plt.legend(NLnodes,
           prop={'size':12},
           loc=0, 
           ncol=3
          )
plt.ylim([0,1.75])

plt.savefig('GP2_loads_24h.png', facecolor=fig.get_facecolor(), transparent=True, bbox_inches='tight',)

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

fileToSend1 = "GP2_loads_24h.png"
fileToSend2 = "GP2_loads_cumulative.png"

recipients = ['icarracedo@partners.org','dpackard@partners.org','rhudonjr@partners.org','bemcguinness@partners.org']


msg = MIMEMultipart()
msg["From"] = "IsilonLoadsScript@partners.org"
msg["To"] = ", ".join(recipients)
msg["Subject"] = "GP2 Isilon LOADS"

ctype1, encoding1 = mimetypes.guess_type(fileToSend1)
if ctype1 is None or encoding1 is not None:
    ctype1 = "application/octet-stream"
    
ctype2, encoding2 = mimetypes.guess_type(fileToSend2)
if ctype2 is None or encoding2 is not None:
    ctype2 = "application/octet-stream"
        
maintype1, subtype1 = ctype1.split("/", 1)
maintype2, subtype2 = ctype2.split("/", 1)

fp = open(fileToSend1, "rb")
attachment1 = MIMEImage(fp.read(), _subtype=subtype1)
fp.close()

fp = open(fileToSend2, "rb")
attachment2 = MIMEImage(fp.read(), _subtype=subtype2)
fp.close()

attachment1.add_header("Content-Disposition", "attachment", filename=fileToSend1)
msg.attach(attachment1)
attachment2.add_header("Content-Disposition", "attachment", filename=fileToSend2)
msg.attach(attachment2)

server = smtplib.SMTP("smtp.partners.org")#:587")
server.starttls()
server.sendmail(msg["From"], recipients, msg.as_string())
server.quit()





















