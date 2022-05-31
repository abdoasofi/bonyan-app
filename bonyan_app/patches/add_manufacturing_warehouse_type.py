""" to add two Warehouse Type (Retail Warehouse) and (Manufacturing Warehouse)
"""

import frappe

def create_warehouse_type(type):
    doc = frappe.get_doc({
        "doctype": "Warehouse Type",
        "__newname": type,
        "type": type,
    })
    doc.save()
    return doc

def execute():
    create_warehouse_type("Manufacturing Warehouse")
    create_warehouse_type("Retail Warehouse")
