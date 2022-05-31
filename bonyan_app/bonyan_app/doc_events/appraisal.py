import frappe
from frappe import _


def set_appraisal_evaluation(appraisal, method):
    evaluation = frappe.get_all("Appraisal Evaluation",
        filters = [{"min_rate": ['<=', appraisal.rate]}],
        order_by = 'min_rate desc', pluck = 'name',
        limit_page_length = 1)
    if evaluation:
        appraisal.appraisal_evaluation = evaluation[0]
