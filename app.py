import streamlit as st
import pandas as pd
import requests
import json
from io import StringIO

st.set_page_config(page_title="Get Monthly Search Data", page_icon="📊")

st.title("Get Monthly Search Data")
st.write("Upload your Keywords Everywhere API key and a CSV file containing keywords to get search volume data.")

# API key input
api_key = st.text_input("Enter your Keywords Everywhere API Key:", type="password")

# File uploader
uploaded_file = st.file_uploader("Upload your keywords CSV file", type=['csv'])

def get_keyword_data(keywords, api_key):
    url = "https://api.keywordseverywhere.com/v1/get_keyword_data"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        'country': 'us',
        'currency': 'USD',
        'dataSource': 'gkp',
        'kw[]': keywords
    }
    
    try:
        response = requests.post(url, data=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result['data']
        else:
            st.error(f"Error: {response.json()}")
            return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

if uploaded_file and api_key:
    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        
        # Show column selection
        st.subheader("Select Keyword Column")
        st.write("Please select the column that contains your keywords:")
        
        # Display column names in tabs
        cols = df.columns.tolist()
        selected_column = st.selectbox("Select the column containing keywords:", cols)
        
        # Show preview of selected column
        st.write("Preview of selected column:")
        st.dataframe(df[[selected_column]].head())
        
        keywords = df[selected_column].astype(str).tolist()
        
        if st.button("Get Keyword Data"):
            with st.spinner('Fetching keyword data...'):
                # Initialize progress bar
                progress_bar = st.progress(0)
                total_keywords = len(keywords)
                results = []
                
                # Process keywords in batches with progress updates
                for i in range(0, len(keywords), 100):
                    batch = keywords[i:i + 100]
                    batch_results = get_keyword_data(batch, api_key)
                    
                    if batch_results:
                        results.extend(batch_results)
                    else:
                        st.error("Error occurred while fetching data")
                        break
                    
                    # Update progress bar
                    progress = min(1.0, (i + len(batch)) / total_keywords)
                    progress_bar.progress(progress)
                
                if results:
                    # Create DataFrame from results
                    output_data = []
                    for item in results:
                        output_data.append({
                            'Keyword': item['keyword'],
                            'Search Volume': item['vol'],
                            'CPC ($)': item['cpc']['value'],
                            'Competition': item['competition']
                        })
                    
                    result_df = pd.DataFrame(output_data)
                    
                    # Display results
                    st.subheader("Results")
                    st.dataframe(result_df)
                    
                    # Download button
                    csv = result_df.to_csv(index=False)
                    st.download_button(
                        label="Download Results as CSV",
                        data=csv,
                        file_name="keyword_volume_results.csv",
                        mime="text/csv"
                    )
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

st.markdown("---")
st.markdown("""
### Instructions:
1. Enter your Keywords Everywhere API key
2. Upload a CSV file containing keywords (one keyword per row)
3. Select the column containing keywords
4. Click 'Get Keyword Data' to fetch the search volume data
5. Download the results as a CSV file
""")
