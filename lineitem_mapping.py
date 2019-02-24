import pandas as pd
import re
import MoneyControl_Scrape as mcs
import requests
import os


def get_annual_data(isin, bse,nse):
	df = mcs.merge_profit_loss_balance_sheet(isin, bse,nse)
	return df


def create_new_dataframe():
	df = pd.DataFrame(columns=['CO_NAME', 'Annual_Quarter', 'Quarter_Period', 'Year_End'])
	# df['CO_NAME'] = company_name
	return df


def line_item_mapping(df, df1, company_name):

	df1['Year_End'] = df['Year_End']

	df1['CO_NAME'] = company_name

	for i in range(len(df1['Year_End'])):
		df1['Year_End'][i] = '20'+ df1['Year_End'][i].split(" ")[1]

	try:
		df1['Annual_Quarter'] = "A"
	except:
		df1['Annual_Quarter'] = 0.01

	try:
		df1['Quarter_Period'] = ""
	except:
		df1['Quarter_Period'] = 0.01

	try:
		df['Hybrid/Debt/Other Securities'] = df['Hybrid/Debt/Other Securities']
	except:
		df['Hybrid/Debt/Other Securities'] = 0

	df1['DM_STOCKHOLDER_EQUITY'] = df['Total Share Capital'].astype('float') + df['Hybrid/Debt/Other Securities'].astype('float')


	try:
		df1['DM_RESERVES'] = df['Total Reserves and Surplus']
	except:
		df1['DM_RESERVES'] = 0.01

	try:
		df1['DM_TOTAL_EQUITY'] = df['Total Shareholders Funds']
	except:
		df1['DM_TOTAL_EQUITY'] = 0.01


	try:
		df1['DM_SENIOR_LONG_TERM_DEBT'] = df['Long Term Borrowings']
	except:
		df1['DM_SENIOR_LONG_TERM_DEBT'] = 0.01

	try:
		df['Other Long Term Liabilities'] = df['Other Long Term Liabilities']
	except:
		df['Other Long Term Liabilities'] = 0.01

	try:
		df['Deferred Tax Liabilities [Net]'] = df['Deferred Tax Liabilities [Net]']
	except:
		df['Deferred Tax Liabilities [Net]'] = 0.01

	df1['DM_OTR_LONG_TERM_LIAB'] = df['Other Long Term Liabilities'].astype('float') + df['Deferred Tax Liabilities [Net]'].astype('float')

	try:
		df1['DM_SHORT_TERM_BORROWINGS'] = df['Short Term Borrowings']
	except:
		df1['DM_SHORT_TERM_BORROWINGS'] = 0.01

	try:
		df1['DM_ACCOUNTS_PAYABLE'] = df['Trade Payables']
	except:
		df1['DM_ACCOUNTS_PAYABLE'] = 0.01


	try:
		df1['DM_OTHER_CURRENT_LIABILITIES'] = df['Other Current Liabilities']
	except:
		df1['DM_OTHER_CURRENT_LIABILITIES'] = 0.01

	try:
		df1['DM_TOTAL_CURRENT_LIABILITIES'] = df['Total Current Liabilities']
	except:
		df1['DM_TOTAL_CURRENT_LIABILITIES'] = 0.01

	try:
		df['Total Non0Current Liabilities'] = df['Total Non0Current Liabilities']
	except:
		df['Total Non0Current Liabilities'] = 0.01

	df1['DM_TOTAL_LIABILITIES'] = df['Total Non0Current Liabilities'].astype('float')+df1['DM_TOTAL_CURRENT_LIABILITIES'].astype('float')

	try:
		df1['DM_TOT_LIAB_N_EQ'] = df['Total Capital And Liabilities']
	except:
		df1['DM_TOT_LIAB_N_EQ'] = 0.01

	try:
		df['Tangible Assets'] = df['Tangible Assets'].astype('float')
	except:
		df['Tangible Assets'] = 0 
	try:
		df['Capital Work0In0Progress'] = df['Capital Work0In0Progress']
	except:
		df['Capital Work0In0Progress'] = 0

	print("Capital Work0In0Progress =====================================", df['Capital Work0In0Progress'])


	df1['DM_NET_PROP_PLANT_EQUIP'] = df['Tangible Assets'].astype('float') + df['Capital Work0In0Progress'].astype('float')


	try:
		df['Intangible Assets'] = df['Intangible Assets']
	except:
		df['Intangible Assets'] = 0

	try:
		df['Intangible Assets Under Development'] = df['Intangible Assets Under Development']
	except:
		df['Intangible Assets Under Development'] = 0


	print("Intangible Assets Under Development =====================================", df['Intangible Assets Under Development'])


	df1['DM_GW_OTR_INTANGIBLES'] = df['Intangible Assets'].astype('float') + df['Intangible Assets Under Development'].astype('float')


	try:
		df['Non0Current Investments'].astype('float') = df['Non0Current Investments'].astype('float')
	except:
		df['Non0Current Investments'].astype('float') = 0

	df1['DM_OTHER_ASSETS'] = df['Non0Current Investments'].astype('float') + df1['Other Assets'].astype('float')

	# try:
	# 	df1['DM_OTHER_ASSETS'] = df['Non0Current Investments']
	# except:
	# 	df1['DM_OTHER_ASSETS'] = 0.01

	try:
		df1['DM_EQ_INV_N_OTR_INV'] = df['Long Term Loans And Advances']
	except:
		df1['DM_EQ_INV_N_OTR_INV'] = 0.01

	try:
		df1['DM_INVENTORY'] = df['Inventories']
	except:
		df1['DM_INVENTORY'] = 0.01

	try:
		df1['DM_TOTAL_RECEIVABLES'] = df['Trade Receivables']
	except:
		df1['DM_TOTAL_RECEIVABLES'] = 0.01

	try:
		df1['DM_TOTAL_CASH_ST_INV'] = df['Cash And Cash Equivalents']
	except:
		df1['DM_TOTAL_CASH_ST_INV'] = 0.01

	try:
		df['OtherCurrentAssets'] = df['OtherCurrentAssets']
	except:
		df['OtherCurrentAssets'] = 0.01

	try:
		df['Current Investments'] = df['Current Investments']
	except:
		df['Current Investments'] = 0.01

	try:
		df['Short Term Loans And Advances'] = df['Short Term Loans And Advances']
	except:
		df['Short Term Loans And Advances'] = 0

	print("Short Term Loans And Advances==========================>", df['Short Term Loans And Advances'])

	df1['DM_OTHER_CURRENT_ASSETS'] = df['OtherCurrentAssets'].astype('float') + df['Current Investments'].astype('float') + df['Short Term Loans And Advances'].astype('float')
	
	try:
		df1['DM_TOTAL_CURRENT_ASSETS'] = df['Total Current Assets']
	except:
		df1['DM_TOTAL_CURRENT_ASSETS'] = 0.01

	try:
		df1['DM_TOTAL_ASSETS'] = df['Total Assets']
	except:
		df1['DM_TOTAL_ASSETS'] = 0.01


	try:
		df1['DM_TOTAL_REVENUES'] = df['Total Revenue']
	except:
		df1['DM_TOTAL_REVENUES'] = 0.01

	try:
		df1['DM_COST_OF_GOODS_SOLD'] = df['Cost Of Materials Consumed']
	except:
		df1['DM_COST_OF_GOODS_SOLD'] = 0.01

	try:
		df['Employee Benefit Expenses'] = df['Employee Benefit Expenses']
	except:
		df['Employee Benefit Expenses'] = 0.01

	try:
		df['Operating And Direct Expenses'] = df['Operating And Direct Expenses']
	except:
		df['Operating And Direct Expenses'] = 0.01

	df1['DM_SGA'] = df['Operating And Direct Expenses'].astype('float') + df['Employee Benefit Expenses'].astype('float')

	try:
		df1['DM_GROSS_INTEREST_EXPENSE'] = df['Finance Costs']
	except:
		df1['DM_GROSS_INTEREST_EXPENSE'] = 0.01

	try:
		df1['DM_DEPR_AMORT'] = df['Depreciation And Amortisation Expenses']
	except:
		df1['DM_DEPR_AMORT'] = 0.01

	try:
		df1['DM_OTR_OPERATING_EXP_INC'] = df['Other Expenses']
	except:
		df1['DM_OTR_OPERATING_EXP_INC'] = 0.01


	try:
		df['Cost Of Materials Consumed'] = df['Cost Of Materials Consumed']
	except:
		df['Cost Of Materials Consumed'] = 0

	try:
		df['Operating And Direct Expenses'] = df['Operating And Direct Expenses']
	except:
		df['Operating And Direct Expenses'] = 0

	try:
		df['Employee Benefit Expenses'] = df['Employee Benefit Expenses']
	except:
		df['Employee Benefit Expenses'] = 0

	try:
		df['Finance Costs'] = df['Finance Costs']
	except:
		df['Finance Costs'] = 0

	try:
		df['Depreciation And Amortisation Expenses'] = df['Depreciation And Amortisation Expenses']
	except:
		df['Depreciation And Amortisation Expenses'] = 0

	try:
		df['Other Expenses'] = df['Other Expenses']
	except:
		df['Other Expenses'] = 0

	try:
		df['Less: Amounts Transfer To Capital Accounts'] = df['Less: Amounts Transfer To Capital Accounts']
	except:
		df['Less: Amounts Transfer To Capital Accounts'] = 0

	try:
		df['Purchase Of Stock-In Trade'] = df['Purchase Of Stock-In Trade']
	except:
		df['Purchase Of Stock-In Trade'] = 0

	try:
		df['Changes In Inventories Of FG/WIP And Stock0In Trade'] = df['Changes In Inventories Of FG/WIP And Stock0In Trade']
	except:
		df['Changes In Inventories Of FG/WIP And Stock0In Trade'] = 0

	df1['DM_TOTAL_OPERATING_EXPENSES'] = df['Cost Of Materials Consumed'].astype('float') + df['Operating And Direct Expenses'].astype('float') + df['Employee Benefit Expenses'].astype('float') + df['Finance Costs'].astype('float') + df['Depreciation And Amortisation Expenses'].astype('float') + df['Other Expenses'].astype('float') - df['Less: Amounts Transfer To Capital Accounts'].astype('float') + df['Purchase Of Stock-In Trade'].astype('float') + df['Changes In Inventories Of FG/WIP And Stock0In Trade'].astype('float')

	try:
		df1['DM_INCOME_TAX_EXPENSE'] = df['Total Tax Expenses']
	except:
		df1['DM_INCOME_TAX_EXPENSE'] = 0.01

	try:
		df['Extraordinary Items'] = df['Extraordinary Items']
	except:
		df['Extraordinary Items'] = 0.01

	try:
		df['Exceptional Items'] = df['Exceptional Items']
	except:
		df['Exceptional Items'] = 0.01
	
	df1['DM_CAPTALI'] = df['Exceptional Items'].astype('float') + df['Extraordinary Items'].astype('float')

	try:
		df1['DM_NET_INCOME'] = df['Profit/Loss For The Period']
	except:
		df1['DM_NET_INCOME'] = 0.01

	return df1

def create_csv(df, file):
	df.to_csv(file, index=False)


def store_annual_finance_data(isin, bse,nse, company_name):
	annual_finance = get_annual_data(isin, bse, nse)
	new_dataframe = create_new_dataframe()
	xlrt_template = line_item_mapping(annual_finance, new_dataframe, company_name)
	file = "/home/prm/Desktop/Money_Control_Api/output/"+company_name+".csv"
	create_csv(xlrt_template, file)
	data = {'co_name': company_name}
	response = requests.post('http://192.168.2.119:5000/Test', json=data)	
	if response.text == "Ok":
		# os.remove(file)
		return "Ok"
	else:
		return "Failed"
