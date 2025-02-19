import streamlit as  from django.conf import setting
import pandas as pd
import io import BytesIO
from IO import BytesIO

st.set_page_config(page_title== "data sweeper",layout='wide')

# custom css 
st.markdown(
    """
    <style>
    .app{
        background-color: black;
        color: white;    
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("Datasweeper sterling integrator by MuhammadNoman")
st.write("Transaction your files between csv and Excel formants with built  -in data cleaning")

#filuploader  
uploader = st.file_uploader(label="Upload your CSV or Excel file", type=['csv','xlsx']),accept_multiple_files=(True)

if uploader_file:
    for file in uploaded _ files:
        file_ext = os .path.splitext (file.name)[1].lower()
        
    if file_ext ==".csv":
        df=pd.read_csv(file)
    elif file_ext == ".xlsx":
        df=pd.read_excel(file)
    else:
    st.write("unsupported file type: {file_ext}")
   continue

#file details
st.write("preview the head of the DataFrame")
st.dataframe(df.head())

#state cleaaning options
st.subheader("clean data for(file.name)"):)
if st.checkbox("clean dats for {file.name}"):
      col1, co2=.columns (2)
      
      with col1:
              if st.button(f"Remove duplicates from the file :{file.name}"):
                  df.drop_duplicates(inplace=True)
                  st.write("Duplicates removed!")
                  
withcol2:    
if st.button(f"Fill missing values for {file.name}"):
    numbeic_cols = df.select_dtypes(include=['float64','int64']).columns
    df[numberic_cols].fillna(df[numberic_cols]-mean())
    st.write("Missing values filled!")
       
#st.sutheasder("salect Colums to keep") 
    columns=st.multiselect(f"choose colums for {file-name},df.colums,default=df.columns)
      df=df[columns]
      
      
       #data visualization
         st.subheader("Data Visualization")
         if st.checkbox("Data Visualization")
                 st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
                         
                 #conversion options
           
           st.subheader("Conversion Options")
         convert_type=st.radiort{file.name} to",["csv","xlsx"])
         if st.button(f-"convart{file.name}")
          buffer=BytesIO()
            if convert_type=="csv":
                df.to_csv(buffer,index=False)
                file_name=file.name.replace(".xlsx",".csv")
                 min_type="text/csv"    
                                           
       elif continue_type=="xlsx":
           df.to_excel(buffer,index=False)
           file_name=file.name.replace(".csv",".xlsx")
           min_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
         buffer.seek(0)
      
      st.download_button(
          label=f"Download{file.name}as{conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=type=min_type
            )
     at.success("All files processed successfully!")