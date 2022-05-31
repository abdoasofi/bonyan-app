

import frappe

def create_account_dimension(doctype, label):
    if not frappe.db.exists("Accounting Dimension", {'label': label}):
        if not frappe.db.exists("Accounting Dimension", {'document_type': doctype}):
            new_doc = frappe.new_doc("Accounting Dimension")
            new_doc.document_type = doctype
            new_doc.label = label
            new_doc.insert()



    
def execute():
    create_account_dimension("Task", "Task")
