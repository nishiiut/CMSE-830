import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    return pd.read_sas('hints5_cycle4_public.sas7bdat')

df = load_data()

st.title("Hints5 Cycle4")

plot_choice = st.sidebar.selectbox(
    "Choose a Plot Type:",
    ["Line Plot of DRA", "Histogram of Weekly Minutes of Moderate Exercise"]
)

if plot_choice == "Line Plot of DRA":
    st.write("Displaying Line Plot of DRA")
    fig, ax = plt.subplots()
    ax.plot(df['DRA'])
    ax.set_title('Line Plot of DRA')
    ax.set_xlabel('Index')
    ax.set_ylabel('DRA')
    st.pyplot(fig)

elif plot_choice == "Histogram of Weekly Minutes of Moderate Exercise":
    st.write("Displaying Histogram of Weekly Minutes of Moderate Exercise")
    fig, ax = plt.subplots()
    ax.hist(df['WeeklyMinutesModerateExercise'].dropna(), bins=30) 
    ax.set_title('Histogram of Weekly Minutes of Moderate Exercise')
    ax.set_xlabel('Weekly Minutes of Moderate Exercise')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
