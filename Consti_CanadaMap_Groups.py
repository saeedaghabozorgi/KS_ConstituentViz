from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pypyodbc
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as colors
import matplotlib.cm as cm

# setup Lambert Conformal basemap.
#m = Basemap(projection='cyl', resolution='l', area_thresh = 100000.0 , llcrnrlon=-84, llcrnrlat=40, urcrnrlon=-74, urcrnrlat=50  )
m = Basemap(projection='cyl', resolution='l', area_thresh = 10000.0 , llcrnrlon=-81, llcrnrlat=40, urcrnrlon=-77, urcrnrlat=50  )

#lat_0=43.723452,lon_0=-79.431616
# draw coastlines.
# draw the coastlines of continental area
m.drawcoastlines()
# draw country boundaries
m.drawcountries(linewidth=2)
# draw states boundaries (America only)
m.drawstates()
#m.drawmapboundary(fill_color='aqua')
#m.fillcontinents(color='coral',lake_color='aqua')
parallels = np.arange(0., 90, 10.)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
meridians = np.arange(180.,360.,10.)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)




# display blue marble image (from NASA) as map background
#m.bluemarble()




conn = pypyodbc.connect('DSN=localMSSQL')
cur = conn.cursor()
sql= "select top 10000 constituentlookupid,post_code,latitude, longitude,gender from [saeed_cons_spatial] where post_code is not null" 
cur.execute(sql)
dd=cur.fetchall();
df=pd.DataFrame(dd)


colors = list("rgb")
groups_gend = df.groupby(df[4])
for name, group in groups_gend:
    lons=group[3].values
    lats=group[2].values
    gend=group[4].values
    x, y = m(lons,lats)
    m.scatter(x.tolist(), y.tolist(), color=colors.pop(), alpha=0.05,linewidth='0', label=name)
plt.legend()
plt.show()