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
m = Basemap(projection='cyl', resolution='l', area_thresh = 100000.0 , llcrnrlon=-84, llcrnrlat=40, urcrnrlon=-74, urcrnrlat=50  )

#lat_0=43.723452,lon_0=-79.431616
# draw coastlines.
m.drawcoastlines()
m.drawcountries()
m.drawstates()
# draw a boundary around the map, fill the background.
# this background will end up being the ocean color, since
# the continents will be drawn on top.
m.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
m.fillcontinents(color='coral',lake_color='aqua')



conn = pypyodbc.connect('DSN=localMSSQL')
cur = conn.cursor()
sql= "select top 100  constituentlookupid,post_code,latitude, longitude from [saeed_cons_spatial] where post_code is not null" 
cur.execute(sql)
dd=cur.fetchall();
df=pd.DataFrame(dd)
lons=df[3].values
lats=df[2].values
x, y = m(lons,lats)


v=np.array( [1.00000  , 0.8954 ,  0.00000 ,  1.0000])

m.plot(x, y,'ro', markersize=3, linestyle='',color=v, alpha=0.5)

# val=np.arange(1,len(x))
# f = val.astype(float)/val.max()
# norm = colors.Normalize(f.min(), f.max())
# col = cm.jet(norm(f))
# for col, xpt, ypt in zip(col, x, y):
#     m.  .text(xpt, ypt, col)
    
plt.show()