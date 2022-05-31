// Copyright (c) 2022, open-alt and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Expense Entry', {
	refresh: function(frm) {
		frm.events.get_attendce_employee_button(frm);
		frm.events.create_expenses_button(frm);
		frm.events.set_account_payable_filter(frm);
	},
	set_account_payable_filter: function(frm){
		frm.set_query("payable_account", function() {
			return {
				filters: {
					"report_type": "Balance Sheet",
					"account_type": "Payable",
					"company": frm.doc.company,
					"is_group": 0
				}
			};
		});
	},
	get_attendce_employee_button: function(frm){

			frm.add_custom_button(__('Get attendace employee'), function(){
				frm.events.get_attendace_employee(frm);
			},
			
			__("Actions"));
		
	},
	get_attendace_employee: function(frm){
		frm.call({
			doc: frm.doc,
			method: "get_attendace_employee",
		}).then((r) => {
		});
	},
	create_expenses_button: function(frm){
		// if(frm.doc.docstatus === 1){
		// 	frm.add_custom_button(__('Create expenses'), function(){
		// 		frm.events.create_expenses(frm);
		// 	},
			
		// 	__("Actions"));
		// }
	},
	create_expenses: function(frm){
		frm.call({
			doc: frm.doc,
			method: "create_expenses",
		}).then((r) => {
		});

	},
	
	

});
