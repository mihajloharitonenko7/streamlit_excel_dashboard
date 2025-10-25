import streamlit as st
import pandas as pd
import io
import os

st.set_page_config(page_title="Excel Dashboard", layout="wide")
st.title("📊 Інтеграція Excel з Python-дашбордом (Streamlit)")

# --- КРОК 1. Завантаження даних ---
st.sidebar.header("📂 Завантаження Excel")

uploaded_file = st.sidebar.file_uploader("Завантаж свій Excel-файл", type=["xlsx", "xls"])
default_path = "sample.xlsx"

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Завантажено власний файл.")
elif os.path.exists(default_path):
    df = pd.read_excel(default_path)
    st.success("✅ Автоматично завантажено sample.xlsx із локальної папки.")
else:
    st.error("❌ Файл не знайдено. Завантаж Excel-файл вручну.")
    st.stop()

# --- КРОК 2. Перегляд даних ---
st.subheader("🔍 Попередній перегляд даних")
st.dataframe(df, use_container_width=True)

# --- КРОК 3. Фільтрація ---
st.subheader("⚙️ Фільтрація")
columns = df.columns.tolist()
column_to_filter = st.selectbox("Оберіть колонку для фільтрації", columns)
unique_values = df[column_to_filter].dropna().unique()
selected_value = st.selectbox(f"Значення у '{column_to_filter}'", unique_values)

filtered_df = df[df[column_to_filter] == selected_value]

st.write("📋 Відфільтровані дані:")
st.dataframe(filtered_df, use_container_width=True)

# --- КРОК 4. Візуалізація ---
st.subheader("📈 Графік")
numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

if len(numeric_cols) >= 2:
    x_col = st.selectbox("X-вісь", numeric_cols, index=0)
    y_col = st.selectbox("Y-вісь", numeric_cols, index=1)
    st.line_chart(filtered_df[[x_col, y_col]])
else:
    st.warning("У таблиці немає достатньо числових даних для графіка.")

# --- КРОК 5. Завантаження результату ---
st.subheader("💾 Завантаж відфільтрований Excel")
buffer = io.BytesIO()
filtered_df.to_excel(buffer, index=False)
buffer.seek(0)

st.download_button(
    label="⬇️ Завантажити Excel",
    data=buffer,
    file_name="filtered_data.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
