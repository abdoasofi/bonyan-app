import frappe
from frappe import _, msgprint
from frappe.utils import get_link_to_form

class InactiveEmployeeStatusError(frappe.ValidationError):
	pass




def validate_active_employee(employee):
	if frappe.db.get_value("Employee", employee, "status") == "Inactive":
		frappe.throw(_("Transactions cannot be created for an Inactive Employee {0}.").format(
			get_link_to_form("Employee", employee)), InactiveEmployeeStatusError)



@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_filtered_dimensions(doctype, txt, searchfield, start, page_len, filters):
	from erpnext.accounts.doctype.accounting_dimension_filter.accounting_dimension_filter import (
		get_dimension_filter_map,
	)
	dimension_filters = get_dimension_filter_map()
	dimension_filters = dimension_filters.get((filters.get('dimension'),filters.get('account')))
	query_filters = []
	or_filters = []
	fields = ['name']

	searchfields = frappe.get_meta(doctype).get_search_fields()

	meta = frappe.get_meta(doctype)
	if meta.is_tree:
		query_filters.append(['is_group', '=', 0])

	if meta.has_field('disabled'):
		query_filters.append(['disabled', '!=', 1])

	if meta.has_field('company'):
		query_filters.append(['company', '=', filters.get('company')])

	for field in searchfields:
		or_filters.append([field, 'LIKE', "%%%s%%" % txt])
		fields.append(field)

	if dimension_filters:
		if dimension_filters['allow_or_restrict'] == 'Allow':
			query_selector = 'in'
		else:
			query_selector = 'not in'

		if len(dimension_filters['allowed_dimensions']) == 1:
			dimensions = tuple(dimension_filters['allowed_dimensions'] * 2)
		else:
			dimensions = tuple(dimension_filters['allowed_dimensions'])

		query_filters.append(['name', query_selector, dimensions])


	output = frappe.get_list(doctype, fields=fields, filters=query_filters, or_filters=or_filters, as_list=1)

	return [tuple(d) for d in set(output)]
