from erpnext.hr.doctype.employee_advance.employee_advance import EmployeeAdvance
# from erpnext.erpnext.projects.doctype.task import Task
import frappe
from frappe import _, msgprint

class CustomEmployeeAdvance(EmployeeAdvance):
    def onload(self):
        super().onload()
        if self.docstatus!=1:
            self.update_costing()

    def on_submit(self):
        if self.approval_status=="Draft" and self.request_type == "Covenant":
            frappe.throw(_("""Approval Status must be 'Approved' or 'Rejected'"""))


    def on_update(self):
        # super().on_update()
        if self.request_type == "Covenant":
            share_doc_with_approver(self, self.expense_approver)


    def validate(self):
        super().validate()

        if self.request_type == "Covenant":
            self.validate_advance_amount()
        else:
            self.expense_approver = None

    def submit(self):
        super().submit()

        if self.request_type == "Covenant":
            self.validate_advance_amount()

    def validate_advance_amount(self):
        if self.task:
            self.project = frappe.get_doc("Task", self.task).project
            self.validate_task_advance_amount()
            self.validate_project_advance_amount()
        elif self.project:
            self.validate_project_advance_amount()


    def update_costing(self):
        if self.task:
            self.update_task_costing()
        if self.project:
            self.update_project_costing()

    def validate_project_advance_amount(self):
        project_spending_amount, project_balance_amount = get_actual_paid_amount("project", self.project)
        project_budget =  get_projects_budget_amount([self.project])[0]
        paid_amount, pending_amount_for_project = get_pending_amount_for_doc("project", self.project, self.posting_date)

        remaining_amount = project_budget - (project_spending_amount + (pending_amount_for_project))

        project_budget = get_project_budget(self.project)
        if project_budget:
            if self.advance_amount > remaining_amount:
                if project_budget.action_if_annual_budget_exceeded_on_actual_for_project=="Stop":
                    frappe.throw(_("Advance Amount Greater than Remaining Amount for this project {0}.").format(self.project))
                elif project_budget.action_if_annual_budget_exceeded_on_actual_for_project=="Warn":
                    frappe.msgprint(_("Advance Amount Greater than Remaining Amount for this project {0}.").format(self.project))

    @frappe.whitelist()
    def update_project_costing(self):
        project_paid_amount, project_balance_amount = get_actual_paid_amount("project", self.project)
        project_budget =  get_projects_budget_amount([self.project])[0]
        remaining_amount = project_budget - project_paid_amount
        pending_amount_for_project = get_pending_amount_for_doc("project", self.project, self.posting_date)[1]
        if self.project:
            self.project_budget = project_budget
            self.project_paid_amount = project_paid_amount
            self.remaining_amount = remaining_amount
            self.pending_project_advance_amount = pending_amount_for_project
            self.project_balance_amount = project_balance_amount

    def validate_task_advance_amount(self):
        if self.task:
            task_spending_amount, task_balance_amount = get_actual_paid_amount("task", self.task)
            paid_amount, pending_amount_for_task = get_pending_amount_for_doc("task", self.task, self.posting_date)

            remaining_amount = self.task_budget - (task_spending_amount + (pending_amount_for_task-paid_amount))

            project_budget = get_project_budget(self.project)
            if project_budget:
                if self.advance_amount > remaining_amount:
                    if project_budget.action_if_annual_budget_exceeded_on_actual_for_project=="Stop":
                        frappe.throw(_("Advance Amount Greater than Remaining Amount for this task {0}.").format(self.task))
                    elif project_budget.action_if_annual_budget_exceeded_on_actual_for_project=="Warn":
                        frappe.msgprint(_("Advance Amount Greater than Remaining Amount for this task {0}.").format(self.task))

    @frappe.whitelist()
    def update_task_costing(self):
        if self.task:
            task_paid_amount, task_balance_amount = get_actual_paid_amount("task", self.task)
            remaining_amount = self.task_budget - task_paid_amount
            pending_amount_for_task = get_pending_amount_for_doc("task", self.task, self.posting_date)[1]
            self.task_spending_amount = task_paid_amount
            self.remaining_task_amount_base_on_budget	 = remaining_amount
            self.pending_task_advance_amount = pending_amount_for_task
            self.task_balance_amount = task_balance_amount



def get_pending_amount_for_doc(type, document, posting_date):
	project_due_amount = frappe.get_all("Employee Advance", \
		filters = {type: document, "docstatus":1, "posting_date":("<=", posting_date)}, \
		fields = ["advance_amount", "paid_amount"])
	paid_amount_sum = sum([(emp.paid_amount) for emp in project_due_amount])
	advance_amount_sum = sum([(emp.advance_amount) for emp in project_due_amount])

	return paid_amount_sum,advance_amount_sum


def get_actual_paid_amount(type, document):
    cash_bank_account = frappe.get_all("Account", filters={"account_type": ["in", "Cash, Bank"]},
                        pluck = "name")
    account_name = cash_bank_account
    account_balance = frappe.get_all("GL Entry",
    filters={"account": ["in", account_name], type: document},
    fields=["debit", "credit"])
    credit_sum = 0.0
    debit_sum = 0.0
    for i in account_balance:
        credit_sum += i.credit
        debit_sum += i.debit
    return credit_sum, debit_sum

def get_projects_budget_amount(projects):
    projects_budget = []
    for i in projects:
        budgets = frappe.get_all("Budget",
                                  filters={"project": i,
                                           "budget_against": "project",
                                           "docstatus": 1},
                                  pluck="name")
        if budgets:
            amount = frappe.get_all("Budget Account",
                                     filters={"parent": [
                                         'in', budgets]},
                                     fields=["sum(budget_amount)"],
                                     as_list=True)[0][0]
            projects_budget.append(amount)
        else:
            projects_budget.append(0)

    return projects_budget

def get_project_budget(project):
    budget = frappe.get_all("Budget", filters={"project": project, "docstatus":1}, fields=["name",
     "applicable_on_employee_advance", "action_if_annual_budget_exceeded_on_actual_for_project"])
    if budget:
        return budget[0]
    else:
        return None

@frappe.whitelist()
def get_request_type_account(request_type, company):
    filed_name = "default_employee_covenant_account" if request_type=="Covenant" else "default_employee_advance_account"
    account = frappe.get_value("Company", company, filed_name)
    if account:
        return account
    else:
        return None


@frappe.whitelist()
def share_doc_with_approver(doc, user):
	# if approver does not have permissions, share
	if not frappe.has_permission(doc=doc, ptype="submit", user=user):
		frappe.share.add(doc.doctype, doc.name, user, submit=1,
			flags={"ignore_share_permission": True})

		frappe.msgprint(_("Shared with the user {0} with {1} access").format(
			user, frappe.bold("submit"), alert=True))

	# remove shared doc if approver changes
	doc_before_save = doc.get_doc_before_save()
	if doc_before_save:
		approvers = {
			"Leave Application": "leave_approver",
			"Expense Claim": "expense_approver",
			"Shift Request": "approver",
            "Employee Advance": "expense_approver",
            "Appraisal": "expense_approvers"
		}

		approver = approvers.get(doc.doctype)
		if doc_before_save.get(approver) != doc.get(approver):
			frappe.share.remove(doc.doctype, doc.name, doc_before_save.get(approver))
