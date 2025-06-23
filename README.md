# Analisis Proyek Energi Terbarukan - Produk Hijau X

Nama : Farhan Fadillah

No. Absen : 9.008.DB2025

Batch : 9

## Latar Belakang

Perubahan iklim global menjadi tantangan terbesar abad ini. Salah satu penyumbang terbesar emisi gas rumah kaca (GRK) adalah sektor energi, khususnya dari pembakaran bahan bakar fosil. Berdasarkan laporan IPCC (2021), sektor energi menyumbang sekitar **73% dari total emisi global**.

![image](https://github.com/user-attachments/assets/ff2ee286-319a-4527-9284-5c47c06ae936)


Indonesia sebagai negara berkembang memiliki tantangan unik:
- Ketergantungan tinggi terhadap energi fosil
- Ketimpangan distribusi energi antar wilayah
- Risiko ekologi lokal yang meningkat akibat eksploitasi energi

Maka dari itu, transisi menuju energi bersih seperti PLTS dan PLTM bukan hanya strategi iklim, tetapi kebutuhan keberlanjutan nasional.

---

## Tujuan Proyek

Produk Hijau X adalah inisiatif untuk:
- Mengimplementasikan proyek energi terbarukan secara masif di berbagai provinsi
- Memantau dampak lingkungan dan efisiensi tiap proyek secara real-time
- Menyediakan sistem rekomendasi untuk perbaikan atau replikasi proyek

**Nilai tambah proyek ini:**
- Memastikan setiap proyek tidak hanya ramah lingkungan, tetapi juga efisien
- Meminimalisir potensi risiko ekologis lokal
- Mempermudah audit ESG (Environmental, Social, Governance) secara data-driven

---

## Solusi yang Diimplementasikan

- ✅ Dashboard analitik lingkungan interaktif berbasis Python & Streamlit
- ✅ Visualisasi performa proyek: efisiensi CO₂, indeks risiko, lokasi, dan distribusi dampak
- ✅ Action Plan otomatis berbasis data
- ✅ Simulasi agregasi provinsi untuk alokasi anggaran & prioritas kebijakan

---

## Dasar Ilmiah & Referensi

1. **IPCC Sixth Assessment Report**  
   [https://www.ipcc.ch/report/ar6/wg3/](https://www.ipcc.ch/report/ar6/wg3/)

2. **IEA – Net Zero by 2050**  
   [https://www.iea.org/reports/net-zero-by-2050](https://www.iea.org/reports/net-zero-by-2050)

3. **KLHK – Inventarisasi GRK Nasional 2023**  
   [https://ditjenppi.menlhk.go.id](https://ditjenppi.menlhk.go.id)

4. **Bappenas – Low Carbon Development Initiative (LCDI)**  
   [https://lcdi-indonesia.id/](https://lcdi-indonesia.id/)

---

## Ringkasan Teknis Proyek

| Komponen         | Penjelasan                                                                  |
|------------------|------------------------------------------------------------------------------|
| **Data**         | Dataset proyek PLTS & PLTM di Indonesia                                      |
| **Tools**        | Python, Pandas, Plotly, Streamlit, Folium                                    |
| **Fitur utama**  | Dashboard, chart interaktif, peta proyek, action plan otomatis               |
| **Output akhir** | Aplikasi web dan notebook analitik                                           |
| **Skalabilitas** | Dapat diperluas ke prediksi tren, geojson spasial, integrasi data emisi      |


---


## Detail Technical Process Analysis
### Import Module
Menampilkan data table source dan membuat kolom baru "Kategori_Dampak" dari kolom "Peringkat_Dampak"

      import pandas as pd
      import plotly.express as px

### Load data
      df = pd.read_excel("Environmental_Dataset.xlsx", sheet_name="Environmental_Dataset")
      df["Provinsi"] = df["Project_ID"].str.extract(r'PL[TSM]+-([A-Z]+)-')
      df["Efisiensi_CO2_per_kWh"] = df["CO2_Reduction"] / df["Energy_Output"]
      df["Kategori_Dampak"] = df["Peringkat_Dampak"].str.extract(r'(High|Medium|Low)')
      df.head()

### Analisa Efisiensi C02 per kWh per Proyek dengan Bar Chart
      fig1 = px.bar(
          df,
          x="Project_ID",
          y="Efisiensi_CO2_per_kWh",
          color="Efisiensi_CO2_per_kWh",
          title="Efisiensi CO₂ per kWh per Proyek",
          color_continuous_scale="greens"
      )
      fig1.show()
![image](https://github.com/user-attachments/assets/a9d3ad07-ed35-44f9-836e-1851380ecf96)

### Analisa Enviromental Risk Index per Proyek dengan Bar Chart
      fig2 = px.bar(
          df,
          x="Project_ID",
          y="Environmental_Risk_Index",
          color="Environmental_Risk_Index",
          title="Environmental Risk Index per Proyek",
          color_continuous_scale="reds"
      )
      fig2.show()
![image](https://github.com/user-attachments/assets/acf34557-b55d-46d1-b859-aa5f20af645e)

### Analisa distribusi peringkat dampak lingkungan (analisa jumlah komposisi High and Medium) dengan Pie Chart
      pie_data = df["Kategori_Dampak"].value_counts().reset_index()
      pie_data.columns = ["Kategori", "Jumlah"]
      
      fig3 = px.pie(
          pie_data,
          names="Kategori",
          values="Jumlah",
          title="Distribusi Peringkat Dampak Lingkungan",
          color_discrete_sequence=px.colors.sequential.Viridis
      )
      fig3.show()
![image](https://github.com/user-attachments/assets/149061ef-ea17-4af2-b28d-680044b33908)

### Analisa Total C02, Rata-rata efisiensi, Rata-rata risiko per provinsi dengan Bar Chart
#### Total CO2 Reduction per Provinsi
      prov_emisi = df.groupby("Provinsi")["CO2_Reduction"].sum().reset_index()
      fig4 = px.bar(prov_emisi, x="Provinsi", y="CO2_Reduction", title="Total CO₂ Reduction per Provinsi")
      fig4.show()
![image](https://github.com/user-attachments/assets/640283e4-419d-4162-81b8-7bef435738a8)

#### Rata-rata Efisiensi per Provinsi
      prov_eff = df.groupby("Provinsi")["Efisiensi_CO2_per_kWh"].mean().reset_index()
      fig5 = px.bar(prov_eff, x="Provinsi", y="Efisiensi_CO2_per_kWh", title="Rata-rata Efisiensi CO₂ per Provinsi")
      fig5.show()
![image](https://github.com/user-attachments/assets/66b7fef3-150f-48fb-b344-307b547507bd)

#### Rata-rata Risiko per Provinsi
      prov_risk = df.groupby("Provinsi")["Environmental_Risk_Index"].mean().reset_index()
      fig6 = px.bar(prov_risk, x="Provinsi", y="Environmental_Risk_Index", title="Rata-rata Risk Index per Provinsi")
      fig6.show()
![image](https://github.com/user-attachments/assets/02ec0055-efc6-4f3a-b881-a6fb66f80479)

### Rekomendasi Action Plan Based on Environmental risk index dan Efisiensi C02 per kWh
      def generate_action_plan(row):
          rekomendasi = []

    if row["Environmental_Risk_Index"] >= 60:
        rekomendasi.append("🚨 Risiko tinggi: audit & konservasi diperlukan.")
    elif row["Environmental_Risk_Index"] >= 45:
        rekomendasi.append("⚠️ Risiko sedang: perlu mitigasi berkala.")
    else:
        rekomendasi.append("✅ Risiko rendah: layak direplikasi.")

    if row["Efisiensi_CO2_per_kWh"] >= 3.0:
        rekomendasi.append("💚 Efisiensi tinggi: cocok jadi proyek percontohan.")
    else:
        rekomendasi.append("📉 Efisiensi dapat ditingkatkan.")

    return " ".join(rekomendasi)

#### Apply ke DataFrame
      df["Action_Plan"] = df.apply(generate_action_plan, axis=1)
      df
![image](https://github.com/user-attachments/assets/c0419f4f-90aa-40ea-94e9-3d7344376310)


## Kesimpulan & Rekomendasi Akhir

- Proyek dengan **efisiensi tinggi** layak untuk dijadikan model di provinsi lain (ex: JATIM, JABW).
- Provinsi dengan **tingkat risiko tinggi** (ex: SUMUT, PAPU) memerlukan **penguatan audit dan mitigasi**.
- Dashboard berbasis data ini dapat membantu pengambil keputusan dalam **alokasi anggaran hijau**, serta memprioritaskan lokasi berdasarkan **data objektif**.

