import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

plt.style.use('seaborn-v0_8-whitegrid')
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.right'] = False

data = {
    'Lapangan Usaha': [
        'Pertanian', 'Pertambangan', 'Manufaktur', 'Listrik/Gas', 'Air/Limbah',
        'Konstruksi', 'Perdagangan', 'Transportasi', 'Akomodasi', 'IT/Komunikasi',
        'Keuangan', 'Properti', 'Jasa Bisnis', 'Pemerintahan', 'Pendidikan', 'Kesehatan', 'Jasa Lainnya'
    ],
    'Nilai': [
        7883.57, 586.55, 7383.31, 280.12, 28.29, 2124.92, 3554.9, 331.61, 426.35, 
        1082.22, 500.52, 666.69, 91.14, 782.76, 724.42, 191.5, 514.21
    ]
}

df = pd.DataFrame(data)

total = df['Nilai'].sum()
df['Persentase'] = (df['Nilai'] / total * 100).round(1)

df = df.sort_values(by='Nilai', ascending=False)

jumlah_sektor_tampil = 6
top_sectors = df.head(jumlah_sektor_tampil).copy()
other_sectors = df.iloc[jumlah_sektor_tampil:].copy()

if not other_sectors.empty:
    other_value = other_sectors['Nilai'].sum()
    other_percentage = (other_value / total * 100).round(1)
    other_row = pd.DataFrame({
        'Lapangan Usaha': ['Lainnya'],
        'Nilai': [other_value],
        'Persentase': [other_percentage]
    })
    top_sectors = pd.concat([top_sectors, other_row])

colors = plt.cm.Paired(np.linspace(0, 1, len(top_sectors)))
plt.figure(figsize=(8, 6), dpi=300)

wedges, texts, autotexts = plt.pie(
    top_sectors['Nilai'],
    labels=top_sectors['Lapangan Usaha'],
    colors=colors,
    startangle=90,
    wedgeprops=dict(width=0.4, edgecolor='white', linewidth=1),
    autopct='%1.1f%%'
)

for text in texts:
    text.set_fontsize(5)
    text.set_fontweight('bold')

for autotext in autotexts:
    autotext.set_fontsize(4)
    text.set_fontweight('bold')

centre_circle = plt.Circle((0, 0), 0.6, fc='white', edgecolor='white')
plt.gca().add_artist(centre_circle)

plt.title('Struktur Ekonomi Kabupaten Probolinggo 2024', fontsize=8, fontweight='bold')
plt.show()