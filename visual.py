import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Langkah 1: Load Data
file_path = r'D:\git\pdrb\PDRB Harga Konstan 2010 Per Kab Jatim.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')

# Langkah 2: Visualisasi Tren PDRB untuk Beberapa Kabupaten/Kota
kabupaten_kota = ['Sidoarjo', 'Kota Surabaya', 'Malang', 'Bojonegoro', 'Pacitan']
filtered_data = data[data['Kabupaten/Kota'].isin(kabupaten_kota)].set_index('Kabupaten/Kota').T

plt.figure(figsize=(12, 6))
for kabupaten in kabupaten_kota:
    plt.plot(filtered_data.index, filtered_data[kabupaten], label=kabupaten)

plt.title('Tren PDRB 2014-2023')
plt.xlabel('Tahun')
plt.ylabel('PDRB (Miliar Rp)')
plt.legend()
plt.grid(True)
plt.show()

# Langkah 3: Visualisasi PDRB 2023 dengan Bar Chart
data_sorted = data.sort_values(by='2023', ascending=False)

plt.figure(figsize=(14, 8))
sns.barplot(x='2023', y='Kabupaten/Kota', data=data_sorted, palette='viridis')
plt.title('PDRB 2023 per Kabupaten/Kota di Jawa Timur')
plt.xlabel('PDRB (Miliar Rp)')
plt.ylabel('Kabupaten/Kota')
plt.show()

# Langkah 4: Analisis Pertumbuhan PDRB
data['Pertumbuhan (%)'] = ((data['2023'] - data['2014']) / data['2014']) * 100
data_sorted_growth = data.sort_values(by='Pertumbuhan (%)', ascending=False)

print("\n10 Kabupaten/Kota dengan Pertumbuhan Tertinggi:")
print(data_sorted_growth[['Kabupaten/Kota', 'Pertumbuhan (%)']].head(10))

print("\n10 Kabupaten/Kota dengan Pertumbuhan Terendah:")
print(data_sorted_growth[['Kabupaten/Kota', 'Pertumbuhan (%)']].tail(10))

# Langkah 5: Visualisasi Dampak Pandemi (2020-2021)
data['Perubahan 2019-2020 (%)'] = ((data['2020'] - data['2019']) / data['2019']) * 100
data['Perubahan 2020-2021 (%)'] = ((data['2021'] - data['2020']) / data['2020']) * 100

plt.figure(figsize=(14, 6))
sns.barplot(x='Kabupaten/Kota', y='Perubahan 2019-2020 (%)', data=data, color='blue', label='2019-2020')
sns.barplot(x='Kabupaten/Kota', y='Perubahan 2020-2021 (%)', data=data, color='orange', label='2020-2021')
plt.title('Perubahan PDRB Selama Pandemi COVID-19')
plt.xlabel('Kabupaten/Kota')
plt.ylabel('Perubahan PDRB (%)')
plt.xticks(rotation=90)
plt.legend()
plt.show()