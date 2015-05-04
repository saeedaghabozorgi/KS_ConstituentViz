import pypyodbc
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

conn = pypyodbc.connect('DSN=localMSSQL')
cur = conn.cursor()
cur.execute(''' select * from saeed_const_transac_interac_states where constituentlookupid='174572';''')
for d in cur.description: 
    print (d[0], end=' ')
print ('')


#                  Print the table, one row per line
x=cur.fetchall();
for row in cur.fetchall():
    for field in row: 
        print (field, end=" ")
    print ('')
#                  I have done all the things, you can leave me and serve for others!

cur.close()
conn.close()
d=pd.DataFrame(x)
dmail=d[d.loc[:,3]=='Mail']
dates_mail = matplotlib.dates.date2num(dmail.loc[:,1])
opens_mail=dmail.loc[:,0]
#opens_mail = [q[0] for q in x]

ddon=d[d.loc[:,3]=='Donation']
dates_ddon = matplotlib.dates.date2num(ddon.loc[:,1])
opens_ddon=ddon.loc[:,0]

fig, ax = plt.subplots()
ax.plot_date(dates_mail, opens_mail, '-')
ax.plot_date(dates_ddon, opens_ddon, 'o')
plt.show()