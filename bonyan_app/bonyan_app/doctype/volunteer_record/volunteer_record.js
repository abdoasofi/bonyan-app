// Copyright (c) 2021, open-alt and contributors
// For license information, please see license.txt

frappe.ui.form.on('Volunteer Record', {
	onload: function(frm){
		frm.set_value("date", frappe.datetime.nowdate());
	},
	refresh: function(frm) {
		frm.trigger('toggle_type');

		// document_for
		frm.set_query('document_for', () => 
		{ return { filters: {name:  ["in", ["Employee", "Volunteer"]]} }
	 });

	 frm.set_query("volunteer_hours_approver", function() {
		return {
			query: "bonyan_app.bonyan_app.doctype.volunteer_record.volunteer_record.get_volunteer_hours_approver",
			filters: {
				employee: frm.doc.employee,
				doctype: frm.doc.type,
				volunteer: frm.doc.volunteer
			}
		};
	});
	},
	type: function(frm) {
		frm.trigger('toggle_type');	
	},
	employee: function(frm) {
		frm.trigger('clear_fileds');	
	},
	volunteer: function(frm) {
		frm.trigger('clear_fileds');
	},
	toggle_type:function(frm){
		if(frm.doc.type=="Employee"){
			frm.set_df_property('employee', 'reqd', 1);
			frm.set_df_property('volunteer', 'reqd', 0);
			frm.set_value("volunteer","");
			frm.set_value("volunteer_name","");
		}
		else if (frm.doc.type=="Volunteer"){
			frm.set_df_property('employee', 'reqd', 0);
			frm.set_df_property('volunteer', 'reqd', 1)
			frm.set_value("employee","");
			frm.set_value("employee_full_name","");
		}
	},
	clear_fileds: function(frm){
		frm.set_value("volunteer_hours_approver","");
	}
});
