import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.titlepad'] = 20

file_path = "D:/git/pdrb/data/PDRB ADHB Tetangga Per Lapangan Usaha.xlsx"
data = pd.read_excel(file_path)

data.set_index('Lapangan Usaha', inplace=True)
gdp_row_name = [x for x in data.index if 'Produk Domestik' in x][0]

full_sector_map = {
    'APertanian, Kehutanan, dan Perikanan\nAgriculture, Forestry, and Fishing': 'Pertanian',
    'BPertambangan dan Penggalian/Mining and Quarrying': 'Pertambangan',
    'CIndustri Pengolahan/Manufacturing': 'Manufaktur',
    'DPengadaan Listrik dan Gas/Electricity and Gas': 'Listrik/Gas',
    'EPengadaan Air; Pengelolaan Sampah, Limbah,\ndan Daur Ulang/ Water Supply; Sewerage,\nWaste Management, and Remediation Activities': 'Air/Limbah',
    'FKonstruksi/Construction': 'Konstruksi',
    'GPerdagangan Besar dan Eceran; Reparasi Mobil\ndan Sepeda Motor/Wholesale and Retail Trade;\nRepair of Motor Vehicles and Motorcycles': 'Perdagangan',
    'HTransportasi dan Pergudangan/Transportation and Storage': 'Transportasi',
    'IPenyediaan Akomodasi dan Makan Minum\nAccommodation and Food Service Activities': 'Akomodasi',
    'JInformasi dan Komunikasi\nInformation and Communication': 'IT/Komunikasi',
    'KJasa Keuangan dan Asuransi\nFinancial and Insurance Activities': 'Keuangan',
    'LReal Estat/Real Estate Activities': 'Properti',
    'M,NJasa Perusahaan/Business Activities': 'Jasa Bisnis',
    'OAdministrasi Pemerintahan, Pertahanan,\ndan Jaminan Sosial Wajib/Public Administration\nand Defence; Compulsory Social Security': 'Pemerintahan',
    'PJasa Pendidikan/Education': 'Pendidikan',
    'QJasa Kesehatan dan Kegiatan Sosial\nHuman Health and Social Work Activities': 'Kesehatan',
    'R,S,T,UJasa Lainnya/Other Services Activities': 'Jasa Lainnya'
}

pct_data = data.div(data.loc[gdp_row_name]) * 100
abs_data = data.copy()
pct_data_short = pct_data.rename(index=full_sector_map)
abs_data_short = abs_data.rename(index=full_sector_map)

all_regions = ['Pasuruan', 'Situbondo', 'Lumajang', 'Jember', 'Probolinggo', 'Kota Probolinggo']

# Gambar 8 - Top 5 Sektor
plt.figure(figsize=(16, 10))

for i, region in enumerate(all_regions, 1):
    region_pct = pct_data_short[region].drop(gdp_row_name, errors='ignore')
    top_sectors = region_pct.nlargest(5)
    
    abs_values = abs_data_short.loc[top_sectors.index, region]
    
    ax = plt.subplot(2, 3, i)
    bars = sns.barplot(x=top_sectors.values, y=top_sectors.index, palette='Blues_r')

    for j, (sector, pct) in enumerate(top_sectors.items()):
        abs_val = abs_values.loc[sector]
        ax.text(pct + 1, j, 
                f'{pct:.1f}%\n({abs_val/1e3:,.1f}T)', 
                va='center', 
                fontsize=9,
                color='dimgrey')
    
    plt.title(f'5 Sektor Utama - {region}', fontsize=12, pad=5, fontweight='bold')
    plt.xlim(0, max(top_sectors) * 1.3)
    if i not in [1, 4]:
        plt.ylabel('')
    
plt.tight_layout()
plt.show()

# Gambar 9 - Perbandingan sektor kunci
key_sectors = ['Pertanian', 'Manufaktur', 'Perdagangan', 'Konstruksi', 'Transportasi']
plt.figure(figsize=(14, 7))
ax = sns.barplot(
    data=pct_data_short.loc[key_sectors][all_regions].reset_index().melt(id_vars='Lapangan Usaha'),
    x='Lapangan Usaha', y='value', hue='variable',
    palette='Set2'
)

for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{height:.1f}%', 
                (p.get_x() + p.get_width()/2., height + 1), 
                ha='center', 
                fontsize=9,
                color='dimgrey')

plt.title('Perbandingan Sektor Kunci - Probolinggo Vs Tetangga', fontsize=14, fontweight='bold')
plt.ylabel('Kontribusi terhadap PDRB (%)', fontsize=11)
plt.xlabel('', fontsize=11)
plt.xticks(fontsize=10, fontweight='bold')
plt.legend(title='Wilayah', bbox_to_anchor=(1.05, 1), fontsize=9)
plt.tight_layout()
plt.show()