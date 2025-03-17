import streamlit as st
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import numpy as np 
from ratios import main
from main import main_ratios
from compare import compare_data
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


data_1 = st.radio("Select", ("company financials", "company ratios", "compare companies"))
if(data_1 == "company financials"):
    try:
        main()
    except:
        st.error("Internal Error")
elif(data_1 == "company ratios"):
    try:
        main_ratios()
    except:
        st.error("Internal Error")
else:
    try:
        compare_data()
    except Exception as  e:
        st.error(e)

