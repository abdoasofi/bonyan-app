from . import __version__ as app_version

app_name = "bonyan_app"
app_title = "bonyan-app"
app_publisher = "open-alt"
app_description = "customize in erpnext"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "erpnext@open-alt.com"
app_license = "MIT"

required_apps = ['erpnext', 'monitoring_and_evaluation', 'openalt_theme']


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/bonyan_app/css/bonyan_app.css"
app_include_js = "/assets/bonyan_app/js/dimensions.js"

# include js, css files in header of web template
# web_include_css = "/assets/bonyan_app/css/bonyan_app.css"
# web_include_js = "/assets/bonyan_app/js/bonyan_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bonyan_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
page_js = {"point-of-sale" : "public/js/point-of-sale.js"}

# include js in doctype views
# doctype_js = {"Leave Application" : "public/js/custome_leave_application.js"}


doctype_js  = {
  "Employee Advance": [
    "public/js/employee_advance.js",
  ],
  "Appraisal": [
    "public/js/appraisal.js",
  ],
  "Warehouse": [
    "public/js/warehouse.js",
  ],
  "Material Request": [
    "public/js/material_request.js"
  ],
  "Leave Application" : [
    "public/js/custome_leave_application.js"
    ],
  "Volunteer": [
    "public/js/volunteer.js",
  ],
  "Payment Entry": [
    "public/js/payment_entry.js"
  ]
}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "bonyan_app.install.before_install"
# after_install = "bonyan_app.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bonyan_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
    "Material Request": "bonyan_app.bonyan_app.utils.permissions.material_request.material_request_query",
    "Expense Claim": "bonyan_app.bonyan_app.utils.permissions.expense_claim.expense_claim_entry_query",
}

#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Employee Advance": "bonyan_app.bonyan_app.overrides.custom_employee_advance.CustomEmployeeAdvance",
	"Attendance Request": "bonyan_app.bonyan_app.overrides.custom_attendance_request.CustomRequestAttendance",
	"Attendance": "bonyan_app.bonyan_app.overrides.custom_attendance.CustomAttendance",
  "Leave Application": "bonyan_app.bonyan_app.overrides.custom_leave_application.CustomLeaveApplication",
  "Payment Entry": "bonyan_app.bonyan_app.overrides.payment_entry.CustomPaymentEntry",

}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Appraisal": {
		"before_save": "bonyan_app.bonyan_app.doc_events.appraisal.set_appraisal_evaluation",
	},
  "POS Invoice":{
    "validate": "bonyan_app.bonyan_app.doc_events.point_of_sale.validate_pos_invoice"
  },
  "Material Request":{
    "on_update": "bonyan_app.bonyan_app.doc_events.material_request.share_request_with_approver"
  },
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"bonyan_app.tasks.all"
# 	],
    "daily": [
    "bonyan_app.scheduler_events.material_request.make_manufacturing_material_request"
    ],
# 	"hourly": [
# 		"bonyan_app.tasks.hourly"
# 	],
# 	"weekly": [
# 		"bonyan_app.tasks.weekly"
# 	]
# 	"monthly": [
# 		"bonyan_app.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "bonyan_app.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.hr.doctype.leave_application.leave_application.get_number_of_leave_days": "bonyan_app.bonyan_app.overrides.custom_leave_application.get_number_of_leave_days"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "bonyan_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"bonyan_app.auth.validate"
# ]
