# Copyright (c) 2013, jyoti and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import flt, getdate, comma_and
from collections import defaultdict
import datetime
import json

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	item_details=fetching_container_details(filters)
	print("item_details",item_details)
	for items in item_details:
		data.append(["",items['item_group'],items['item_code'],items['stock_uom'],items['qty'],
		items['stock_qty'],items['qty']-items['stock_qty'],"","",items['rate'],items['amount'],
		items['rate']*(items['qty']-items['stock_qty'])])
	return columns, data

def fetching_container_details(filters):
	condition = get_conditions(filters)
	items = frappe.db.sql("""select tmri.item_code,tmri.rate,tmri.stock_qty,tmri.stock_uom, 
	ti.item_group,tmri.rate,tmri.qty,tmri.amount from `tabMaterial Request Item` tmri,
	`tabItem` ti  
	where ti.name=tmri.item_code %s
	order by ti.item_group""" % condition, as_dict=1)
	return items

def get_columns():
	"""return columns"""
	columns = [
			_("PO No.")+"::100",
			_("Item Group")+"::100",
			_("Item Code")+"::100",
			_("Stock Uom")+"::100",
			_("Total Qty")+"::100",
			_("Stock Qty")+":Link/Item:100",
			_("Order Qty")+"::100",
			_("Planning Remark")+"::100",
			_("Store Remark")+"::100",
			_("Price/unit")+"::100",
			_("Total BOM cost")+"::100",
			_("Order Cost")+"::100"
			

			]
	return columns

def get_conditions(filters):
	conditions=""
	if filters.get("project"):
		conditions += 'and  tmri.project= %s'  % frappe.db.escape(filters.get("project"), percent=False)

	if filters.get("bom_no"):
		conditions +='and tmri.pch_bom_no = %s' % frappe.db.escape(filters.get("bom_no"), percent=False)

	print("condition",conditions)
	return conditions

