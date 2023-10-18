# Streamlit app for the plot with faceting

import streamlit as st
import pandas as pd
import altair as alt
from clean_data import combined_df_cleaned as combined_df

st.title("Exploring the Relationship between Patient Portal Access and Patient Centered communication")

st.markdown("""
## Introduction

The digital era has brought about significant transformations in various sectors, including healthcare. Patient portals are used by patients to access their electronic health records, check their health status, order prescription refills, and more. The way patients access, utilize, and interact with healthcare through the patient portals can have important implications for health outcomes and equity. 

## Objective

The primary objectives of this study are: (1) to examine patients' access of patient portals over time, (2) to understand the correlation between access of patient portals and patient provider communication, and (3) to analyze the disparities in patient provider communication across various demographic groups, including sex, age, race, ethnicity, education level, and location.

Such an exploration is crucial because effective utilization of the patient portals may significantly influence health outcomes. Addressing disparities in access and use of these digital tools ensures equitable health benefits for all. This type of data exploration should also shed light on the areas requiring policy interventions.

## Dataset Exploration

The project will include the analysis of four cycles of the HINTS survey (each conducted on different years): HINTS 5 Cycle 1 (2017), Cycle 3 (2019), Cycle 4 (2020), and HINTS 6 (2022). As a survey conducted by the National Cancer Institute, HINTS evaluates the U.S. adult population's accessibility and usage of health-related information. However, there is the issue of missing data, often due to non-responses or vague answers. The reasons for missing data were as follows: 

""")

# Dropdown to select the x-variable
x_variable = st.selectbox(
    "Choose the x variable:",
    ['SpentEnoughTime', 'InvolvedDecisions', 'ChanceAskQuestions', 
     'FeelingsAddressed', 'UnderstoodNextSteps', 'HelpUncertainty', 'ExplainedClearly']
)

# Dropdown to select the year
selected_year = st.selectbox("Choose the year:", [2017, 2019, 2020, 2022])

# Subset the dataframe for the specific year
year_subset = combined_df[combined_df['survey_year'] == selected_year]

# Calculate proportions
grouped_df = year_subset.groupby([x_variable, 'AccessOnlineRecord_cat_2']).size().reset_index(name='counts')
total = year_subset.groupby(x_variable).size().reset_index(name='total')
grouped_df = grouped_df.merge(total, on=x_variable)
grouped_df['proportion'] = grouped_df['counts'] / grouped_df['total']

# Define your custom orders here
spent_enough_time_order = ['Never', 'Sometimes', 'Usually', 'Always']
access_online_record_cat_2_order = ["None", "1 to 2 times", "3 to 5 times", "6 to 9 times", "10 or more times"]

# Base chart
base = alt.Chart(grouped_df).mark_bar().encode(
    x=alt.X('AccessOnlineRecord_cat_2:N', sort=access_online_record_cat_2_order, title=None),
    y=alt.Y('proportion:Q', axis=alt.Axis(format='%')),
    color='AccessOnlineRecord_cat_2:N',
    tooltip=[x_variable, 'AccessOnlineRecord_cat_2', 'proportion']
).properties(
    width=150
)

# Facet the chart
chart = base.facet(
    column=alt.Column(f'{x_variable}:N', sort=spent_enough_time_order, header=alt.Header(labelOrient="top", title="How many times did you access your online medical record or patient portal in the last 12 months?", titleOrient="bottom")),
    spacing=15
).resolve_scale(
    x='shared'
).properties(
    title=f"Proportion of those who accessed online portals by '{x_variable}' for the year {selected_year}"
)

st.altair_chart(chart)


st.markdown("""

## Conclusion

In the age of digital health and telemedicine, understanding the patterns and disparities of patients' access to online portals is very important. This project emphasizes the need for equal access to health technologies and promotes optimal health outcomes for all.
""")