import streamlit as st
import pandas as pd
import altair as alt
from clean_data import combined_df_cleaned as combined_df

st.title("Exploring the Relationship between Patient Portal Access and Patient Centered communication")

st.markdown("""
## Introduction

The digital era has brought about significant transformations in various sectors, including healthcare. Patient portals are used by patients to access their electronic health records, check their health status, order prescription refills, and more. The way patients access, utilize, and interact with healthcare through the patient portals can have important implications for health outcomes and equity. 

## Objective

The primary objectives of this study are: (1) to examine patients' access of patient portals for various demographic categories over time, (2) to understand the correlation between access of patient portals and patient provider communication, and (3) to analyze the disparities in patient provider communication and portal access across various demographic groups, including sex, age, race, ethnicity, education level, and location.

Such an exploration is crucial because effective utilization of the patient portals may significantly influence health outcomes. Addressing disparities in access of portals through improvements in patient communication may ensure equitable health benefits for all. This type of data exploration should also shed light on the areas requiring policy interventions.

## Dataset Exploration

The project will include the analysis of four cycles of the HINTS survey (each conducted on different years): HINTS 5 Cycle 1 (2017), Cycle 3 (2019), Cycle 4 (2020), and HINTS 6 (2022). 
            As a survey conducted by the National Cancer Institute, HINTS evaluates the U.S. adult population's accessibility and usage of health-related information. 
            However, there is the issue of missing data, often due to non-responses or vague answers. The reasons for missing data were as follows: 
            Missing data (Not Ascertained), Multiple responses selected in error, Question answered in error (Commission Error), Inapplicable, Unreadable, and  Non-conforming numeric response.
            Because there were a sufficient number of subjects in each survey, any rows with missing data were dropped from the study.
            After dropping the rows with missing data, HINTS 5 Cycle 1 (2017) had 2514 subjects, Cycle 3 (2019) had 2157 subjects, Cycle 4 (2020) had 3017 subjects, and HINTS 6 (2022) had 4855 subjects.

""")


st.markdown("""
### Part 1: Patients' access of patient portals      
For the initial phase of this project, we examined the survey question: "How many times did you access your online medical record or patient portal in the last 12 months?" Respondents who answered "0" were recoded as "No", while those who reported a number greater than "0" were recoded as "Yes". After this recoding process, we plotted the proportion of patients recoded as "Yes" (i.e., those who accessed an online portal at least once) over time, segmented by various demographic categories.

The plots revealed two primary observations. Firstly, there has been a general increase in patient portal access by patients over time across all demographic categories. Secondly, a marked surge in the number of patients accessing online portals was observed following the onset of the COVID pandemic, which can be attributed to a higher reliance on telehealth visits.

When assessing portal access variations among different demographic categories, it's evident that Black and Hispanic individuals, those with lower educational levels, residents of non-metro areas, individuals in fair or poor health, those without internet access, the uninsured, and older populations generally accessed portals less frequently across all timeframes. This trend is concerning, as these groups are often already marginalized in many healthcare contexts. If these individuals remain less engaged with patient portals, their ability to benefit from healthcare resources might be limited, potentially exacerbating existing healthcare disparities.
""")

# Create a dictionary to map column names to more descriptive strings
column_map = {
    'RaceEthn5': 'Race/Ethnicity',
    'BirthGender': 'Birth Gender',
    'EducA': 'Education Level',
    'RUC2013': 'Rural-Urban Code',
    'GeneralHealth': 'General Health',
    'UseInternet': 'Internet Usage',
    'HealthInsurance': 'Health Insurance',
    'age_cat': 'Age Category'
}

# Use the mapped strings in the dropdown
selected_label = st.selectbox(
    "Choose the variable to group by:",
    list(column_map.values())
)

# Get the actual column name based on the selected string
group_variable = [col for col, label in column_map.items() if label == selected_label][0]

# Calculate proportions for the selected variable
grouped_df = combined_df.groupby(['survey_year', group_variable])
yes_grouped = grouped_df['AccessOnlineRecord_cat'].apply(lambda x: (x == 'Yes').mean()).reset_index()
yes_grouped = yes_grouped.rename(columns={'AccessOnlineRecord_cat': 'proportion_yes'})

# Plot
chart = alt.Chart(yes_grouped).mark_line().encode(
    x='survey_year:O',  # Treat survey_year as ordinal data
    y=alt.Y('proportion_yes:Q', axis=alt.Axis(format='.0%'), title='Proportion saying Yes'),
    color=f'{group_variable}:N',
    tooltip=[
        alt.Tooltip('survey_year:O', title='Year'),
        alt.Tooltip(f'{group_variable}:N', title=group_variable),
        alt.Tooltip('proportion_yes:Q', title='Proportion saying Yes', format='.0%')
    ]
).properties(
    title=f"Proportion of 'Yes' responses to AccessOnlineRecord_cat over time by {group_variable}",
    width=800
)

st.altair_chart(chart)


x_variable_map = {
    'SpentEnoughTime': 'spend enough time with you?',
    'InvolvedDecisions': 'involve you in decisions about your health care as much as you wanted?',
    'ChanceAskQuestions': 'give you the chance to ask all the health- related questions you had?',
    'FeelingsAddressed': 'give the attention you needed to your feelings and emotions?',
    'UnderstoodNextSteps': 'make sure you understood the things you needed to do to take care of your health?',
    'HelpUncertainty': 'help you deal with feelings of uncertainty about your health or health care?',
    'ExplainedClearly': 'explain things in a way you could understand?'
}

spent_enough_time_order = ['Never', 'Sometimes', 'Usually', 'Always']


st.markdown("""
### Part 2: Relationship between access of patient portals and patient provider communication
Previous research suggests a potential correlation between effective patient-doctor communication and increased utilization of patient portals. Consequently, the subsequent phase of this project aims to explore the relationship between patient portal usage and patient-provider communication.

To assess patient-provider communication, respondents were asked seven questions reflecting their experiences over the past 12 months. Participants indicated their level of agreement using a four-point scale: always, usually, sometimes, never. The questions addressed whether health professionals:

• Allowed patients to ask all health-related questions they had.
• Attended to their feelings and emotions adequately.
• Involved them in health care decisions to the desired extent.
• Ensured their understanding of health care instructions.
• Explained concepts in comprehensible terms.
• Spent sufficient time with them.
• Assisted them in navigating feelings of uncertainty about health matters.

Subsequently, the distribution of respondents across different frequency categories for patient portal access (None, 1-2, 3-5, 6-9, or 10 or more times) was plotted against each response category (always, usually, sometimes, never) for the patient-provider communication questions.

From the data, a trend emerged: the proportion of participants who reported no portal access decreased, while portal access increased when moving from the "Never" to the "Always" response for each patient-provider communication question. This suggests that enhanced communication between patients and doctors potentially boosts patients' willingness and capability to use portals.    
""")

# Use the questions in the dropdown
selected_question = st.selectbox(
    "Choose the variable to group by: In the past 12 months how often did your doctors, nurses, or other health professionals...",
    list(x_variable_map.values())
)

# Get the actual column name based on the selected question
x_variable = [col for col, question in x_variable_map.items() if question == selected_question][0]


# Dropdown to select the year
selected_year = st.selectbox("Choose the year for plot 3:", [2017, 2019, 2020, 2022])

# Subset the dataframe for the specific year
year_subset = combined_df[combined_df['survey_year'] == selected_year]

# Calculate proportions
grouped_df = year_subset.groupby([x_variable, 'AccessOnlineRecord_cat_2']).size().reset_index(name='counts')
total = year_subset.groupby(x_variable).size().reset_index(name='total')
grouped_df = grouped_df.merge(total, on=x_variable)
grouped_df['proportion'] = grouped_df['counts'] / grouped_df['total']

# Define your custom orders here
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
### Part 3: Disparities in patient provider communication
From our findings in phase 1, we understand that disparities exist in portal access, and from phase 2, we have discerned a relationship between portal access and patient-provider communication. In the third phase of the project, we aim to investigate whether demographics that found it challenging to access portals also experienced lower levels of patient-provider communication. If this is true, enhancing patient-provider communication for these demographics could potentially boost their portal access.

The data visualizations indicate that Hispanics and those without health insurance tend to report "never" more frequently (and "always" less frequently) in response to several patient-provider communication questions. This suggests that these demographics might be experiencing subpar patient-provider communication. Therefore, one could hypothesize that this insufficient communication is a factor in their decreased use of portals. While this is not a conclusive observation, it's an aspect that warrants deeper exploration.  
""")

selected_group = st.selectbox(
    "Choose the variable to group by for final plot:",
    list(column_map.values())
)

# Dropdown to select the year
selected_year_2 = st.selectbox("Choose the year for final plot:", [2017, 2019, 2020, 2022])


group_variable_new = [col for col, label in column_map.items() if label == selected_group][0]

selected_x_question_new = st.selectbox(
    "Choose the x variable: In the past 12 months how often did your doctors, nurses, or other health professionals...:",
    list(x_variable_map.values())
)

x_variable_new = [col for col, question in x_variable_map.items() if question == selected_x_question_new][0]

# Calculate data for the new plot
year_subset = combined_df[combined_df['survey_year'] == selected_year_2]
grouped_df_new = year_subset.groupby([group_variable_new, x_variable_new]).size().reset_index(name='counts')
total_new = year_subset.groupby(group_variable_new).size().reset_index(name='total')
grouped_df_new = grouped_df_new.merge(total_new, on=group_variable_new)
grouped_df_new['proportion'] = grouped_df_new['counts'] / grouped_df_new['total']

# Base chart for the new plot
base_new = alt.Chart(grouped_df_new).mark_bar().encode(
    x=alt.X(f'{x_variable_new}:N', sort=spent_enough_time_order, title=None),  # Remove title here
    y=alt.Y('proportion:Q', axis=alt.Axis(format='%')),
    color=f'{x_variable_new}:N',
    tooltip=[group_variable_new, x_variable_new, 'proportion']
).properties(
    width=100
)

# Facet the new chart
chart_new = base_new.facet(
    column=alt.Column(f'{group_variable_new}:N', sort=spent_enough_time_order, header=alt.Header(labelOrient="top", title=f"{x_variable_new}", titleOrient="bottom")),  # Adjust the title here
    spacing=15
).resolve_scale(
    x='shared'
).properties(
    title=f"Proportion of each option in '{x_variable_new}' by '{group_variable_new}' for the year {selected_year_2}"
)

st.altair_chart(chart_new)


st.markdown("""

## Conclusion

In the era of digital health and telemedicine, comprehending the nuances of how patients access online portals is pivotal. Our project illuminated clear disparities in portal access and underscored a distinct relationship between this access and the quality of patient-provider communication. Notably, specific demographics, like Hispanics and those without health insurance, showcased both reduced portal access and subpar patient-provider communication. Policies aimed at bolstering patient-provider communication for these groups might offer a tangible solution to bridge these disparities in portal access. This project emphasizes the need for equal access to health technologies and promotes optimal health outcomes for all.
""")