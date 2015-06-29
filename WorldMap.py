from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

map = Basemap(projection='cyl',     lat_0=0, lon_0=0)

map.drawmapboundary(fill_color='aqua')

map.drawcoastlines()

lons = [-70]
lats = [ 0]

x, y = map(lons, lats)

map.scatter(x, y, marker='D',color='m')
map.fillcontinents(color='coral',lake_color='aqua')
plt.show()