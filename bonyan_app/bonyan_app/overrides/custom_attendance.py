import frappe
from frappe import _, msgprint
from erpnext.hr.doctype.attendance.attendance import Attendance
from .utils import validate_active_employee
from frappe.utils import getdate

class CustomAttendance(Attendance):
    """
    this class override for validate date function for fuctur data
    """ 
    def validate_attendance_date(self):
        date_of_joining = frappe.db.get_value("Employee", self.employee, "date_of_joining")

		# leaves can be marked for future dates
        # if self.status != 'On Leave' and not self.leave_application and getdate(self.attendance_date) > getdate(nowdate()):
        #     frappe.throw(_("Attendance can not be marked for future dates"))
        if date_of_joining and getdate(self.attendance_date) < getdate(date_of_joining):
            frappe.throw(_("Attendance date can not be less than employee's joining date"))



def validate_dates(doc, from_date, to_date):
	date_of_joining, relieving_date = frappe.db.get_value("Employee", doc.employee, ["date_of_joining", "relieving_date"])
	if getdate(from_date) > getdate(to_date):
		frappe.throw(_("To date can not be less than from date"))
	elif date_of_joining and getdate(from_date) < getdate(date_of_joining):
		frappe.throw(_("From date can not be less than employee's joining date"))
	elif relieving_date and getdate(to_date) > getdate(relieving_date):
		frappe.throw(_("To date can not greater than employee's relieving date"))