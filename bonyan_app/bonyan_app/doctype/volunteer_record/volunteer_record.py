# Copyright (c) 2021, open-alt and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.desk.form import assign_to

class VolunteerRecord(Document):
	def save(self):
		super().save()
		if self.volunteer_hours_approver:
			user = frappe.db.get_value("Employee", self.volunteer_hours_approver, ["user_id"])
			if user:
				assign_to.add(dict(
				assign_to = [user],
				doctype = "Volunteer Record",
				name = self.get('name'),
				description = _("Volunteer Hours Working need Approved"),
				notify = True
				))
		
	def validate(self):
		if self.type=="Employee":
			employee = frappe.db.get_value("Employee", self.employee, ["reports_to"])
			if self.volunteer_hours_approver!=employee:
				frappe.throw(_("Volunteer Hours Approver is not the Employee Approver"))

		elif self.type=="Volunteer":
			volunteer = frappe.db.get_value("Volunteer", self.volunteer, ["reports_to"])
			if self.volunteer_hours_approver!=volunteer:
				frappe.throw(_("Volunteer Hours Approver is not the Volunteer Approver"))

	def on_submit(self):
		user = frappe.session.user
		if "Employee" in frappe.get_roles():
			emp = frappe.db.get_value("Employee", {"user_id":user}, ["name"])
			if emp:
				if self.volunteer_hours_approver!=emp:
					frappe.throw(_('Can not Submitted, You are not the responsible person for this employee.'))
			else:
				frappe.throw(_("Your User not connect to Employee."))						
		else:
			frappe.throw(_("You do not have Employee Role."))

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_volunteer_hours_approver(doctype, txt, searchfield, start, page_len, filters):
	args = {
		'employee': filters.get("employee"),
		"volunteer": filters.get("volunteer")
	}
	list = None
	type = filters.get("doctype")

	if type=="Employee":
		list = frappe.db.sql("""select name, employee_name from tabEmployee
		where name=(select reports_to from tabEmployee
		where name=%(employee)s)""", args)
	elif type=="Volunteer":
		list = frappe.db.sql("""select name, employee_name from tabEmployee
		where name=(select reports_to from tabVolunteer
		where name=%(volunteer)s)""", args)

	return list
	
