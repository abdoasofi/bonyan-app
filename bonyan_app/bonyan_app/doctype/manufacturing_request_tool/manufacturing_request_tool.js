// Copyright (c) 2021, open-alt and contributors
// For license information, please see license.txt

frappe.ui.form.on('Manufacturing Request Tool', {
	refresh: function(frm) {
		frm.disable_save();
		frm.events.set_query(frm);
		frm.events.primary_action(frm);
	},
	set_query: function(frm){
		frm.fields_dict['manufacturing_request_warehouse'].grid.get_field(
			'manufacturing_warehouse').get_query = {
					type: "Manufacturing Warehouse"
			};
	},
	primary_action: function(frm){
		frm.page.set_primary_action(__('Create Material Request'), function(){
			frm.save();
		});
	},
});

window.route_to_requests = function (today){
	frappe.set_route("List", "Material Request", {
			"schedule_date": today,
			"material_request_type": "Manufacture",
			"docstatus": 1});
}
