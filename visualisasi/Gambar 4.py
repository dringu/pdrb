import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "D:/git/pdrb/data/PDRB Harga Konstan 2010 Per Kab Jatim1.xlsx"
data = pd.read_excel(file_path, skiprows=1) 
data.columns = ['Kabupaten/Kota', 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

probolinggo = data[data['Kabupaten/Kota'].str.strip() == 'Probolinggo'].iloc[:, 1:].T
probolinggo.columns = ['PDRB']
probolinggo = probolinggo.reset_index()
probolinggo.columns = ['Tahun', 'PDRB']
probolinggo['Tahun'] = probolinggo['Tahun'].astype(int)
probolinggo['Pertumbuhan (%)'] = probolinggo['PDRB'].pct_change() * 100

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
sns.lineplot(data=probolinggo, x='Tahun', y='PDRB', marker='o', color='#3498DB', linewidth=2.5)
plt.title('Tren PDRB Probolinggo (2015-2024)', fontweight='bold', pad=20)
plt.xlabel('Tahun', labelpad=10)
plt.ylabel('PDRB (Miliar Rp)', labelpad=10)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(probolinggo['Tahun'])

plt.subplot(2, 1, 2)
bars = plt.bar(probolinggo['Tahun'][1:], probolinggo['Pertumbuhan (%)'][1:], 
              color=['#E74C3C' if x < 0 else '#2ECC71' for x in probolinggo['Pertumbuhan (%)'][1:]])
plt.title('Pertumbuhan Tahunan (%)', fontweight='bold', pad=20)
plt.xlabel('Tahun', labelpad=10)
plt.ylabel('Pertumbuhan (%)', labelpad=10)
plt.axhline(y=0, color='black', linestyle='--')
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, 
             f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top', fontsize=9)

plt.tight_layout()
plt.show()
#plt.savefig("tren_probolinggo.png", dpi=300, bbox_inches='tight')