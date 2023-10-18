import pandas as pd
import numpy as np

# path = "data"

# Read in data
hints5_cycle1_public = pd.read_sas("hints5_cycle1_public.sas7bdat")
hints5_cycle3_public = pd.read_sas("hints5_cycle3_public.sas7bdat")
hints5_cycle4_public = pd.read_sas("hints5_cycle4_public.sas7bdat")
hints6_public = pd.read_sas("hints6_public.sas7bdat")

# Prep data for each survey cycle
hints5_cycle1_public['survey_year'] = 2017
hints5_cycle3_public['survey_year'] = 2019
hints5_cycle4_public['survey_year'] = 2020
hints6_public['survey_year'] = 2022

# Prepare merging of 2017, 2019, 2020, 2022
hints5_cycle1_public_subset = hints5_cycle1_public[['OfferedAccessHCP2', 'AccessOnlineRecord', 'SpentEnoughTime', 'InvolvedDecisions', 'ChanceAskQuestions', 'FeelingsAddressed', 'UnderstoodNextSteps', 'HelpUncertainty', 'ExplainedClearly', 'RaceEthn5', 'GenderC', 'EducA', 'RUC2013', 'QualityCare', 'GeneralHealth', 'Age','FreqGoProvider', 'UseInternet', 'survey_year', 'HealthInsurance']]
hints5_cycle3_public_subset = hints5_cycle3_public[['OfferedAccessHCP2', 'AccessOnlineRecord', 'SpentEnoughTime', 'InvolvedDecisions', 'ChanceAskQuestions', 'FeelingsAddressed', 'UnderstoodNextSteps', 'HelpUncertainty', 'ExplainedClearly', 'RaceEthn5', 'GenderC', 'EducA', 'RUC2013', 'QualityCare', 'GeneralHealth', 'Age', 'FreqGoProvider', 'UseInternet', 'survey_year', 'HealthInsurance']]
hints5_cycle4_public_subset = hints5_cycle4_public[['OfferedAccessHCP2', 'AccessOnlineRecord', 'SpentEnoughTime', 'InvolvedDecisions', 'ChanceAskQuestions', 'FeelingsAddressed', 'UnderstoodNextSteps', 'HelpUncertainty', 'ExplainedClearly', 'RaceEthn5', 'BirthGender', 'EducA', 'RUC2013', 'QualityCare', 'GeneralHealth', 'Age', 'FreqGoProvider', 'UseInternet', 'survey_year', 'HealthInsurance']]
hints6_public_subset = hints6_public[['OfferedAccessHCP3', 'AccessOnlineRecord2', 'SpentEnoughTime', 'InvolvedDecisions', 'ChanceAskQuestions', 'FeelingsAddressed', 'UnderstoodNextSteps', 'HelpUncertainty', 'ExplainedClearly', 'RaceEthn5', 'BirthGender', 'EducA', 'RUC2013', 'QualityCare', 'GeneralHealth', 'Age', 'FreqGoProvider', 'UseInternet', 'survey_year', 'HealthInsurance2']]

# Rename column names as necessary
hints5_cycle1_public_subset = hints5_cycle1_public_subset.rename(columns={'GenderC': 'BirthGender'})
hints5_cycle3_public_subset = hints5_cycle3_public_subset.rename(columns={'GenderC': 'BirthGender'})
hints6_public_subset = hints6_public_subset.rename(columns={
    'OfferedAccessHCP3': 'OfferedAccessHCP2',
    'AccessOnlineRecord2': 'AccessOnlineRecord',
    'HealthInsurance2': 'HealthInsurance'
})

# AccessOnlineRecord make "5" None
hints6_public_subset['AccessOnlineRecord'] = hints6_public_subset['AccessOnlineRecord'].replace(5, -9)

# Create list of dataframes
dataframe_subsets = [hints5_cycle1_public_subset, hints5_cycle3_public_subset, hints5_cycle4_public_subset, hints6_public_subset]

# Define list of numbers to replace with NA (using None for NA in Python)
na_list = [-1, -2, -4, -5, -6, -7, -9]

# Define function to replace values with NA
def replace_with_na(df):
    for i in na_list:
        df = df.replace(i, None)
    return df

# Apply function to each dataframe in the list
dataframe_subsets = [replace_with_na(df) for df in dataframe_subsets]

# Use concat to combine all dataframes
combined_df = pd.concat(dataframe_subsets, ignore_index=True)

cols_to_convert = ["SpentEnoughTime", "InvolvedDecisions", "ChanceAskQuestions", "FeelingsAddressed", "UnderstoodNextSteps", "HelpUncertainty", "ExplainedClearly"]

# Create new column names with "_invert" suffix
new_cols = [col + "_invert" for col in cols_to_convert]

for old_col, new_col in zip(cols_to_convert, new_cols):
    combined_df[new_col] = 5 - combined_df[old_col]


# Calculate mean for each row if at least half of the variables have valid values
def calculate_mean(row):
    valid_values = row.dropna()
    if len(valid_values) >= len(row) / 2:
        return valid_values.mean()
    else:
        return None

combined_df['PCCScale_calc'] = combined_df[new_cols].apply(calculate_mean, axis=1)

# Subtract the minimum value of the new scale
combined_df['PCCScale_calc'] -= 1

# Multiply by the scaling factor
combined_df['PCCScale_calc'] *= (100 / 3)  # The factor is 100/3 for converting 1-4 scale to 0-100

# Replace missing PCCScale values with NA (equivalent to None in Python)
# combined_df['PCCScale_calc'].fillna(-9, inplace=True)

# Convert specific columns back to categorical type
for col in cols_to_convert:
    combined_df[col] = combined_df[col].astype('category')

# rename column levels
combined_df["AccessOnlineRecord_cat"] = combined_df["AccessOnlineRecord"].replace({0: "None", 1: "Yes", 2: "Yes", 3: "Yes", 4: "Yes", 5: "No"})
combined_df["AccessOnlineRecord_cat_2"] = combined_df["AccessOnlineRecord"].replace({0: "None", 1: "1 to 2 times", 2: "3 to 5 times", 3: "6 to 9 times", 4: "10 or more times"})
combined_df["OfferedAccessHCP2"] = combined_df["OfferedAccessHCP2"].replace({1: "Yes", 2: "No", 3: "No"})
combined_df["RaceEthn5"] = combined_df["RaceEthn5"].replace({1: "Non-Hispanic White", 2: "Non-Hispanic Black", 3: "Hispanic", 4: "Asian", 5: "Other"})
combined_df["BirthGender"] = combined_df["BirthGender"].replace({1: "Male", 2: "Female"})
combined_df["EducA"] = combined_df["EducA"].replace({1: "High School or Less", 2: "High School or Less", 3: "Some College", 4: "College Graduate or More"})
combined_df["RUC2013"] = combined_df["RUC2013"].replace({1: "Metro", 2: "Metro", 3: "Metro", 4: "Nonmetro", 5: "Nonmetro", 6: "Nonmetro", 7: "Nonmetro", 8: "Nonmetro", 9: "Nonmetro"})
combined_df["QualityCare"] = combined_df["QualityCare"].replace({1: "5", 2: "4", 3: "3", 4: "2", 5: "1"})
combined_df["GeneralHealth"] = combined_df["GeneralHealth"].replace({1: "Excellent, Very good, Good", 2: "Excellent, Very good, Good", 3: "Excellent, Very good, Good", 4: "Fair, Poor", 5: "Fair, Poor"})
combined_df["UseInternet"] = combined_df["UseInternet"].replace({1: "Yes", 2: "No"})
combined_df["SpentEnoughTime"] = combined_df["SpentEnoughTime"].replace({1: "Always", 2: "Usually", 3: "Sometimes", 4: "Never"})
combined_df["InvolvedDecisions"] = combined_df["InvolvedDecisions"].replace({1: "Always", 2: "Usually", 3: "Sometimes", 4: "Never"})
combined_df["ChanceAskQuestions"] = combined_df["ChanceAskQuestions"].replace({1: "Always", 2: "Usually", 3: "Sometimes", 4: "Never"})
combined_df["FeelingsAddressed"] = combined_df["FeelingsAddressed"].replace({1: "Always", 2: "Usually", 3: "Sometimes", 4: "Never"})
combined_df["UnderstoodNextSteps"] = combined_df["UnderstoodNextSteps"].replace({1: "Always", 2: "Usually", 3: "Sometimes", 4: "Never"})
combined_df["HelpUncertainty"] = combined_df["HelpUncertainty"].replace({1: "Always", 2: "Usually", 3: "Sometimes", 4: "Never"})
combined_df["ExplainedClearly"] = combined_df["ExplainedClearly"].replace({1: "Always", 2: "Usually", 3: "Sometimes", 4: "Never"})
combined_df["HealthInsurance"] = combined_df["HealthInsurance"].replace({1: "Yes", 2: "No"})

# Replace NA values (which will now be the string 'nan') with "Missing"
combined_df['RaceEthn5'] = combined_df['RaceEthn5'].astype(str)
combined_df['RaceEthn5'].replace('None', 'Missing', inplace=True)

# Create age_cat column
conditions = [
    (combined_df['Age'] >= 18) & (combined_df['Age'] <= 30),
    (combined_df['Age'] >= 31) & (combined_df['Age'] <= 40),
    (combined_df['Age'] >= 41) & (combined_df['Age'] <= 50),
    (combined_df['Age'] >= 51) & (combined_df['Age'] <= 64),
    (combined_df['Age'] >= 65)
]
choices = ['18-30', '31-40', '41-50', '51-64', '65 or older']
combined_df['age_cat'] = pd.Categorical(pd.Series(np.select(conditions, choices, default=np.nan)))

# Remove rows containing NaN or None values
combined_df_cleaned = combined_df.dropna()

# Reset the index after dropping rows, if needed
combined_df_cleaned.reset_index(drop=True, inplace=True)
