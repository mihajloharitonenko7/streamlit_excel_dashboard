import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Excel Dashboard", layout="wide")
st.title("📊 Інтеграція Excel з Python-дашбордом (Streamlit)")

uploaded_file = st.file_uploader("📂 Завантаж Excel-файл", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.subheader("🔎 Попередній перегляд даних")
    st.dataframe(df, use_container_width=True)

    st.subheader("⚙️ Фільтрація даних")
    columns = df.columns.tolist()
    column_to_filter = st.selectbox("Оберіть колонку для фільтрації:", columns)

    unique_values = df[column_to_filter].dropna().unique()
    selected_value = st.selectbox(f"Оберіть значення для '{column_to_filter}'", unique_values)

    filtered_df = df[df[column_to_filter] == selected_value]

    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("📈 Візуалізація даних")
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    if len(numeric_cols) >= 2:
        x_col = st.selectbox("X-вісь", numeric_cols, index=0)
        y_col = st.selectbox("Y-вісь", numeric_cols, index=1)
        st.line_chart(filtered_df[[x_col, y_col]])
    else:
        st.warning("У таблиці немає достатньо числових стовпців для побудови графіка.")

    st.subheader("💾 Завантаження відфільтрованого Excel")

    buffer = io.BytesIO()
    filtered_df.to_excel(buffer, index=False)
    buffer.seek(0)

    st.download_button(
        label="⬇️ Завантажити відфільтровані дані (Excel)",
        data=buffer,
        file_name="filtered_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("👆 Завантажте Excel-файл для початку роботи.")
