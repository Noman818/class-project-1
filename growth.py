import streamlit as st
import pandas as pd
import os
from io import BytesIO
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    .app {
        background-color: black;
        color: white;    
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Datasweeper Sterling Integrator by Muhammad Noman")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning tools.")

# File uploader
uploaded_files = st.file_uploader(
    label="Upload your CSV or Excel files", 
    type=['csv', 'xlsx'], 
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.write(f"Unsupported file type: {file_ext}")
            continue

        # File details and preview
        st.write(f"### Preview of {uploaded_file.name}")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader(f"Clean Data for {uploaded_file.name}")
        if st.checkbox(f"Enable data cleaning for {uploaded_file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove duplicates from {uploaded_file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed!")
            
            with col2:
                if st.button(f"Fill missing values in {uploaded_file.name}"):
                    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled!")

        # Select columns to keep
        st.subheader("Select Columns to Keep")
        columns = st.multiselect(
            f"Choose columns for {uploaded_file.name}", 
            df.columns, 
            default=list(df.columns)
        )
        if columns:
            df = df[columns]

        # Data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show visualization for {uploaded_file.name}"):
            numeric_cols = df.select_dtypes(include='number').columns
            if len(numeric_cols) >= 2:
                fig = px.bar(
                    df, 
                    x=numeric_cols[0], 
                    y=numeric_cols[1], 
                    title=f"Bar Chart for {uploaded_file.name}",
                    labels={numeric_cols[0]: "X-Axis", numeric_cols[1]: "Y-Axis"},
                    template="plotly_dark"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Not enough numeric columns for visualization!")

        # Conversion options
        st.subheader("Conversion Options")
        convert_type = st.radio(
            f"Convert {uploaded_file.name} to", 
            ["csv", "xlsx"]
        )
        if st.button(f"Convert {uploaded_file.name}"):
            buffer = BytesIO()
            if convert_type == "csv":
                df.to_csv(buffer, index=False)
                file_name = uploaded_file.name.replace(".xlsx", ".csv")
                mime_type = "text/csv"
            elif convert_type == "xlsx":
                df.to_excel(buffer, index=False)
                file_name = uploaded_file.name.replace(".csv", ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)
            st.download_button(
                label=f"Download {uploaded_file.name} as {convert_type.upper()}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
    st.success("All files processed successfully!")
