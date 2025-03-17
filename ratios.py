import streamlit as st
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import numpy as np 

def cash_flows(company):
    url = 'https://ticker.finology.in/company/{}'.format(company)  # Replace this with the target website URL
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if(response.status_code == 200):
        data = BeautifulSoup(response.text, 'html.parser')
        data_extracted = data_extracted = data.find("div",{"class": "innerpagecontent"}).find("div", {"id": "mainContent_cashflows"}).find("table")
        # extracted rows 
        rows = ['Profit from operations ','Adjustment ','Changes in Assets & Liabilities ','Tax Paid ','Operating Cash Flow ','Investing Cash Flow ','Financing Cash Flow ','Net Cash Flow ']
        cols = [  'Mar 2019', 'Mar 2020', 'Mar 2021', 'Mar 2022', 'Mar 2023']
        # main data
        x_data = data_extracted.find_all("td")
        alfa = []
        temp_file = []
        for i in x_data:
            temp_text = i.text
            temp_text = temp_text.strip()

            #print(temp_text)
            if(temp_text != ''):
                temp_file.append(temp_text)
            if(len(temp_file) == 5):
                alfa.append(temp_file)
                temp_file = []

        #print(alfa)
        dummy = pd.DataFrame(alfa,columns=cols, index =rows)
        return dummy
        
        
        
    else:
        print("Request failed with status code: {}".format(response.status_code))

def balance_sheet(company):
    url = 'https://ticker.finology.in/company/{}'.format(company)  # Replace this with the target website URL
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if(response.status_code == 200):
        data = BeautifulSoup(response.text, 'html.parser')
        data_extracted = data_extracted = data.find("div",{"class": "innerpagecontent"}).find("div", {"id": "balance"}).find("table")
        # extracted rows 
        rows = ['Share Capital ','Total Reserves ','Borrowings ',
                'Other N/C liabilities ','Current liabilities ','Total Liabilities ','Net Block ','Capital WIP ',
                'Intangible WIP ','Investments ','Loans & Advances ','Other N/C Assets ','Current Assets ','Total Assets ']
        cols = [  'Mar 2019', 'Mar 2020', 'Mar 2021', 'Mar 2022', 'Mar 2023']
        # main data
        x_data = data_extracted.find_all("td")
        alfa = []
        temp_file = []
        for i in x_data:
            temp_text = i.text
            temp_text = temp_text.strip()

            #print(temp_text)
            if(temp_text != ''):
                temp_file.append(temp_text)
            if(len(temp_file) == 5):
                alfa.append(temp_file)
                temp_file = []

        #print(alfa)
        dummy = pd.DataFrame(alfa,columns=cols, index =rows)
        return dummy
        
        
        
    else:
        print("Request failed with status code: {}".format(response.status_code))
def quarterly_financials(company):
    url = 'https://ticker.finology.in/company/{}'.format(company)  # Replace this with the target website URL
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if(response.status_code == 200):
        data = BeautifulSoup(response.text, 'html.parser')
        data_extracted = data.find("div",{"class": "innerpagecontent"}).find("div", {"id": "mainContent_quarterly"})\
            .find("div", {"class": "col-12"}).find("div",{"class": "card cardscreen"}).find("table")
        # extracted rows 
        rows = ['Net Sales ','Total Expenditure ','Operating Profit ','Other Income ','Interest ','Depreciation ','Exceptional Items ','Profit Before Tax ','Tax ',
                'Profit After Tax ','Adjusted EPS (Rs) ']
        cols = [ 'Sep 2022', 'Dec 2022', 'Mar 2023', 'Jun 2023', 'Sep 2023']
        # main data
        x_data = data_extracted.find_all("td")
        alfa = []
        temp_file = []
        for i in x_data:
            temp_text = i.text
            temp_file.append(float(temp_text.strip()))
            if(len(temp_file) == 5):
                alfa.append(temp_file)
                temp_file = []
        dummy = pd.DataFrame(alfa,columns=cols, index =rows)
        return dummy
        
        
        
    else:
        print("Request failed with status code: {}".format(response.status_code))
def company_basics(company):

    url = 'https://ticker.finology.in/company/{}'.format(company)
    data_dict = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data_extracted = BeautifulSoup(response.text, 'html.parser')
    text = data_extracted.find("div",{"class": "innerpagecontent"}).find("div", {"id": "mainContent_divCompanyEssentials"}).text
    if response.status_code == 200:
        try:
            market_cap = re.search(r'Market Cap[\s\S]*?₹ ([\d.]+) Cr.', text).group(1)
        except:
            market_cap = None
        
        try:
            enterprise_value = re.search(r'Enterprise Value[\s\S]*?₹ ([\d.]+) Cr.', text).group(1)
        except:
            enterprise_value = None
        
        try:
            no_of_shares = re.search(r'No. of Shares[\s\S]*?([\d.]+) Cr.', text).group(1)
        except:
            no_of_shares = None 
        
        try:
            pe_ratio = re.search(r'P/E[\s\S]*?([\d.]+)', text).group(1)
        except:
            pe_ratio = None
        
        try:
            pb_ratio = re.search(r'P/B[\s\S]*?([\d.]+)', text).group(1)
        except:
            pb_ratio = None
        
        try:
            face_value = re.search(r'Face Value[\s\S]*?₹ (\d+)', text).group(1)
        except:
            face_value = None
        
        try:
            div_yield = re.search(r'Div. Yield[\s\S]*?([\d.]+) %', text).group(1)
        except:
            div_yield = None
        
        try:
            book_value = re.search(r'Book Value \(TTM\)[\s\S]*?₹ ([\d.]+)', text).group(1)
        except:
            book_value = None
        
        try:
            cash = re.search(r'CASH[\s\S]*?₹ ([\d.]+) Cr.', text).group(1)
        except:
            case = None 
        
        try:
            debt = re.search(r'DEBT[\s\S]*?₹ ([\d.]+) Cr.', text).group(1)
        except:
            debt = None
        
        try:
            promoter_holding = re.search(r'Promoter Holding[\s\S]*?(\d+) %', text).group(1)
        except:
            promoter_holding = None
        
        try:
            sales_growth = re.search(r'Sales Growth[\s\S]*?([\d.]+)%', text).group(1)
        except:
            sales_growth = None
        
        try:
            roe = re.search(r'ROE[\s\S]*?([\d.]+) %', text).group(1)
        except:
            roe = None
        try:
            roce = re.search(r'ROCE[\s\S]*?([\d.]+)%', text).group(1)
        except:
            roce = None 
        data_dict = {'market_cap(in Cr.)':market_cap,'enterprise_value (    in Cr.)':enterprise_value,'no_of_shares (in Cr.)':no_of_shares,'pe_ratio':pe_ratio,'pb_ratio':pb_ratio,
                                  'face_value':face_value,'div_yield':div_yield,'book_value (in Rs.)':book_value,'cash(in Cr.)':cash,'debt (in Cr.)':debt,'promoter_holding(%)':promoter_holding,'sales_growth(%)':sales_growth,'roe(%)':roe,'roce(%)':roce}
        print(data_dict)
        alfa = pd.DataFrame()
        alfa['Indicators'] = list(data_dict.keys())
        alfa['Values'] = list(data_dict.values())
        return alfa

        
    else:
        print(f'Request failed with status code: {response.status_code}')
@st.cache_data
def company_list():
    df = pd.read_csv('company_list.csv')
    return df['company_name']

def display_help():
    st.header("Help")
    data_list = [
        ["Market Cap (in Cr.)", "Market Capitalization represents the total value of a company's outstanding shares of stock. It is calculated by multiplying the current market price per share by the total number of outstanding shares.", "Indicates the overall size and worth of a company in the stock market.", "Helps investors assess the company's relative size compared to others in the market."],
        # ... (rest of the data_list)
    ]
    for i in data_list:
        st.subheader(i[0])
        st.write(i[1])
        st.subheader("Importance")
        st.write(i[2])

def download_csv_button(data, file_name):
    st.download_button("Download", data=data.to_csv(index=False), file_name=file_name, mime="text/csv")

def display_financials(company_options, company_basics, quarterly_financials, balance_sheet, cash_flows):
    st.write("https://ticker.finology.in/company/{}".format(company_options))
    company_data = company_basics(company_options)
    st.dataframe(company_data, width=900, height=600)
    download_csv_button(company_data, "{}_basics.csv".format(company_options))

    st.subheader("Quarterly Financials(All Data in Cr.)")
    quarterly_financials_data = quarterly_financials(company_options)
    st.dataframe(quarterly_financials_data, width=900, height=500)
    transposed_dataframe = quarterly_financials_data.T

    st.subheader("Visualization of Financial")
    options = st.selectbox("Select", transposed_dataframe.columns)
    st.bar_chart(transposed_dataframe[options])

    st.subheader("Multi-Chart Visualization")
    options = st.multiselect("Select", transposed_dataframe.columns)
    st.line_chart(transposed_dataframe[options])

    data_balance_sheet = balance_sheet(company_options)
    st.header("Balance Sheet")
    st.dataframe(data_balance_sheet, width=900, height=700)

    st.subheader("Visualization of balance sheet(all data in Cr.)")
    transpose_balance_sheet = data_balance_sheet.T
    options = st.multiselect("Select", transpose_balance_sheet.columns)
    st.line_chart(transpose_balance_sheet[options])

    st.header("Cashflows")
    data_cash_flows = cash_flows(company_options)
    st.dataframe(data_cash_flows, width=900, height=500)

    st.subheader("Visualization of cash flows(all data in Cr.)")
    transpose_cash_flows = data_cash_flows.T
    options = st.multiselect("Select", transpose_cash_flows.columns)
    st.line_chart(transpose_cash_flows[options])

def main():
    company_options = st.selectbox("Company", company_list())
    with st.sidebar:
        st.write("This web app provides state-of-the-art visualization of company financials on a few clicks that other sites do not provide")
        #st.subheader("My Github Account")
        #st.write("https://github.com/innovsm")

    if company_options:
        with st.expander("Help", expanded=False):
            display_help()
        display_financials(company_options, company_basics, quarterly_financials, balance_sheet, cash_flows)

