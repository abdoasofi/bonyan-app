# Copyright (c) 2022, open-alt and contributors
# For license information, please see license.txt

from math import exp
import frappe
from frappe.model.document import Document
from frappe.utils import add_days
from dateutil import parser


class EmployeeExpenseEntry(Document):


    def on_submit(self):
        self.create_expenses()

    @frappe.whitelist()
    def get_attendace_employee(self):
        """
        this function for get employee
        """
        self.employes = None
        to_date = add_days(parser.parse(self.date), 1)
        filters = dict()

        filters["gender"] = "`emp`.`gender` = %(gender)s" if self.gender else " 1 = 1 "
        filters["department"] = "`emp`.`department` = %(department)s" if self.department else " 1 = 1 "


        attendance_employes = frappe.db.sql("""
            SELECT
                `emp`.`gender` AS `gender`,
                `emp`.`department` AS `department`,
                `emp`.`name` AS `employee`,
                `emp`.`employee_name` AS `employee_name`,
                "%(amount)s" AS `amount`,
                `emp_chk`.time as time
            FROM
                `tabEmployee Checkin` AS `emp_chk`,
                `tabEmployee` AS `emp`

            WHERE
               `emp`.`name` = `emp_chk`.`employee` AND
                {gender_filter} AND {department_filter} AND time >= %(date)s AND time < %(to_date)s
            GROUP BY employee
        """.format(gender_filter = filters["gender"], department_filter = filters["department"]),
            {
                "date": self.date,
                "to_date": to_date,
                "gender": self.gender,
                "department": self.department,
                "amount": self.amount
        }, as_dict = 1)
        for i in attendance_employes:
            self.append("employes", i)

    @frappe.whitelist()
    def create_expenses(self):
        """
        create expenses for all employes
        """
        for i in self.employes:
            expense = frappe.get_doc(
                {
                    "doctype": "Expense Claim",
                    "employee": i.employee,
                    "payable_account": self.payable_account,
                    "approval_status": "Approved",
                    "is_employee_expense_entry": True,
                    "expense_entry": self.name,
					"posting_date": self.date,
                    "remark": self.remark,
                    "expense_claim_request_type": self.expense_claim_request_type,
                }
            )
            expense.append(
                "expenses",
                {
                    "expense_date": self.date,
                    "expense_type": self.expense_claim_type,
                    "amount": i.amount,
                    "sanctioned_amount": i.amount,
                    "cost_center": self.cost_center
                },
            )

            expense.insert()
            if self.submit_expense_after_create:
                expense.submit()
