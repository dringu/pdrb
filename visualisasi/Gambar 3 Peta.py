import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.patches as mpatches

file_path_pdrb = r'D:\git\pdrb\data\PDRB ADHB Kabupaten_Kota.xlsx'
df_pdrb = pd.read_excel(file_path_pdrb, skiprows=1)
df_pdrb.columns = ["Kabupaten/Kota", 2022, 2023, 2024]
df_pdrb = df_pdrb.dropna(subset=["Kabupaten/Kota"])

df_pdrb_2024 = df_pdrb[["Kabupaten/Kota", 2024]].copy()
df_pdrb_2024.columns = ["Kabupaten/Kota", "PDRB_2024"]

file_path_geojson = r'E:\Project\GH\batas\geojson\jatim.geojson'
gdf = gpd.read_file(file_path_geojson)

def normalize_name(name):
    name = str(name)
    if "Kabupaten" in name:
        return "Kabupaten " + name.replace("Kabupaten ", "").strip().title()
    elif "Kota" in name:
        return "Kota " + name.replace("Kota ", "").strip().title()
    else:
        return name.strip().title()

gdf["Nama_Normalized"] = gdf["Nama_Normalized"].apply(normalize_name)
df_pdrb_2024["Nama_Normalized"] = df_pdrb_2024["Kabupaten/Kota"].apply(normalize_name)

gdf = gdf.merge(df_pdrb_2024, on="Nama_Normalized", how="left")

plt.style.use('default')
fig, ax = plt.subplots(1, 1, figsize=(14, 12), facecolor='#f5f5f5')

xmin, ymin, xmax, ymax = 110.5, -8.9, 115.5, -6.7
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

colors = ['#f0f9e8', '#bae4bc', '#7bccc4', '#43a2ca', '#0868ac']
cmap = LinearSegmentedColormap.from_list('gradient_improved', colors)

gdf.plot(
    column="PDRB_2024",
    cmap=cmap,
    linewidth=0.8,
    edgecolor='#555555',
    ax=ax,
    legend=False,
    missing_kwds={'color': '#f5f5f5', 'edgecolor': '#aaaaaa', 'hatch': '...'}
)

cities_to_annotate = {
    "Surabaya": {"offset": (10, -15)},
    "Probolinggo": {"offset": (10, 5)},
    "Tuban": {"offset": (-15, 5)},
    "Malang": {"offset": (5, 10)},
    "Banyuwangi": {"offset": (15, 0)},
    "Situbondo": {"offset": (5, -10)},
    "Jember": {"offset": (0, 15)},
    "Lumajang": {"offset": (-15, 0)},
    "Pasuruan": {"offset": (10, -5)},
    "Gresik": {"offset": (-10, -10)},
    "Sumenep": {"offset": (-15, 15)},
    "Sampang": {"offset": (0, 10)},
    "Madiun": {"offset": (0, -15)},
    "Mojokerto": {"offset": (-5, 10)},
    "Kediri": {"offset": (10, 10)},
    "Pacitan": {"offset": (-10, -5)},
    "Ngawi": {"offset": (10, 0)},
    "Tulungagung": {"offset": (0, -12)}
}

for city, settings in cities_to_annotate.items():
    if city in gdf["Nama_Normalized"].values:
        row = gdf[gdf["Nama_Normalized"] == city].iloc[0]
        x, y = row.geometry.centroid.x, row.geometry.centroid.y
        ax.annotate(
            text=f"{city}\n{row['PDRB_2024']/1000:,.1f}T",
            xy=(x, y),
            xytext=settings["offset"],
            textcoords="offset points",
            ha='center',
            fontsize=9,
            fontweight='bold',
            color='black',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=0.2)
        )
        ax.plot(x, y, 'o', color='red', markersize=5, alpha=0.7)

divider = make_axes_locatable(ax)
cax = divider.append_axes("bottom", size="5%", pad=0.5)
sm = ScalarMappable(norm=Normalize(vmin=gdf["PDRB_2024"].min(), vmax=gdf["PDRB_2024"].max()), cmap=cmap)
cbar = fig.colorbar(sm, cax=cax, orientation='horizontal')
cbar.set_label('PDRB (Miliar Rupiah)', fontsize=9)
cbar.ax.tick_params(labelsize=8)

ax.plot([xmin+0.5, xmin+1.0], [ymin+0.3, ymin+0.3], color='black', linewidth=1.5)
ax.text(xmin+0.75, ymin+0.28, '50 km', ha='center', va='top', fontsize=8, 
       bbox=dict(facecolor='white', alpha=0.7, pad=0.1))

ax.plot(xmax-0.3, ymax-0.2, marker='^', color='black', markersize=10)
ax.text(xmax-0.3, ymax-0.25, 'Utara', ha='center', va='top', fontsize=8)

plt.figtext(0.15, 0.02, "Sumber: BPS Jawa Timur | Data diolah", 
            fontsize=8, color='#555555', bbox=dict(facecolor='white', alpha=0.7, pad=0.1))

ax.set_axis_off()
plt.tight_layout()
#plt.savefig("Peta_PDRB_ADHB.png", dpi=300, bbox_inches='tight')
plt.show()