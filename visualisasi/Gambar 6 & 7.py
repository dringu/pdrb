import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap

plt.rcParams['font.weight'] = 'normal'
plt.rcParams['axes.titleweight'] = 'bold'

probolinggo_data = {
    'Lapangan Usaha': [
        'Pertanian, Kehutanan, dan Perikanan',
        'Pertambangan',
        'Industri Pengolahan/Manufaktur',
        'Pengadaan Listrik dan Gas',
        'Penyedian Air dan Pengelolaan Sampah',
        'Konstruksi',
        'Perdagangan & Retail',
        'Transportasi dan Pergudangan',
        'Penyediaan Akomodasi dan Makan Minum',
        'Informasi dan Komunikasi',
        'Jasa Keuangan dan Asuransi',
        'Perumahan',
        'Jasa Perusahaan',
        'Adm Pemerintahan, Pertahanan, dan Jamsos',
        'Jasa Pendidikan',
        'Jasa Kesehatan dan Kegiatan Sosial',
        'Jasa Lainnya'
    ],
    'Nilai (Miliar Rp)': [
        7760.63, 551.55, 6890.04, 264.69, 29.4, 1997.5, 3414.49,
        295.26, 401.34, 1015.9, 476.36, 641.45, 84.44, 729.83,
        691.66, 183.25, 477.13
    ]
}

jatim_data = {
    'Lapangan Usaha': [
        'Pertanian, Kehutanan, dan Perikanan',
        'Pertambangan',
        'Industri Pengolahan/Manufaktur',
        'Pengadaan Listrik dan Gas',
        'Penyedian Air dan Pengelolaan Sampah',
        'Konstruksi',
        'Perdagangan & Retail',
        'Transportasi dan Pergudangan',
        'Penyediaan Akomodasi dan Makan Minum',
        'Informasi dan Komunikasi',
        'Jasa Keuangan dan Asuransi',
        'Perumahan',
        'Jasa Perusahaan',
        'Adm Pemerintahan, Pertahanan, dan Jamsos',
        'Jasa Pendidikan',
        'Jasa Kesehatan dan Kegiatan Sosial',
        'Jasa Lainnya'
    ],
    'Nilai (Miliar Rp)': [
        177632.3, 73016.89, 558452.31, 6265.58, 1853.36, 170376.15, 352735.63,
        60314.16, 101732.19, 126964.01, 44736.2, 32469.01, 14196.94, 35054.16,
        48871.83, 13645.76, 26492.18
    ]
}

df_probolinggo = pd.DataFrame(probolinggo_data)
df_jatim = pd.DataFrame(jatim_data)

df_probolinggo['Persentase (%)'] = (df_probolinggo['Nilai (Miliar Rp)'] / df_probolinggo['Nilai (Miliar Rp)'].sum()) * 100
df_jatim['Persentase (%)'] = (df_jatim['Nilai (Miliar Rp)'] / df_jatim['Nilai (Miliar Rp)'].sum()) * 100

df_probolinggo['IS'] = df_probolinggo['Persentase (%)'] / df_jatim['Persentase (%)']

comparison_df = pd.DataFrame({
    'Lapangan Usaha': df_probolinggo['Lapangan Usaha'],
    'Probolinggo (%)': df_probolinggo['Persentase (%)'],
    'Jawa Timur (%)': df_jatim['Persentase (%)'],
    'Indeks Spesialisasi': df_probolinggo['IS']
})

# Menghitung selisih persentase
comparison_df['Selisih (%)'] = comparison_df['Probolinggo (%)'] - comparison_df['Jawa Timur (%)']

# Mengurutkan berdasarkan selisih untuk melihat perbedaan terbesar
comparison_df_sorted = comparison_df.sort_values(by='Selisih (%)', ascending=False)

# Membuat DataFrame untuk visualisasi perbandingan
comparison_visual = pd.melt(
    comparison_df,
    id_vars=['Lapangan Usaha'],
    value_vars=['Probolinggo (%)', 'Jawa Timur (%)'],
    var_name='Wilayah',
    value_name='Persentase'
)

# 1. Gambar 6
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
fig.suptitle('Perbandingan Struktur Ekonomi Kabupaten Probolinggo vs Jawa Timur (2023)', 
            fontsize=20, fontweight='bold', y=0.98)

# warna konsisten
all_sectors = df_probolinggo['Lapangan Usaha'].tolist()
num_sectors = len(all_sectors)
color_map = plt.cm.tab20
sector_colors = {sector: color_map(i % 20) for i, sector in enumerate(all_sectors)}

probolinggo_sorted = df_probolinggo.sort_values(by='Persentase (%)', ascending=False)
jatim_sorted = df_jatim.sort_values(by='Persentase (%)', ascending=False)
top_n = 6

top_sectors_probolinggo = probolinggo_sorted.head(top_n)['Lapangan Usaha'].tolist()
sizes_probolinggo = probolinggo_sorted.head(top_n)['Persentase (%)'].tolist()
colors_probolinggo = [sector_colors[sector] for sector in top_sectors_probolinggo]
other_size_probolinggo = probolinggo_sorted.iloc[top_n:]['Persentase (%)'].sum()
sizes_probolinggo.append(other_size_probolinggo)
colors_probolinggo.append(plt.cm.Greys(0.5))

top_sectors_jatim = jatim_sorted.head(top_n)['Lapangan Usaha'].tolist()
sizes_jatim = jatim_sorted.head(top_n)['Persentase (%)'].tolist()
colors_jatim = [sector_colors[sector] for sector in top_sectors_jatim]
other_size_jatim = jatim_sorted.iloc[top_n:]['Persentase (%)'].sum()
sizes_jatim.append(other_size_jatim)
colors_jatim.append(plt.cm.Greys(0.5))

short_labels = {
    'Pertanian, Kehutanan, dan Perikanan': 'Pertanian & Perikanan',
    'Industri Pengolahan/Manufaktur': 'Industri Pengolahan',
    'Perdagangan & Retail': 'Perdagangan & Retail',
    'Informasi dan Komunikasi': 'Info & Komunikasi',
    'Penyediaan Akomodasi dan Makan Minum': 'Akomodasi & Makan',
    'Jasa Keuangan dan Asuransi': 'Jasa Keuangan',
    'Adm Pemerintahan, Pertahanan, dan Jamsos': 'Administrasi Pemerintahan',
    'Transportasi dan Pergudangan': 'Transportasi'
}

wedges_probolinggo, _ = ax1.pie(sizes_probolinggo, colors=colors_probolinggo, 
                              startangle=90, wedgeprops={'edgecolor': 'w', 'linewidth': 1})
ax1.set_title('Kabupaten Probolinggo', fontsize=16, fontweight='bold')

wedges_jatim, _ = ax2.pie(sizes_jatim, colors=colors_jatim, 
                        startangle=90, wedgeprops={'edgecolor': 'w', 'linewidth': 1})
ax2.set_title('Jawa Timur', fontsize=16, fontweight='bold')

legend_labels_probolinggo = [
    f"{short_labels.get(sector, sector)}: {probolinggo_sorted[probolinggo_sorted['Lapangan Usaha']==sector]['Persentase (%)'].values[0]:.1f}%" 
    for sector in top_sectors_probolinggo
]
legend_labels_probolinggo.append(f"Lainnya: {other_size_probolinggo:.1f}%")

legend_labels_jatim = [
    f"{short_labels.get(sector, sector)}: {jatim_sorted[jatim_sorted['Lapangan Usaha']==sector]['Persentase (%)'].values[0]:.1f}%" 
    for sector in top_sectors_jatim
]
legend_labels_jatim.append(f"Lainnya: {other_size_jatim:.1f}%")

ax1.legend(wedges_probolinggo, legend_labels_probolinggo, 
         loc='center left', bbox_to_anchor=(0.97, 0.5), 
         frameon=True, fontsize=11)

ax2.legend(wedges_jatim, legend_labels_jatim, 
         loc='center left', bbox_to_anchor=(0.97, 0.5), 
         frameon=True, fontsize=11)

plt.tight_layout()
plt.subplots_adjust(wspace=0.2)

# 2. Gambar 7 - chart perbandingan komposisi
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 12), gridspec_kw={'width_ratios': [3, 2]})

comparison_df_sorted_by_prob = comparison_df.sort_values(by='Probolinggo (%)', ascending=True)

sectors = comparison_df_sorted_by_prob['Lapangan Usaha'].tolist()
num_sectors = len(sectors)
cmap = plt.cm.viridis
colors_dict = {sector: cmap(i/num_sectors) for i, sector in enumerate(sectors)}

bar_width = 0.4
y = np.arange(len(comparison_df_sorted_by_prob))

probolinggo_bars = ax1.barh(y - bar_width/2, comparison_df_sorted_by_prob['Probolinggo (%)'], 
                          bar_width, label='Kab. Probolinggo', color='#1f77b4', alpha=0.8)
jatim_bars = ax1.barh(y + bar_width/2, comparison_df_sorted_by_prob['Jawa Timur (%)'], 
                    bar_width, label='Jawa Timur', color='#ff7f0e', alpha=0.8)

ax1.set_yticks(y)
ax1.set_yticklabels(comparison_df_sorted_by_prob['Lapangan Usaha'], fontweight='normal')
ax1.set_xlabel('Persentase PDRB (%)', fontweight='bold')
ax1.grid(axis='x', linestyle='--', alpha=0.7)
ax1.legend(loc='lower right')

def add_percentage_labels(bars):
    for bar in bars:
        width = bar.get_width()
        ax1.text(width + 0.3, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}%', va='center')

add_percentage_labels(probolinggo_bars)
add_percentage_labels(jatim_bars)

colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in comparison_df_sorted_by_prob['Selisih (%)']]

selisih_bars = ax2.barh(comparison_df_sorted_by_prob['Lapangan Usaha'], 
                      comparison_df_sorted_by_prob['Selisih (%)'], 
                      color=colors, alpha=0.8)

ax2.axvline(x=0, color='black', linestyle='-', alpha=0.3)

ax2.set_xlabel('Selisih Persentase (Probolinggo - Jawa Timur)', fontweight='bold')
ax2.grid(axis='x', linestyle='--', alpha=0.7)
ax2.set_yticks([]) 

for bar in selisih_bars:
    width = bar.get_width()
    label_x = width + 0.3 if width > 0 else width - 0.8
    ax2.text(label_x, bar.get_y() + bar.get_height()/2, 
            f'{width:.1f}%', va='center', 
            ha='left' if width > 0 else 'right',
            color='black')

plt.tight_layout()
plt.suptitle('Perbandingan PDRB Kabupaten Probolinggo vs Jawa Timur (2023)', fontsize=20, fontweight='bold', y=1.02)
plt.subplots_adjust(top=0.92)

plt.show()