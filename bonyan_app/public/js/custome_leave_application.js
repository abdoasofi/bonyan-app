frappe.ui.form.on('Leave Application', {
    hours_furlough: function(frm){

        frm.trigger('calculate_total_days');
        // var employee = frm.doc.holiday_list;
        // // var employee = "dsfhasjkfhksa"
        // console.log("this is employee", employee);
    },
	from_time: function(frm){
		console.log(frm.doc.from_time, frm.doc.to_time)
        frm.trigger('calculate_total_days');
        // var employee = frm.doc.holiday_list;
        // // var employee = "dsfhasjkfhksa"
        // console.log("this is employee", employee);
    },
	to_time: function(frm){

        frm.trigger('calculate_total_days');
        // var employee = frm.doc.holiday_list;
        // // var employee = "dsfhasjkfhksa"
        // console.log("this is employee", employee);
    },

	from_date: function(frm){

        frm.trigger('calculate_total_days');
        // var employee = frm.doc.holiday_list;
        // // var employee = "dsfhasjkfhksa"
        // console.log("this is employee", employee);
    },
	to_date: function(frm){

        frm.trigger('calculate_total_days');
        // var employee = frm.doc.holiday_list;
        // // var employee = "dsfhasjkfhksa"
        // console.log("this is employee", employee);
    },

	calculate_total_days: function(frm){
        if (frm.doc.from_date && frm.doc.to_date && frm.doc.employee && frm.doc.leave_type) {

			var from_date = Date.parse(frm.doc.from_date);
			var to_date = Date.parse(frm.doc.to_date);

			if (to_date < from_date) {
				frappe.msgprint(__("To Date cannot be less than From Date"));
				frm.set_value('to_date', '');
				return;
			}
            
			// server call is done to include holidays in leave days calculations
			return frappe.call({
				method: 'bonyan_app.bonyan_app.overrides.custom_leave_application.get_number_of_leave_days',
				args: {
					"employee": frm.doc.employee,
					"leave_type": frm.doc.leave_type,
					"from_date": frm.doc.from_date,
					"to_date": frm.doc.to_date,
					"half_day": frm.doc.half_day,
					"is_furlough": frm.doc.is_furlough,
					"half_day_date": frm.doc.half_day_date,
                    "hours_furlough": frm.doc.hours_furlough,
					"from_time": frm.doc.from_time,
					"to_time": frm.doc.to_time
				},
				callback: function(r) {
					if (r && r.message) {
						frm.set_value('total_leave_days', r.message);
						frm.trigger("get_leave_balance");
					}
				}
			});
		}
    }
})