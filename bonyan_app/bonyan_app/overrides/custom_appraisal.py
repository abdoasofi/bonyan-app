from erpnext.hr.doctype.appraisal.appraisal import Appraisal
import frappe
from frappe import _, msgprint
from bonyan_app.bonyan_app.overrides.custom_employee_advance.custom_employee_advance import share_doc_with_approver

class CustomAppraisal(Appraisal):
    def onload(self):
        super().onload()
    def on_submit(self):
        if self.approval_status=="Draft":
            frappe.throw(_("""Approval Status must be 'Approved' or 'Rejected'"""))

    def on_update(self):
        super().on_update()
        share_doc_with_approver(self, self.expense_approver) 
   