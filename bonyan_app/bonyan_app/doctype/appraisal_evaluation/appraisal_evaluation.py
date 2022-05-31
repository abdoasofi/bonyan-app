# Copyright (c) 2021, open-alt and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class AppraisalEvaluation(Document):
	def validate(self):
		found = frappe.db.exists(self.doctype,
				{'min_rate': self.min_rate, 'name' : ['!=', self.name]})

		if found:
			frappe.throw(_("For Min Rate {0} already found {1}").format(
					frappe.bold(self.min_rate),
					frappe.get_desk_link(self.doctype, found),
					))
