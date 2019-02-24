import pandas as pd
from bs4 import BeautifulSoup
import requests, copy, re


def money_control_base_url(search_key):
	url = "http://www.moneycontrol.com/stocks/cptmarket/compsearchnew.php?search_data=&cid=&mbsearch_str=&topsearch_type=1&search_str="+str(search_key)
	return url


def get_all_link(key):
	
	url = money_control_base_url(key)
	response = get_response(url)
	soup = parse_response_to_text(response)
	link = str(soup.find('link'))
	return link


def get_search_string(isin,bse,nse):
	link = get_all_link(isin)

	if 'stockpricequote' in link:
		return link
	else:
		link = get_all_link(bse)
		if 'stockpricequote' in link:
			return link
		else:
			link = get_all_link(nse)
			return link


def get_search_key(search_string):
	sort = re.search('stockpricequote/(.+?)" rel', search_string).group(1)
	key = sort.split('/')[2]
	return key


def profit_loss_url(search_key):
	url = 'https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did=' + str(search_key) + '&type=profit_VI'
	return url


def balance_sheet_url(search_key):
	url = 'https://www.moneycontrol.com/stocks/company_info/print_financials.php?sc_did='+str(search_key)+'&type=balance_VI'
	return url

def get_response(url):
	response = requests.get(url)
	return response


def parse_response_to_text(response):
	soup = BeautifulSoup(response.text, 'html.parser')
	return soup


def get_rows(soup):
	data = soup.find_all('table', {'class': 'table4'})
	rows = data[2].find_all('tr')
	final_rows = []
	flag = 1
	while flag == 1:
		flag = 0
		final_rows = []
		for row in rows:
			if row.find('tr'):
				flag = 1
				inner_rows = row.find_all('tr')
				for inner_row in inner_rows:
					final_rows.append(inner_row)
			else:
				final_rows.append(row)

		rows = copy.copy(final_rows)
	# print final_rows
	rows = []
	return final_rows


def strip_data(rows):
	striped_data = []
	# m.append("y")
	for i in range(0, len(rows)):
		if rows[i]['height'] == '1px':
			break

		fields = rows[i].find_all('td')

		fields[0] = re.sub(',', '/', fields[0].get_text())
		for i in range(1, len(fields)):
			fields[i] = re.sub(',', '', fields[i].get_text())
		for each in fields[0:]:
		   striped_data.append(each.strip())

	return striped_data


def remove_null(striped_data):
	str_list = list(filter(None, striped_data))
	return str_list


def remove_strings_from_profit_loss():
	removeString = ["12 mths", "INCOME", "EXPENSES", "12 mths", "Tax Expenses-Continued Operations", "12 mths",
					"OTHER ADDITIONAL INFORMATION", "EARNINGS PER SHARE",
					"VALUE OF IMPORTED AND INDIGENIOUS RAW MATERIALS", "STORES, SPARES AND LOOSE TOOLS",
					"STORES/ SPARES AND LOOSE TOOLS", "DIVIDEND AND DIVIDEND PERCENTAGE",
					"Source : Dion Global Solutions Limited"]
	return removeString


def remove_strings_from_balancesheet():
	remove_string = ["12 mths", "EQUITIES AND LIABILITIES", "SHAREHOLDER'S FUNDS", "ASSETS", "NON-CURRENT LIABILITIES",
					"CURRENT LIABILITIES", "NON-CURRENT ASSETS", "CURRENT ASSETS", "OTHER ADDITIONAL INFORMATION",
					"CONTINGENT LIABILITIES/ COMMITMENTS", "CIF VALUE OF IMPORTS", "EXPENDITURE IN FOREIGN EXCHANGE",
					"REMITTANCES IN FOREIGN CURRENCIES FOR DIVIDENDS", "EARNINGS IN FOREIGN EXCHANGE", "BONUS DETAILS",
					"NON-CURRENT INVESTMENTS", "CURRENT INVESTMENTS", "Source : Dion Global Solutions Limited"]
	return remove_string



def create_pre_list(remove_string, str_list):
	# str_list = remove_null(search_key)
	pre_list = []
	for each in str_list:
		if each in remove_string:
			pass
		else:
			pre_list.append(each.replace("-", "0"))
	return pre_list


def create_final_list(pre_list):
	final_list = [inner for outer in [(['Year_End', x] if x == 'Mar 18' else [x]) for x in pre_list] for inner in outer]
	return final_list


def create_dictionary(final_list, dictionary):
	i = 0
	while i < len(final_list):
			dictionary[str(final_list[i])] = [str(final_list[i + 1]), str(final_list[i + 2]), str(final_list[i + 3]),
									 str(final_list[i + 4]), str(final_list[i + 5])]
			i += 6
	return dictionary

def json_to_dataframe(dictionary):
	df = pd.DataFrame.from_dict(dictionary,orient='index').transpose()
	return df



def scrape_balance_sheet(isin, bse,nse,key):
	url = balance_sheet_url(key)
	response = get_response(url)
	soup = parse_response_to_text(response)
	rows = get_rows(soup)
	striped_data = strip_data(rows)
	str_list = remove_null(striped_data)
	remove_string = remove_strings_from_balancesheet()
	pre_list = create_pre_list(remove_string, str_list)
	final_list = create_final_list(pre_list)
	dictionary = {}
	dictionary = create_dictionary(final_list, dictionary)
	balance_sheet_df = json_to_dataframe(dictionary)
	return balance_sheet_df


def scrape_profit_loss(isin, bse,nse, key):
	url = profit_loss_url(key)
	response = get_response(url)
	soup = parse_response_to_text(response)
	rows = get_rows(soup)
	striped_data = strip_data(rows)
	str_list = remove_null(striped_data)
	remove_string = remove_strings_from_profit_loss()
	pre_list = create_pre_list(remove_string, str_list)
	final_list = create_final_list(pre_list)
	dictionary = {}
	dictionary = create_dictionary(final_list, dictionary)
	profit_loss_df = json_to_dataframe(dictionary)
	return profit_loss_df


def merge_profit_loss_balance_sheet(isin, bse,nse):
	try:
		search_string = get_search_string(isin, bse, nse)
		key = get_search_key(search_string)
		profit_loss = scrape_profit_loss(isin, bse, nse, key)
		balance_sheet = scrape_balance_sheet(isin, bse, nse, key)
		annual_report = pd.merge(profit_loss, balance_sheet)
		# annual_report.to_csv("/home/prm/Desktop/Money_Control_Api/annual_report.csv", index = False)
		return annual_report
	except:
		return "Failed"











