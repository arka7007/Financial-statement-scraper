from flask import Flask, request, jsonify
import json
import os
import MoneyControl_Scrape as mcs
import lineitem_mapping as lm
import pprint

app = Flask(__name__)

@app.route('/moneyControl', methods=["GET", "POST"])
def get_co_name():
	if request.method == "POST":
		company_datils = request.json['Screap_Details']['CompDetails']
		co_name = company_datils['Name']
		isin = company_datils['NAICSCode']
		bse = company_datils['SICCode']
		nse = "AXISBANK"
		status = lm.store_annual_finance_data(isin, bse,nse, co_name)
	return "True"


@app.route('/Test', methods=["GET","POST"])
def test():
	if request.method == "POST":
		print(request.json)
		file_name = request.json['co_name']
		if not file_name:
			return "Check"
		else:
			return "Ok" 

if __name__ == '__main__':
	app.run(host='192.168.2.119', port=5000)