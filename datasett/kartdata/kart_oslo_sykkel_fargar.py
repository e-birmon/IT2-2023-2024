import osmnx as ox
import folium as fol
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# Les inn data
df = pd.read_csv('sykkel.csv')

# Definer størrelsen på rutenettet
bins_lat = np.arange(df['end_station_latitude'].min(), df['end_station_latitude'].max(), 0.005) # 0.005 grader er ca 500 meter 
bins_lon = np.arange(df['end_station_longitude'].min(), df['end_station_longitude'].max(), 0.005)

# Grupper punktene i bokser
df['latbin'] = pd.cut(df['end_station_latitude'], bins=bins_lat)
df['lonbin'] = pd.cut(df['end_station_longitude'], bins=bins_lon)
binned = df.groupby(['latbin', 'lonbin']).size().reset_index(name='count')
print(binned)

# Normaliser fargene til antall punkter
norm = colors.Normalize(binned['count'].min(), binned['count'].max())

# Lager et kart
m = fol.Map([59.911491, 10.757933], zoom_start=12) # Midtpunkt Oslo, og godt zooma ut

# Velger fargekart
cmap = plt.cm.viridis

# Legger til boksene
for _, row in binned.iterrows():
    # Beregn midtpunktet av boksen for å plassere sirkelen
    lat = (row['latbin'].left + row['latbin'].right) / 2
    lon = (row['lonbin'].left + row['lonbin'].right) / 2
    # Bruk antall punkter i boksen til å bestemme radiusen av sirkelen
    # radius = row['count'] / 10
    radius = np.sqrt(row['count'])
    # Use the number of points in the bin to determine the color of the circle
    color = cmap(norm(row['count']))
    # Konverterer RGBA-fargar til HEX for bruk i folium
    color = colors.to_hex(color)
    fol.CircleMarker([lat, lon], radius=radius, color=color).add_to(m)

# Lagrer kartet
# m.save("oslo_sykkel_binning_fargar.html")