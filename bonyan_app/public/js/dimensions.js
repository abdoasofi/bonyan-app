frappe.provide("erpnext.queries");
$.extend(erpnext.queries, {
	get_filtered_dimensions: function(doc, child_fields, dimension, company) {
		let account = '';

		child_fields.forEach((field) => {
			if (!account) {
				account = doc[field];
			}
		});

		return {
			query: "bonyan_app.bonyan_app.overrides.utils.get_filtered_dimensions",
			filters: {
				'dimension': dimension,
				'account': account,
				'company': company
			}
		};
	}
});
