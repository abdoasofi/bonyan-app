import frappe
from frappe import _



def share_request_with_approver(doc, method):
    from erpnext.hr.utils import  share_doc_with_approver
    frappe.share.add(doc.doctype, doc.name, doc.employee_approvor, submit=1,
			flags={"ignore_share_permission": True})

    frappe.msgprint(_("Shared with the user {0} with {1} access").format(
			doc.employee_approvor, frappe.bold("submit"), alert=True))
