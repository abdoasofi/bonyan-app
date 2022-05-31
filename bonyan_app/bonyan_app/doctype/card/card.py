# Copyright (c) 2021, open-alt and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from six import string_types
import json

class Card(Document):
	def before_save(self):
		fields = frappe.get_all("DocField", fields = ["fieldname", "default"],
		 	filters = {"parent": self.doctype_card, "in_standard_filter": 1})
		fields = {field["fieldname"] : field["default"] for field in fields}
		self.fields = json.dumps(fields)



@frappe.whitelist()
def save_filters(doc_name, filters):
	doc = frappe.get_doc("Card", doc_name)
	doc.filters = filters
	doc.save(ignore_permissions = True)
	return True
