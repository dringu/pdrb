import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

file_path = r'D:\git\pdrb\data\PDRB Harga Konstan 2010 Per Kab Jatim1.xlsx'

df_fixed = pd.read_excel(file_path, skiprows=1)
df_fixed.columns = ["Kabupaten/Kota"] + list(range(2015, 2025))
df_fixed = df_fixed.dropna(subset=["Kabupaten/Kota"])
df_fixed['Pertumbuhan'] = ((df_fixed[2024] - df_fixed[2015]) / df_fixed[2015]) * 100
df_pertumbuhan = df_fixed.sort_values(by='Pertumbuhan', ascending=False)
df_pertumbuhan_tahunan = pd.DataFrame({'Kabupaten/Kota': df_fixed['Kabupaten/Kota']})

year_cols = list(range(2016, 2025))
for year in year_cols:
    prev_year = year - 1
    df_pertumbuhan_tahunan[year] = ((df_fixed[year] - df_fixed[prev_year]) / df_fixed[prev_year]) * 100

df_pertumbuhan_tahunan['Avg_Growth'] = df_pertumbuhan_tahunan[year_cols].mean(axis=1)
mean_growth_by_year = {}
std_growth_by_year = {}

for year in year_cols:
    mean_growth_by_year[year] = df_pertumbuhan_tahunan[year].mean()
    std_growth_by_year[year] = df_pertumbuhan_tahunan[year].std()

outlier_kabupaten = []
for idx, row in df_pertumbuhan_tahunan.iterrows():
    kabupaten = row['Kabupaten/Kota']
    is_outlier = False
    
    for year in year_cols:
        growth = row[year]
        if (growth > (mean_growth_by_year[year] + 2 * std_growth_by_year[year]) or 
            growth < (mean_growth_by_year[year] - 2 * std_growth_by_year[year])):
            is_outlier = True
            break
    
    if is_outlier and kabupaten not in outlier_kabupaten:
        outlier_kabupaten.append(kabupaten)

plt.figure(figsize=(14, 7))
for idx, row in df_pertumbuhan_tahunan.iterrows():
    kabupaten = row['Kabupaten/Kota']
    if kabupaten == 'Probolinggo':
        plt.plot(year_cols, row[year_cols], color='blue', linewidth=2.5, label='Probolinggo')
    else:
        plt.plot(year_cols, row[year_cols], color='gray', alpha=0.3)

# Plot rata-rata Jawa Timur
mean_values = [mean_growth_by_year[year] for year in year_cols]
plt.plot(year_cols, mean_values, color='red', linestyle='--', linewidth=2.5, label='Rata-rata Jawa Timur')

# anotasi untuk outlier
for idx, row in df_pertumbuhan_tahunan.iterrows():
    kabupaten = row['Kabupaten/Kota']
    if kabupaten in outlier_kabupaten:
        for year in year_cols:
            growth = row[year]
            if (growth > (mean_growth_by_year[year] + 2 * std_growth_by_year[year]) or 
                growth < (mean_growth_by_year[year] - 2 * std_growth_by_year[year])):
                plt.text(year, growth, kabupaten, fontsize=9, color='black', ha='center', va='bottom')

plt.title("Pertumbuhan Tahunan PDRB Kabupaten/Kota di Jawa Timur (2016-2024)", 
          fontsize=14, fontweight='bold')
plt.ylabel("Pertumbuhan Tahunan (%)", fontsize=12)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("tren_pertumbuhan_jatim.png", dpi=300, bbox_inches='tight')