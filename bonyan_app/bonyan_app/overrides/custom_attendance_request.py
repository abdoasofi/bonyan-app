import frappe
from frappe import _, msgprint
from erpnext.hr.doctype.attendance_request.attendance_request import AttendanceRequest
from .utils import validate_active_employee
from frappe.utils import getdate

class CustomRequestAttendance(AttendanceRequest):
    """
    this class override for validate date function for fuctur data
    """ 
    def validate(self):
        validate_active_employee(self.employee)
        validate_dates(self, self.from_date, self.to_date)
        if self.half_day:
            if not getdate(self.from_date)<=getdate(self.half_day_date)<=getdate(self.to_date):
                frappe.throw(_("Half day date should be in between from date and to date"))



def validate_dates(doc, from_date, to_date):
	date_of_joining, relieving_date = frappe.db.get_value("Employee", doc.employee, ["date_of_joining", "relieving_date"])
	if getdate(from_date) > getdate(to_date):
		frappe.throw(_("To date can not be less than from date"))
	elif date_of_joining and getdate(from_date) < getdate(date_of_joining):
		frappe.throw(_("From date can not be less than employee's joining date"))
	elif relieving_date and getdate(to_date) > getdate(relieving_date):
		frappe.throw(_("To date can not greater than employee's relieving date"))