import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

file_path = r'D:\git\pdrb\data\PDRB Harga Konstan 2010 Per Kab Jatim1.xlsx'
df_fixed = pd.read_excel(file_path, skiprows=1)
df_fixed.columns = ["Kabupaten/Kota"] + list(range(2015, 2025))
df_fixed = df_fixed.dropna(subset=["Kabupaten/Kota"])

sns.set(style="whitegrid")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))

def calculate_mean_without_outliers(data):
    return data[~data["Kabupaten/Kota"].isin(["Kota Surabaya", "Sidoarjo"])].iloc[:, 1:].mean()

def create_plot(ax, data, title, highlight_outliers=False, highlight_top_4=False):
    if not highlight_outliers:
        data = data[~data["Kabupaten/Kota"].isin(["Kota Surabaya", "Sidoarjo"])]

    for idx, row in data.iterrows():
        if row["Kabupaten/Kota"] == "Probolinggo":
            ax.plot(row.index[1:], row.values[1:], color='red', linewidth=2.5, label='Probolinggo')
        elif highlight_outliers and row["Kabupaten/Kota"] in ["Kota Surabaya", "Sidoarjo"]:
            ax.plot(row.index[1:], row.values[1:], color='orange', linewidth=2.5, label=row["Kabupaten/Kota"])
        else:
            ax.plot(row.index[1:], row.values[1:], color='grey', alpha=0.5)

    if highlight_outliers:
        mean_values = data.iloc[:, 1:].mean() 
    else:
        mean_values = calculate_mean_without_outliers(data) 
    ax.plot(mean_values.index, mean_values.values, color='blue', linestyle='--', linewidth=2.5, label='Rata-rata')

    if highlight_top_4:
        top_4 = data.set_index("Kabupaten/Kota").mean(axis=1).nlargest(5).index
        for kabupaten in top_4:
            row = data[data["Kabupaten/Kota"] == kabupaten].iloc[0]
            ax.plot(row.index[1:], row.values[1:], linewidth=2.5, label=kabupaten)

    ax.set_title(title, fontsize=16, pad=20)
    ax.tick_params(axis='x', rotation=45)
    ax.legend()

create_plot(ax1, df_fixed, 'Besaran PDRB ADHK Kabupaten/Kota Per Tahun\n(2015 - 2024)', highlight_outliers=True)
create_plot(ax2, df_fixed, 'Besaran PDRB ADHK Kabupaten/Kota Per Tahun (tanpa Surabaya dan Sidoarjo)\n(2015 - 2024)', highlight_top_4=True)

plt.tight_layout()
plt.show()
plt.savefig('PDRB_Probolinggo_Tetangga_Trend.png', dpi=300, bbox_inches='tight')