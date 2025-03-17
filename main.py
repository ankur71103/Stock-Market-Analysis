import streamlit as  st  
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

def financial_ratio(url):
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    
    
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
            
            return BeautifulSoup(response.text, 'html.parser')
            # Print the content of the response
            
    else:
            
        print(f'Request failed with status code: {response.status_code}')

def final_ratio(url):
     testing_page_1 = financial_ratio(url)  # this  is company main web page
     ''' 
     for i in test.find_all('li'):
    temp_link = i.find("a")
    if(temp_link != None):
        title = temp_link.get("title")
        if(title == "Ratios"):
            print(temp_link.get("href"))
     '''
     signal = 0
     for i in testing_page_1.find_all("li"):  #type: ignore
          temp_link = i.find("a")
          if(temp_link != None):
               title = temp_link.get("title")
               if(title == "Ratios" and signal == 0):
                    testing_page = financial_ratio(temp_link.get("href"))
                    signal = 1
                    

     target_table = testing_page.find_all("table") #type: ignore
     columns = []
     data = []
     index = []
     for i in target_table[1].find_all("td"):
          target_text = i.text
          if("Mar " in target_text):
               columns.append(target_text)

          elif(target_text != "" and target_text.isprintable()):  # type: ignore
               try:
                    target_text = target_text.replace(",","")
                    alfa = float(target_text)
                    data.append(alfa)
               except:
                if target_text not in ['Per Share Ratios','Profitability Ratios','Liquidity Ratios','Valuation Ratios']:
                     index.append(target_text)
     final_data_list = []
     len_1 = len(columns)
     temp_data = []
     len_2 = 0
     for i in data:
          temp_data.append(i)
          len_2 += 1
          if(len_2 == len_1):
               final_data_list.append(temp_data)
               temp_data = []
               len_2 = 0
     dummy = pd.DataFrame(final_data_list, columns = columns,index = index[1:])
     return dummy


@st.cache_data
def get_data():
    data = pd.read_csv('financial_ratio.csv')
    return data

data = get_data()
def main_ratios():
    st.title('Financial Ratio')
    company_name = st.selectbox('Select Company', data['company_name'])

    if(company_name != ''):
        url = get_data()[get_data()['company_name'] == company_name]['company_link'].values[0]
        datafame_1 = final_ratio(url)
        st.dataframe(datafame_1,width = 900, height=1300,use_container_width=True,hide_index=False)
    
    # visulization part 
    st.title('Financial Ratio Visualization')
    dataframe_1_transposed = datafame_1.T  #type: ignore
    finance_ratios = st.selectbox("Select ratio",dataframe_1_transposed.columns)
    st.bar_chart(dataframe_1_transposed[finance_ratios])

    # multi-chart visulization
    st.title('Financial Ratio Visualization (Multi-Chart)')
    finance_ratios_1 = st.multiselect("Select ratio",dataframe_1_transposed.columns)
    st.line_chart(dataframe_1_transposed[finance_ratios_1])
    

    



