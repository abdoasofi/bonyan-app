import frappe
from frappe.utils import today

def get_beneficiaries_items(manufacturing_warehouse, test_settings):
    """ get Manufacturing Warehouse, Retail Warehouse, items, and quantity
    """

    filter_str = " AND `wh`.`manufacturing_warehouse` in %(manufacturing_warehouse)s" if manufacturing_warehouse else ""
    if test_settings:
        filter_str +=" AND `mf_wh`.`auto_material_request` = 1"

    beneficiaries_items = frappe.db.sql("""
        SELECT
            `wh`.`manufacturing_warehouse`,
            `bf`.`retail_warehouse`,
            `bf_it`.`item`,
            SUM(`bf_it`.`quantity`) AS `quantity`
        FROM
            `tabBeneficiary` AS `bf`,
            `tabBeneficiary Item` AS `bf_it`,
            `tabItem` AS `it`,
            `tabWarehouse` AS `wh`,
            `tabWarehouse` AS `mf_wh`
        WHERE
            `bf`.`beneficiary_status` = 'Active' AND `bf_it`.`parent` = `bf`.`name` AND
            `bf_it`.`item` = `it`.`name` AND `it`.`default_bom` IS NOT NULL AND
            `wh`.`name` = `bf`.`retail_warehouse`  AND
            `mf_wh`.`name` = `wh`.`manufacturing_warehouse` {filter_str}
        GROUP BY
            `bf`.`retail_warehouse`,
            `bf_it`.`item`
    """.format(filter_str = filter_str),
        {"manufacturing_warehouse": manufacturing_warehouse},
        as_dict = True)
    return beneficiaries_items


def get_warehouse_required_amount(manufacturing_warehouse, test_settings):
    beneficiaries_items = get_beneficiaries_items(manufacturing_warehouse, test_settings)
    required_amount = dict()

    for bi in beneficiaries_items:
        required_amount.setdefault(bi['manufacturing_warehouse'], []).append({
            "warehouse": bi["manufacturing_warehouse"],
            "retail_warehouse": bi["retail_warehouse"],
            "item_code": bi["item"],
            "qty": bi["quantity"]
        })
    return required_amount


def requst_found(dt, manufacturing_warehouse, today_date):
    return frappe.db.exists(dt, {
        "manufacturing_warehouse": manufacturing_warehouse,
        "schedule_date": today_date,
        "material_request_type": "Manufacture",
        "docstatus": ["in", (0,1)]})


def make_material_request(required_amount):
    dt = "Material Request"
    today_date = today()
    result = {"found" : set(), "created" : set()}

    for (manuf, items) in required_amount.items():
        if requst_found(dt, manuf, today_date):
            result["found"].add(manuf)
        else:
            material_request = frappe.get_doc({
                "doctype": dt,
                "material_request_type": "Manufacture",
                "manufacturing_warehouse": manuf,
                "schedule_date": today_date,
                "items": items,
            })
            material_request.save()
            material_request.submit()
            result["created"].add(manuf)

    return result



def make_manufacturing_material_request(manufacturing_warehouse = None, test_settings = True):
    """ make material_request that lead to Manufacture beneficiaries allocation.
    """

    required_amount = get_warehouse_required_amount(manufacturing_warehouse, test_settings)
    return make_material_request(required_amount)
