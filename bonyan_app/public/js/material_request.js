frappe.ui.form.on('Material Request', {
    refresh: function(frm){
      frm.set_query("employee_approvor", function() {
        return {
            query: "erpnext.hr.doctype.department_approver.department_approver.get_approvers",
            filters: {
                employee: frm.doc.employee,
                doctype: "Expense Claim"
            }
        };
    });
        frm.events.set_query(frm);
    },
    set_query: function(frm){

      
      frm.set_query("manufacturing_warehouse", function(){
        return {
          filters: {
            "type": "Manufacturing Warehouse",
            "company": frm.doc.company,
          }
        };
      });
    },
    manufacturing_warehouse: function(frm){
      if (frm.doc.manufacturing_warehouse)
      {
        frm.set_df_property("set_warehouse", "read_only", true);
        frm.set_value("set_warehouse", frm.doc.manufacturing_warehouse);
      }
      else {
        frm.set_df_property("set_warehouse", "read_only", false);
      }
    },
});

frappe.ui.form.on("Material Request Item", {
    item_code: function(frm, cdt, cdn)
    {
      if (frm.doc.manufacturing_warehouse)
      {
        const item = locals[cdt][cdn];
        frappe.model.set_value(cdt, cdn, 'warehouse', frm.doc.manufacturing_warehouse)
      }
    }
}
);
