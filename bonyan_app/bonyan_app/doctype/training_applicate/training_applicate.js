// Copyright (c) 2022, open-alt and contributors
// For license information, please see license.txt

frappe.ui.form.on('Training Applicate', {
  refresh: function(frm) {
    frm.set_query("approver", function() {
            return {
                query: "erpnext.hr.doctype.department_approver.department_approver.get_approvers",
                filters: {
                    employee: frm.doc.employee,
                    doctype: "Expense Claim"
                }
            };
        });
  }
});
