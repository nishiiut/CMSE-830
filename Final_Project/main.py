# Import necessary libraries
import streamlit as st
import pandas as pd
import altair as alt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import os


# Set page title
st.title("Gene Expression Analysis App")

# Create tabs for different sections
tab1, tab2, tab3, tab4 = st.tabs(["Introduction", "Explore Data", "Compare Data", "About Me"])

# Introduction Tab
with tab1:
    st.markdown("""
        # What is RNA?
        RNA, or ribonucleic acid, is a fundamental molecule in biology, vital for coding, decoding, regulation, and expression of genes. It acts as a messenger carrying instructions from DNA for controlling the synthesis of proteins. Unlike DNA, RNA is single-stranded and can fold into complex 3D structures. This flexibility allows RNA to perform various roles in the cell, including acting as a template for protein synthesis and regulating gene expression.

        # What is RNA-Seq?
        RNA sequencing (RNA-seq) is a next-generation sequencing (NGS) method used to study the quantity and sequences of RNA in a sample. It provides insights into the cellular transcriptome, actively expressed genes at a given moment. This method is crucial for understanding gene expression patterns and alterations in different conditions, such as disease states or environmental changes.
        RNA-seq lets you capture all of the RNA that is being expressed at any given moment!

        # The Dataset
        "In vitro" refers to studies conducted with microorganisms, cells, or biological molecules outside their normal biological context. These are typically done in controlled laboratory environments, like petri dishes or test tubes.
        "In vivo" studies are carried out in living organisms. These experiments provide a more comprehensive understanding of biological phenomena in the context of the organism's natural environment (in a living organism)
        Having results from both in vitro and in vivo experiments is beneficial as it combines the controlled specificity of in vitro studies with the comprehensive relevance of in vivo studies. This dual approach can validate findings across different levels of biological complexity and enhance the understanding of biological processes.

        ## In Vitro Experimental Design
        This experiment focuses on how adipocytes (fat cells) adapt to cool temperatures in vitro. The design involves exposing mature adipocytes, derived from mesenchymal stem cells (MSCs) of C57BL/6J mice, to 31°C for varying durations (0, 1, or 12 days). The 0-day control group is maintained at 37°C. The purpose is to observe the RNA changes during this adaptation process.
        The raw data for this can be accessed via this link: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE159451

        ## In Vivo Experimental Design
        The in vivo experiment investigates RNA changes in the gluteal portion of the posterior subcutaneous adipose tissue in mice. Mice were housed at 22°C (test condition) or 29°C (control condition). RNA-Seq was performed to compare the RNA profiles under these two temperature conditions.
        The raw data for this can be accessed via this link: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE169142

        In Summary, the in vitro experiment involved exposing cells to a cold condition, and the in vivo experiment involved exposing the mouse to a cold condition.
        
        # Goal:
        The goal of this app is to allow users to explore the RNA-Seq data and compare the results from different experiments. This can help users identify genes of interest and compare their expression levels across different conditions. Users can also compare the expression levels of the same gene across different experiments to see if there are any correlations.

        At its core, the app enables users to compare and contrast RNA-Seq results from different experiments, notably in vitro and in vivo studies. For example, a user might examine how certain genes respond to cooler temperatures in adipose tissue cells in a controlled lab setting (in vitro) and then compare these findings with responses in a living organism (in vivo). Such comparisons are crucial for understanding the broader implications of laboratory findings in real-world biological systems.

        The utility of this app becomes particularly evident when considering its potential to uncover correlations or, intriguingly, discrepancies between in vitro and in vivo data. Imagine a scenario where a gene shows significant upregulation in response to cold in in vitro conditions but exhibits negligible or opposite trends in vivo. This kind of insight can be a gateway to new hypotheses about how certain cellular mechanisms might be influenced by the complex interplay of factors present in a living organism, factors that are absent in a petri dish.

    """)

# Data Exploration Tab
with tab2:
    st.header("Explore Gene Expression Data")

    st.markdown("""
    # What the RNA-seq Dataset Looks Like:
    The dataset consists of four RNA-seq data files, each representing a different experimental comparison. Here's a breakdown of what each file contains:
    1. **RNAseq_mouse_invitro_cold_one_vs_zero:**  
    Comparison: Adipocytes exposed to 31°C for 1 day versus control adipocytes cultured at 37°C.  
    Purpose: To observe early gene expression changes due to a mild temperature drop.  
    2. **RNAseq_mouse_invitro_cold_twelve_vs_one:**  
    Comparison: Adipocytes exposed to 31°C for 12 days versus those exposed for 1 day.  
    Purpose: To study the progression of gene expression changes over a longer cold exposure.  
    3. **RNAseq_mouse_invitro_cold_twelve_vs_zero:**  
    Comparison: Adipocytes exposed to 31°C for 12 days versus control adipocytes at 37°C.  
    Purpose: To identify the cumulative effect of long-term cold exposure on gene expression.  
    4. **RNAseq_mouse_invivo_cold_22_vs_29:**  
    Comparison: Mice housed at 22°C versus those at 29°C.  
    Purpose: To explore in vivo responses of adipose tissue to cooler ambient temperatures.  

    # Differential Expression Analysis
    Each file contains results from differential expression analysis. This analysis identifies genes whose expression levels significantly differ between the experimental and control groups. It's key for understanding how conditions like temperature affect gene activity.

    # Understanding the Data Columns
    Each file includes the following columns:

    1. **Symbol:** The gene symbol, a shorthand notation for the name of the gene being studied.
    2. **baseMean:** The average expression level of the gene across all samples. A higher baseMean indicates higher average expression.
    3. **log2FoldChange:** The logarithm (base 2) of the fold change in gene expression. A positive value indicates upregulation under experimental conditions, while a negative value indicates downregulation.
    4. **padj:** Adjusted p-value. This value accounts for multiple testing corrections, reducing false positives. A lower padj suggests a higher significance of the gene expression change.

    Example Interpretation for the In Vivo Experiment
    Consider the example data for the gene 'Gnai3':  

    1. **Symbol:** Gnai3
    2. **baseMean:** 2045.592068 - This value indicates the average expression level of Gnai3 is relatively high across all samples.
    3. **log2FoldChange:** -0.176436068 - Indicates a slight downregulation of Gnai3 in mice housed at 22°C compared to 29°C.
    4. **padj: 0.12836299** - This adjusted p-value, being higher than typical significance thresholds (e.g., 0.05), suggests that the observed change in Gnai3 expression might not be statistically significant.
    
    """)

    st.markdown("""
    ### Part 1: Select a dataset to explore. Search a gene symbol to see its expression levels.
    """)

    # File selection
    file_option = st.selectbox("Select a CSV file", (
        "RNAseq_mouse_invitro_cold_one_vs_zero.csv",
        "RNAseq_mouse_invitro_cold_twelve_vs_one.csv",
        "RNAseq_mouse_invitro_cold_twelve_vs_zero.csv",
        "RNAseq_mouse_invivo_cold_22_vs_29.csv"
    ))
    
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    # Load data
    df = pd.read_csv(f"{path}/{file_option}").dropna()

    # Search bar for gene symbol
    search_query = st.text_input("Search for a Gene Symbol")

    if search_query:
        # Display search results
        search_results = df[df['Symbol'].str.contains(search_query, case=False, na=False)]
        st.write(search_results)
    else:
        # Pagination for the table
        page_size = 10  # Set the number of rows per page
        page_number = st.number_input(label="Page Number", min_value=1, max_value=(len(df) // page_size) + 1, value=1)
        start_row = (page_number - 1) * page_size
        end_row = start_row + page_size
        st.write(df.iloc[start_row:end_row])

    st.markdown("""
    ### Part 2: Explore plot of the selected data
    Red points represent genes whose expression changes are not statistically significant.
    Blue points represent genes with statistically significant changes in expression (p < 0.05).

    Note: Extreme outliers, especially those in blue, are often the focus of further investigation as they may represent genes with major roles in the response to experimental conditions.

    **We can see how the in vitro results are much cleaner compared to the in vivo results.**
    """)

    # Altair Plotting for significance
    points = alt.Chart(df).mark_point().encode(
        x=alt.X('baseMean:Q', scale=alt.Scale(type='log'), title='log2(Base Mean)'),
        y='log2FoldChange:Q',
        color=alt.condition(
            alt.datum.padj < 0.05, 
            alt.value('blue'),  # Significant points in blue
            alt.value('red')    # Non-significant points in red
        ),
        tooltip=['Symbol:N', 'baseMean:Q', 'log2FoldChange:Q'] 
    ).interactive()

    st.altair_chart(points, use_container_width=True)



# Data Comparison and Linear Regression Tab
with tab3:
    st.header("Compare Two Datasets")

    st.markdown("""
        In order to use the app, select the two data files you would like to compare using linear regression, then click the button "Run Linear Regression". After running you get the following:   
          
        **Mean Squared Error (MSE):** This measures the average of the squares of the errors, i.e., the average squared difference between the estimated values and the actual value. A lower MSE indicates a better fit of the regression model to the data.  
        **R-Squared:** This represents the proportion of the variance for the dependent variable that's explained by the independent variables in the model. A higher R-Squared value indicates a better fit.  
        **Correlation Coefficient (R):** This measures the strength and direction of a linear relationship between two variables. A value close to 1 or -1 indicates a strong linear relationship, while a value around 0 indicates a weak relationship.  
    """)

    # File selection for comparison
    file_option1 = st.selectbox("Select the first CSV file for comparison", (
        "RNAseq_mouse_invitro_cold_one_vs_zero.csv",
        "RNAseq_mouse_invitro_cold_twelve_vs_one.csv",
        "RNAseq_mouse_invitro_cold_twelve_vs_zero.csv",
        "RNAseq_mouse_invivo_cold_22_vs_29.csv"
    ), key='file1')

    file_option2 = st.selectbox("Select the second CSV file for comparison", (
        "RNAseq_mouse_invitro_cold_one_vs_zero.csv",
        "RNAseq_mouse_invitro_cold_twelve_vs_one.csv",
        "RNAseq_mouse_invitro_cold_twelve_vs_zero.csv",
        "RNAseq_mouse_invivo_cold_22_vs_29.csv"
    ), key='file2')

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    # Load data for comparison
    df1 = pd.read_csv(f"{path}/{file_option1}").dropna()
    df2 = pd.read_csv(f"{path}/{file_option2}").dropna()

    # Merge datasets on 'Symbol' for comparison
    merged_df = pd.merge(df1[['Symbol', 'log2FoldChange']], df2[['Symbol', 'log2FoldChange']], on='Symbol', suffixes=('_1', '_2'))

    # Linear Regression and Plot
    if st.button("Run Linear Regression"):
        X = merged_df[['log2FoldChange_1']]
        Y = merged_df['log2FoldChange_2']

        model = LinearRegression().fit(X, Y)
        Y_pred = model.predict(X)

        # Calculating metrics
        mse = mean_squared_error(Y, Y_pred)
        r2 = r2_score(Y, Y_pred)
        r = np.sqrt(r2)

        st.write(f"Mean Squared Error: {mse}")
        st.write(f"R-Squared: {r2}")
        st.write(f"R: {r}")

        # Scatter plot with regression line using Altair
        scatter = alt.Chart(merged_df).mark_point(color='blue').encode(
            x='log2FoldChange_1:Q',
            y='log2FoldChange_2:Q',
        tooltip=['Symbol:N', 'log2FoldChange_1:Q', 'log2FoldChange_2:Q'] 
        )

        regression_line = scatter.transform_regression(
            'log2FoldChange_1', 'log2FoldChange_2', method="linear"
        ).mark_line(color='red')

        st.altair_chart(scatter + regression_line, use_container_width=True)

    st.markdown("""
        The linear regression analysis conducted on various pairings of RNA-seq data from in vitro and in vivo experiments has yielded insights into the correlations between different experimental conditions. The key metrics used in this analysis were Mean Squared Error (MSE), R-Squared, and the correlation coefficient (R).

        **Comparisons:**  

        1. Cold One vs Zero and Cold Twelve vs One: Low correlation (R = 0.1466), suggesting minimal linear relationship.
        2. Cold One vs Zero and Cold Twelve vs Zero: Moderate to high correlation (R = 0.6503). This indicates a more substantial linear relationship, suggesting that the changes from day 1 to day 12 are more linearly related to the initial changes from the control state.
        3. Cold Twelve vs One and Cold Twelve vs Zero: High correlation (R = 0.6561), implying a strong linear relationship between these two conditions.
        4. In Vitro vs In Vivo Comparisons: All comparisons showed very low correlation, with R values ranging from 0.0161 to 0.0650. This indicates a weak linear relationship between in vitro and in vivo datasets.

        **Possible reasons:**  
        * Variability in In Vivo Experiments: The low correlation between in vitro and in vivo results may be attributed to the increased complexity and variability inherent in in vivo conditions. In vivo environments are influenced by a lot of factors that are not present in the controlled in vitro settings.  
        * Linear vs Non-linear Responses: The biological processes and gene expression changes in response to temperature might not always follow linear patterns, especially in the dynamic in vivo environments.


        **Conclusion/Recommendations:**  
        Reassessing the in vivo experimental design to reduce variability and improve the correlation with in vitro results could be beneficial.
        The moderate to high correlations in certain in vitro comparisons suggest specific areas for focused study, especially regarding the adaptive responses of adipocytes to temperature changes.

        The scientists should continue to work with the in vitro results, but should be more skeptical about using the in vivo results. 

        """)

# More Information Tab
with tab4:
    st.markdown("""
        # About Me
        
        Uta Nishii is a first-year Masters student in Data Science at Michigan State University, where she is dedicated to applying her mathematical background to complex business and scientific problems. 
        Her professional goal is to utilize data science in practical, impactful ways, combining her academic knowledge with real-world applications. 

        Outside of her academic pursuits, Uta is actively engaged in hobbies like karate and fashion. In karate, she finds a unique blend of physical skill and mental discipline, viewing it as more than a sport but a way of life that instills resilience and focus.
    """)

