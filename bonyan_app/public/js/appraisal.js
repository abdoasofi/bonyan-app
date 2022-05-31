frappe.ui.form.on('Appraisal', {
    refresh: function(frm){
        // frm.evaluation = frm.get_field('evaluation').df.options.split('\n')

        frm.set_query("expense_approvers", function() {
            return {
                query: "erpnext.hr.doctype.department_approver.department_approver.get_approvers",
                filters: {
                    employee: frm.doc.employee,
                    doctype: "Expense Claim"
                }
            };
        });
    },
    total_score: function(frm) {
        frm.set_value("rate", (frm.doc.total_score / 5) * 100);
    },
    before_save: function(frm) {
        frm.set_value("appraisal_evaluation", null);
    },
})

frappe.ui.form.on('Appraisal Skill', {
	score: function(frm, cdt, cdn) {
		var d = locals[cdt][cdn];
		if (flt(d.score) > 5) {
			frappe.msgprint(__("Score must be less than or equal to 5"));
			d.score = 0;
			refresh_field('score', d.name, 'goals');
		}
		else {
			frm.trigger('set_score_earned');
		}
	},
});
