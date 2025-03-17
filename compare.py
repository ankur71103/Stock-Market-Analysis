import streamlit as st 
import pandas as  pd
# import main engine
#from master import quarterly_financials, balance_sheet, cash_flows
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pandas as pd


def quarterly_financials_1(company):
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
        cols = [ 'Sep 2022', 'Dec 2022', 'Mar 2023', 'Jun 2023', 'Sep 2023']  # must be dynamic
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


#  balance sheet

def balance_sheet_1(company):
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
        cols = [  'Mar 2019', 'Mar 2020', 'Mar 2021', 'Mar 2022', 'Mar 2023']  # must be dynamic
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



# CASH FLOW

def cash_flows_1(company):
    url = 'https://ticker.finology.in/company/{}'.format(company)  # Replace this with the target website URL
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if(response.status_code == 200):
        data = BeautifulSoup(response.text, 'html.parser')
        data_extracted = data_extracted = data.find("div",{"class": "innerpagecontent"}).find("div", {"id": "mainContent_cashflows"}).find("table")
        # extracted rows 
        rows = ['Profit from operations ','Adjustment ','Changes in Assets & Liabilities ','Tax Paid ','Operating Cash Flow ','Investing Cash Flow ','Financing Cash Flow ','Net Cash Flow ']
        cols = [  'Mar 2019', 'Mar 2020', 'Mar 2021', 'Mar 2022', 'Mar 2023']  # must be   dynamic
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
def compare_data():
    st.header("Compare the performance of different companies")
    data_company = pd.read_csv('company_list.csv')
    company_1 = st.selectbox('Select the first company', data_company['company_name'])
    company_2 = st.selectbox('Select the second company', data_company['company_name'])

    criteria= st.selectbox('Select the criteria', ["",'income statement', 'balance sheet', 'cash flow'])
    st.write(f'You have selected {company_1} and {company_2} for comparison based on {criteria}')
    if(criteria  == "income statement"):
        df1 = quarterly_financials_1(company_1)
        df2 = quarterly_financials_1(company_2)
        select_criteria =  st.selectbox('Select the criteria',df1.T.columns)
        temp_dataframe = pd.DataFrame()
        temp_dataframe[company_1] = df1.T[select_criteria]
        temp_dataframe[company_2] = df2.T[select_criteria]
    
        if(select_criteria):
            st.line_chart(temp_dataframe[[company_1,company_2]])
        # making visulization
        
    elif(criteria =="balance sheet"):
        df1 = balance_sheet_1(company_1)
        df2 = balance_sheet_1(company_2)

        # making visulization
        select_criteria =  st.selectbox('Select the criteria',df1.T.columns)
        temp_dataframe = pd.DataFrame()
        temp_dataframe[company_1] = df1.T[select_criteria]
        temp_dataframe[company_2] = df2.T[select_criteria]

        if(select_criteria):
            st.line_chart(temp_dataframe[[company_1,company_2]])
    elif(criteria == "cash flow"):
        df1 = cash_flows_1(company_1)
        df2 = cash_flows_1(company_2)
        select_criteria =  st.selectbox('Select the criteria',df1.T.columns)
        temp_dataframe = pd.DataFrame()
        temp_dataframe[company_1] = df1.T[select_criteria]
        temp_dataframe[company_2] = df2.T[select_criteria]
        if(select_criteria):
            st.line_chart(temp_dataframe[[company_1,company_2]])

