frappe.ui.form.on('Payment Entry', {
    refresh: function(frm) {
		console.log("this is payment entry");
        
        frm.events.set_query(frm);

        
	},
    is_employee_expense_entry: function(frm){
        frm.events.set_query(frm);
    },
    paid_to_filter_cread: function(frm){
        frm.set_query("paid_to", function() {
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

    refrence_filter: function(frm){
        frm.set_query("reference_doctype", "references", function() {
			
				var doctypes = ["Expense Claim", "Journal Entry"];
		

			return {
				filters: { "name": ["in", doctypes] }
			};
		});
    },

    refrence_name_filter: function(frm){
        frm.set_query("reference_name", "references", function(doc, cdt, cdn) {
			const child = locals[cdt][cdn];
			const filters = {"docstatus": 1, "company": doc.company};
			// const party_type_doctypes = ['Sales Invoice', 'Sales Order', 'Purchase Invoice',
			// 	'Purchase Order', 'Expense Claim', 'Fees', 'Dunning', 'Donation'];

			// if (in_list(party_type_doctypes, child.reference_doctype)) {
			// 	filters[doc.party_type.toLowerCase()] = doc.party;
			// }

			if(child.reference_doctype == "Expense Claim") {
				filters["docstatus"] = 1;
				filters["is_paid"] = 0;
                filters["expense_entry"] = frm.doc.employee_expense_entry
			}

			return {
				filters: filters
			};
		});

    },
    

    set_query: function(frm){
        if(frm.doc.is_employee_expense_entry){
            frm.events.paid_to_filter_cread(frm);
            // frm.refresh();
            frm.refresh_field('paid_to');
            frm.events.refrence_filter(frm);
            frm.events.refrence_name_filter(frm)
            frm.refresh_field('references');
        }
    },
    get_employee_expenses_entry: function(frm){
        frm.call({
            doc: frm.doc,
            method: "get_employee_expenses_entry",
        }).then((r) => {
        });

    }
})