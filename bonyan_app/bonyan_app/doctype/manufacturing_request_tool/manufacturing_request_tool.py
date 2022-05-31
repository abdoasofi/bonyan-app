# Copyright (c) 2021, open-alt and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import today
from frappe.model.document import Document
from ....scheduler_events.material_request import make_manufacturing_material_request

class ManufacturingRequestTool(Document):
	def save(self):
		#on install self.manufacturing_request_warehouse is not defined
		try:
			warehouse_name = {mf.manufacturing_warehouse for mf in self.manufacturing_request_warehouse}
			res = make_manufacturing_material_request(warehouse_name, False)

			title = _("Failed")
			indicator = "red"
			message = ""

			if res["created"]:
				message = _("Material Requests created for {0} for today {1}.").format(
					", ".join(res["created"]),
					today()) + "<br/>"
				title = _("Success")
				indicator = "green"


			if res["found"]:
				message += _("{0} Has already Material Request for today {1}.").format(
				", ".join(res["found"]),
				today()) + "<br/>"

			no_create = warehouse_name.difference(res["created"].union(res["found"]))

			if no_create:
				message += _("No Material Request created for {0}.").format(", ".join(no_create))

			frappe.msgprint(message,
				title = title,
				indicator = indicator,
				primary_action = {
					"label": _("Material Requests"),
					"client_action" : "route_to_requests",
					"args": today()
					}
				)

			self.manufacturing_request_warehouse = []
		except AttributeError:
			#on install self.manufacturing_request_warehouse is not defined
			pass
