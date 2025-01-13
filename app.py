import streamlit as st
import pandas as pd
import requests
import json
from io import StringIO

st.set_page_config(page_title="Keyword Volume Analyzer", page_icon="📊")

st.title("Keyword Volume Analyzer")
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
    
    # Ensure we don't exceed 100 keywords per request
    max_keywords = 100
    all_results = []
    
    for i in range(0, len(keywords), max_keywords):
        batch = keywords[i:i + max_keywords]
        data = {
            'country': 'us',
            'currency': 'USD',
            'dataSource': 'gkp',
            'kw[]': batch
        }
        
        try:
            response = requests.post(url, data=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                all_results.extend(result['data'])
            else:
                st.error(f"Error: {response.json()}")
                return None
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None
    
    return all_results

if uploaded_file and api_key:
    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        
        # Check if there's a column with keywords
        if len(df.columns) > 0:
            # Assume first column contains keywords if column name not found
            keyword_column = df.columns[0]
            keywords = df[keyword_column].astype(str).tolist()
            
            if st.button("Get Keyword Data"):
                with st.spinner('Fetching keyword data...'):
                    results = get_keyword_data(keywords, api_key)
                    
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
        else:
            st.error("The uploaded CSV file appears to be empty.")
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")

st.markdown("---")
st.markdown("""
### Instructions:
1. Enter your Keywords Everywhere API key
2. Upload a CSV file containing keywords (one keyword per row)
3. Click 'Get Keyword Data' to fetch the search volume data
4. Download the results as a CSV file
""")
