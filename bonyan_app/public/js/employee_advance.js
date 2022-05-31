frappe.ui.form.on('Employee Advance', {
    onload: function(frm) {
        // frm.events.fresh_advance_request(frm);
        // console.log("on load");
        if(frm.doc.request_type=="Advance"){
            frm.add_fetch("company", "default_employee_advance_account", "advance_account");
        }
        else if(frm.doc.request_type=="Covenant"){
            frm.add_fetch("company", "default_employee_covenant_account", "advance_account");
        }
    },
    refresh: function(frm){
        console.log("on refresh");
        if(!frm.is_new()){
            frm.set_df_property('request_type', 'read_only', 1);
            
        }
        frm.set_query('task', () =>
            {
                // var project = frm.doc.project ?  : '';
                 return { filters: {project: frm.doc.project} } 
            });

        frm.set_query("expense_approver", function() {
            return {
                query: "erpnext.hr.doctype.department_approver.department_approver.get_approvers",
                filters: {
                    employee: frm.doc.employee,
                    doctype: "Expense Claim"
                }
            };
        });

        frm.set_query('task', () => {return {filters: { project: frm.doc.project }}});
        frm.set_query('project', () => {return {filters: { status: 'Open' }}});
    },
project: function(frm){
    frappe.call({
        doc: frm.doc,
        method: "update_project_costing",
       callback: function(r) {
        frm.refresh_field('project_budget');
        frm.refresh_field('project_paid_amount');
        frm.refresh_field('remaining_amount');
        frm.refresh_field('pending_project_advance_amount');
        frm.refresh_field('project_balance_amount');
           }
       });

       frm.set_value('task', '');
    	    
       frappe.db.get_value("Project", {"name": frm.doc.project}, "status", (r) => {
       console.log("", r);
       if(r.status!="Open"){
             frm.set_value({   project: ''});
       }
       });
},
task: function(frm){
  frappe.call({
      doc: frm.doc,
      method: "update_task_costing",
     callback: function(r) {
      frm.refresh_field('task_spending_amount');
      frm.refresh_field('remaining_task_amount_base_on_budget');
      frm.refresh_field('pending_task_advance_amount');
      frm.refresh_field('task_balance_amount');
         }
     });
},
request_type: function(frm){
     frm.events.fresh_advance_request(frm);
    },
fresh_advance_request: function(frm){
    if(frm.doc.request_type!=null){
        frappe.call({
                method:"bonyan_app.bonyan_app.overrides.custom_employee_advance.get_request_type_account",
                args:{
                    request_type: frm.doc.request_type,
                    company: frm.doc.company
                },
                callback:function(r){
                        frm.set_value("advance_account", r.message);
                        if(frm.doc.request_type=="Advance"){
                            frm.set_value("naming_series", "HR-EAD-.YYYY.-");
                        }
                        else if(frm.doc.request_type=="Covenant"){
                            frm.set_value("naming_series", "HR-ECO-.YYYY.-");
                        }
                        }
                });
        frm.set_value("advance_account", "");
        if(frm.doc.request_type=="Advance"){
            frm.set_value("repay_unclaimed_amount_from_salary", 1);
            frm.set_value("project_required", 0);
            frm.set_value("project", " ");
            frm.toggle_display("project_and_task", 0);
            // frm.set_value("naming_series", "HR-EAD-.YYYY.-");
            frm.add_fetch("company", "default_employee_advance_account", "advance_account");
            project_and_task
        }
        else if(frm.doc.request_type=="Covenant"){
            frm.toggle_display("project_and_task", 1);
            frm.set_value("repay_unclaimed_amount_from_salary", 0);
            frm.set_value("project_required", 1);
            // frm.set_value("naming_series", "HR-ECO-.YYYY.-");
            frm.add_fetch("company", "default_employee_covenant_account", "advance_account");
        }
    }
},
});
