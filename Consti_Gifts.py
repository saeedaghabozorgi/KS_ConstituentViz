# to visualize a constituent behaviour in terms of actions, intractions, BU

import pypyodbc
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


conn = pypyodbc.connect('DSN=localMSSQL')
cur = conn.cursor()
consid='70434'
sql= "select * from saeed_Const_Transac_Interaction_BU_Appeal_states where constituentlookupid='%s'" % consid
cur.execute(sql)
x=cur.fetchall();
df=pd.DataFrame(x)
sql= "select * from [saeed_const_transac_payment_states] where revenuetransactiontypecode=0 and CONSTITUENTLOOKUPID='%s' order by seq" % consid
cur.execute(sql)
y=cur.fetchall();
df2=pd.DataFrame(y)

cur.close()
conn.close()

fig = plt.figure()
col=np.array(['r','c','m','g'])
df['act_int'] = np.nan
df.loc[df[3] == 'inactive', 'act_int'] = 0
df.loc[df[3] == 'Donation', 'act_int'] = 1
df.loc[df[3] == 'Recurring gift', 'act_int'] = 2
df.loc[df[3] == 'Pledge', 'act_int'] = 3
df.loc[df[3] == 'Planned gift', 'act_int'] = 4

dintr=df[(df.loc[:,3] == 'Email') | (df.loc[:,3] == 'In Person')| (df.loc[:,3] == 'Mail')| (df.loc[:,3] == 'Phone')]
dgift=df[(df.loc[:,3] == 'Donation') | (df.loc[:,3] == 'Recurring gift')| (df.loc[:,3] == 'Pledge') | (df.loc[:,3] == 'Planned gift') | (df.loc[:,3] == 'inactive')]




groups_int = dintr.groupby(df[3])
groups_gif = dgift.groupby(df[3])
groups_BU = dgift.groupby(df[4])

df2['act_int'] = np.nan
df2.loc[df2[3] == 'RG_Payment', 'act_int'] = 1.5
df2.loc[df2[3] == 'Pledge_Payment', 'act_int'] = 2.5
dpay=df2[(df2.loc[:,3] == 'Pledge_Payment') | (df2.loc[:,3] == 'RG_Payment')]
groups_pay = dpay.groupby(df2[3])

#---------------------------------------------------------------------
## the top axes
# ax1 = fig.add_subplot(3,1,1)
# ax1.set_ylabel('rank')
# ax1.set_title('Constituent Transaction-Interaction')


# for name, group in groups_int:
#     ax1.plot_date(group[1], group[0], marker='*', linestyle='', ms=7, label=name)
#         
# for name, group in groups_gif:
#     ax1.plot_date(group[1], group[0], marker='o', linestyle='', ms=7, label=name)
        
# ax1.legend(loc=4)
# ax1.autoscale_view()
# ax1.grid(True)

#---------------------------------------------------------------------

## the button axes
ax2 = fig.add_subplot(311)
ax2.set_title('Constituent Transaction-Interaction %s' % consid )
ax2.set_ylabel('Actions')

i=0; 
for name, group in groups_int:
    a=[7+i*0.1]*group[0].count()
    ax2.plot_date(group[2], a, marker='|', linestyle='', ms=7, label=name)
    i=i+1
i=0;    
for name, group in groups_BU:
    b=[6+i*0.1]*group[2].count()
    rects=ax2.plot_date(group[2], b, marker='*', linestyle='', ms=7, label=name, markeredgewidth = 0) 
    i=i+1
     
i=0;        
for name, group in groups_gif:
    ax2.plot_date(group[2], group['act_int'], marker='o', linestyle='', ms=7, label=name, color=col[i])
    i=i+1

for name, group in groups_pay:
    rects=ax2.plot_date(group[1], group['act_int'], marker='o', linestyle='', ms=3, label=name,markeredgecolor=None) 

ax2.legend(loc=3)

ax2.set_yticks((0,1,2,3,4,6,7))
labels = ax2.set_yticklabels(('inactive','donation', 'rec gift', 'pledge', 'planned gift','BU','interaction'))
#ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# ax.annotate('angle', xy=(50, 50),  xycoords='data', 
#      xytext=(-50, 30), textcoords='offset points',
#      arrowprops=dict(arrowstyle="->", connectionstyle="angle,angleA=0,angleB=90,rad=10"),)
ax2.set_ylim([-1,8])
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
#ax2.autoscale_view()
ax2.grid(True)


#---------------------------------------------------------------------
ax4 = fig.add_subplot(312, sharex=ax2)
ax4.set_ylabel('Payment') 
groups_payment = df2.groupby(df2[3])
i=0;

for name, group in groups_payment:
    #ax4.plot_date(group[1], group[4],  linestyle='-', ms=2, label=name)
    rects=ax4.bar(group[1], group[4], label=name,width=25, color=col[i], alpha=.5, edgecolor = None)
    i=i+1
    # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         ax4.text(rect.get_x(), 1.05*float(height), '%dk'%int(height/1000), ha='center', va='bottom')  
ax4.xaxis_date()
ax4.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
#ax4.autoscale_view()
ax4.grid(True)
#---------------------------------------------------------------------

ax3 = fig.add_subplot(313,sharex=ax2)
ax3.set_ylabel('Accumulative revenue')
df2['acum_amount'] = np.cumsum(df2[4])
ax3.plot_date(df2[1], df2['acum_amount'],  linestyle='-', marker='')

i=0
for name, group in groups_gif:
    ax3.plot_date(group[2], group[6], marker='o', linestyle='', ms=7, color=col[i],label=name)
    i=i+1
ax3.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
#ax3.autoscale_view()
ax3.grid(True)

fig.subplots_adjust(hspace=.5)

plt.show()


