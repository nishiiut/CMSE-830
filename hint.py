# my_streamlit_app.py

import streamlit as st
import pandas as pd
import sas7bdat

# Load the dataset
@st.cache  # This decorator will make the data loading faster
def load_data():
    with sas7bdat.SAS7BDAT('hints5_cycle4_public.sas7bdat.sas7bdat') as f:
        df = f.to_data_frame()
    return df

data = load_data()

# App title
st.title('Streamlit App for hints5_cycle4_public Dataset')

# Display a subset of the dataset
num_rows = st.slider('Select number of rows to view', 1, 100, 50)
st.write(data.head(num_rows))


