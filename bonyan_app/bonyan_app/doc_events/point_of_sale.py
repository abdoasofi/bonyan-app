import frappe
from frappe import _, msgprint

import datetime


def validate_pos_invoice(doctype, method):
    """
    this function for validate doctype pos invoice to make shure qnt is the same
    """
    invoices_today = frappe.db.get_list('POS Invoice', filters={
                                        'customer': doctype.customer, 'posting_date': doctype.posting_date, 'status': 'paid'}, pluck='name')
    id = frappe.db.get_value("Customer", doctype.customer, "id")
    beneficiaries = frappe.get_all('Beneficiary',
            filters = {
                "retail_warehouse": doctype.set_warehouse,
                "beneficiary_status": "Active"
            },
            or_filters = {'customer': doctype.customer, "id": id}, pluck = "name"
        )
    if beneficiaries:
        for i in doctype.items:
            count = sum(frappe.db.get_list('POS Invoice Item', filters={
                        'item_code': i.item_code, 'parent': ['in', invoices_today]}, pluck='qty'))

            item_qty = get_item_qty(beneficiaries, i.item_code)

            if item_qty:
                if count >= item_qty:

                    frappe.throw(_("Item Quantity {0} is more than specified quantity for item {1}.").format(
                        count, i.item_code))
            else:
                frappe.throw(
                    _("Beneficiary has not quantity for item {0} please add it.").format(i.item_code))
    else:
        frappe.throw(
                    _("Customer has not beneficiary , {0} please add it.").format(doctype.customer))



def get_item_qty(beneficiaries, item_code):
    """
    this function for get beneficiary item qty from beneficiary
    doctype
    beneficiary: beneficiary doctype
    item_code: item code need to get gty for it
    """
    for b in beneficiaries:
        beneficiary = frappe.get_doc("Beneficiary", b)
        for i in beneficiary.beneficiary_items:
            if i.item == item_code:
                return i.quantity
        return None
