from __future__ import unicode_literals
import frappe
import json
from frappe.utils.nestedset import get_root_of
from frappe.utils import cint


@frappe.whitelist()
def get_qty(customer, item):

    customer = frappe.get_doc('Customer', json.loads(customer)['customer'])
    beneficiaries = frappe.get_all('Beneficiary',
            filters = {
                "beneficiary_status": "Active"
            },
            or_filters = {'customer': customer.name, "id": customer.id}, pluck = "name"
        )
    if beneficiaries:
        qty = 0
        for b in beneficiaries:
            beneficiary = frappe.get_doc('Beneficiary', b)
            for i in beneficiary.beneficiary_items:
                if i.item == json.loads(item)['item_code']:
                    qty += i.quantity

        return qty
    else:
        return 1
