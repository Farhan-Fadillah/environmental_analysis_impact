import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("Environmental_Dataset.xlsx", sheet_name="Environmental_Dataset")
    df["Provinsi"] = df["Project_ID"].str.extract(r'PL[TSM]+-([A-Z]+)-')
    df["Efisiensi_CO2_per_kWh"] = df["CO2_Reduction"] / df["Energy_Output"]
    df["Kategori_Dampak"] = df["Peringkat_Dampak"].str.extract(r'(High|Medium|Low)')
    return df

df = load_data()

st.set_page_config(layout="wide")
st.title("Environmental Project Dashboard - Produk Hijau X")
st.markdown("Made by Farhan Fadillah")

# Sidebar Summary
with st.sidebar:
    st.header("Summary")
    st.metric("Total CO₂ Reduction (kg)", int(df["CO2_Reduction"].sum()))
    st.metric("Total Energy Output (kWh)", int(df["Energy_Output"].sum()))
    st.metric("Rata-rata Risiko Lingkungan", round(df["Environmental_Risk_Index"].mean(), 2))

# Section: Dashboard
st.subheader("Analisis Proyek")
col1, col2 = st.columns(2)

with col1:
    top_eff = df.sort_values("Efisiensi_CO2_per_kWh", ascending=False).iloc[0]
    st.success(f"Proyek Paling Efisien: {top_eff['Project_ID']} ({top_eff['Efisiensi_CO2_per_kWh']:.2f} kg/kWh)")

with col2:
    top_risk = df.sort_values("Environmental_Risk_Index", ascending=False).iloc[0]
    st.warning(f"Risiko Tertinggi: {top_risk['Project_ID']} (Index: {top_risk['Environmental_Risk_Index']})")

# Table
st.markdown("### Tabel Data Proyek")
st.dataframe(df, use_container_width=True)

# Mapping by Province
province_coords = {
    "NTT": [-10.1772, 123.607], "NTB": [-8.652, 117.361],
    "JATIM": [-7.536, 112.238], "SUMUT": [2.1154, 99.5451],
    "KALB": [0.1322, 111.096], "PAPU": [-4.2699, 138.08],
    "SULS": [-3.6688, 119.974], "SULU": [1.4306, 120.654],
    "ACHD": [4.6951, 96.7494], "JABW": [-6.9175, 107.6191]
}
df["lat"] = df["Provinsi"].map(lambda x: province_coords.get(x, [None, None])[0])
df["lon"] = df["Provinsi"].map(lambda x: province_coords.get(x, [None, None])[1])

st.markdown("### Peta Lokasi Proyek dengan Informasi")
map_df = df.dropna(subset=["lat", "lon"])
m = folium.Map(location=[-2, 117], zoom_start=4)

for _, row in map_df.iterrows():
    popup_text = f'''
    <b>Project:</b> {row["Project_ID"]}<br>
    <b>Provinsi:</b> {row["Provinsi"]}<br>
    <b>Peringkat Dampak:</b> {row["Peringkat_Dampak"]}<br>
    <b>Risk Index:</b> {row["Environmental_Risk_Index"]}<br>
    <b>Energy Output:</b> {row["Energy_Output"]} kWh<br>
    <b>CO2 Reduction:</b> {row["CO2_Reduction"]} kg
    '''
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=8,
        color='green',
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=250)
    ).add_to(m)

st_data = st_folium(m, width=900, height=500)

# =============================
# 📊 Visualisasi Interaktif
# =============================
st.subheader("Visualisasi Data")

# Efisiensi CO₂ per kWh (sorted)
sorted_df_eff = df.sort_values("Efisiensi_CO2_per_kWh", ascending=False)
fig1 = px.bar(
    sorted_df_eff,
    x="Project_ID",
    y="Efisiensi_CO2_per_kWh",
    color="Efisiensi_CO2_per_kWh",
    color_continuous_scale="greens",
    title="Efisiensi CO₂ per kWh per Proyek"
)
st.plotly_chart(fig1, use_container_width=True)

# Risiko Lingkungan (sorted)
sorted_df_risk = df.sort_values("Environmental_Risk_Index", ascending=False)
fig2 = px.bar(
    sorted_df_risk,
    x="Project_ID",
    y="Environmental_Risk_Index",
    color="Environmental_Risk_Index",
    color_continuous_scale="reds",
    title="Environmental Risk Index per Proyek"
)
st.plotly_chart(fig2, use_container_width=True)

# Pie Chart Peringkat Dampak
pie_data = df["Kategori_Dampak"].value_counts().reset_index()
pie_data.columns = ["Kategori", "Jumlah"]
fig3 = px.pie(
    pie_data,
    names="Kategori",
    values="Jumlah",
    title="Distribusi Peringkat Dampak Lingkungan",
    color_discrete_sequence=px.colors.sequential.Viridis
)
st.plotly_chart(fig3, use_container_width=True)

# Visualisasi Berdasarkan Provinsi
st.subheader("Visualisasi Berdasarkan Provinsi")

# Total CO₂ Reduction per Provinsi (sorted)
prov_emisi = df.groupby("Provinsi")["CO2_Reduction"].sum().reset_index().sort_values("CO2_Reduction", ascending=False)
fig4 = px.bar(
    prov_emisi,
    x="Provinsi",
    y="CO2_Reduction",
    title="Total CO₂ Reduction per Provinsi",
    color="CO2_Reduction",
    color_continuous_scale="Greens"
)
st.plotly_chart(fig4, use_container_width=True)

# Rata-rata Efisiensi per Provinsi (sorted)
prov_efisiensi = df.groupby("Provinsi")["Efisiensi_CO2_per_kWh"].mean().reset_index().sort_values("Efisiensi_CO2_per_kWh", ascending=False)
fig5 = px.bar(
    prov_efisiensi,
    x="Provinsi",
    y="Efisiensi_CO2_per_kWh",
    title="Rata-rata Efisiensi CO₂ per kWh per Provinsi",
    color="Efisiensi_CO2_per_kWh",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig5, use_container_width=True)

# Rata-rata Risiko Lingkungan per Provinsi (sorted)
prov_risk = df.groupby("Provinsi")["Environmental_Risk_Index"].mean().reset_index().sort_values("Environmental_Risk_Index", ascending=False)
fig6 = px.bar(
    prov_risk,
    x="Provinsi",
    y="Environmental_Risk_Index",
    title="Rata-rata Environmental Risk Index per Provinsi",
    color="Environmental_Risk_Index",
    color_continuous_scale="Reds"
)
st.plotly_chart(fig6, use_container_width=True)

# =============================
# 🧭 Rekomendasi & Action Plan
# =============================
st.subheader("Rekomendasi & Action Plan")

selected_project = st.selectbox("Pilih Project ID", df["Project_ID"].unique())
selected_row = df[df["Project_ID"] == selected_project].iloc[0]

st.markdown(f"### Project: **{selected_project}** ({selected_row['Provinsi']})")

if selected_row["Environmental_Risk_Index"] >= 60:
    st.write("- 🚨 Risiko tinggi, perlu audit lingkungan dan konservasi area sekitar.")
elif selected_row["Environmental_Risk_Index"] >= 45:
    st.write("- ⚠️ Risiko sedang, lakukan pemantauan berkala dan mitigasi teknis.")
else:
    st.write("- ✅ Risiko rendah, direkomendasikan untuk direplikasi di wilayah lain.")

if selected_row["Efisiensi_CO2_per_kWh"] >= 3.0:
    st.write("- 💚 Efisiensi sangat baik, cocok jadi proyek percontohan.")
else:
    st.write("- 📉 Efisiensi bisa ditingkatkan, evaluasi teknologi yang digunakan.")
