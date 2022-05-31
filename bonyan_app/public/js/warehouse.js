frappe.ui.form.on('Warehouse', {
    refresh: function(frm){
      frm.events.set_query(frm);
    },
    set_query: function(frm){
      debugger;
      frm.set_query("manufacturing_warehouse", {"type": "Manufacturing Warehouse"});
    },
});
