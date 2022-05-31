from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import (
    cint,
    date_diff,
    flt,
)
import erpnext
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry
from erpnext.hr.doctype.expense_claim.expense_claim import update_reimbursed_amount



class CustomPaymentEntry(PaymentEntry):
    """
    this is override custom payment entry
    """
    def set_missing_values(self):
        """
        this is override party type
        """
        if not self.is_employee_expense_entry:
            return super().set_missing_values()

    def add_party_gl_entries(self, gl_entries):
        if not self.is_employee_expense_entry:
            return super().add_party_gl_entries(gl_entries)
        if self.party_account:
            against_account = self.paid_from

            party_gl_dict = self.get_gl_dict({
                "account": self.party_account,

                "against": against_account,
                "account_currency": self.party_account_currency,
                "cost_center": self.cost_center
            }, item=self)

            dr_or_cr = "credit" if erpnext.get_party_account_type(self.party_type) == 'Receivable' else "debit"

            for d in self.get("references"):
                cost_center = self.cost_center
                if d.reference_doctype == "Sales Invoice" and not cost_center:
                    cost_center = frappe.db.get_value(d.reference_doctype, d.reference_name, "cost_center")
                party = frappe.db.get_value(d.reference_doctype, d.reference_name, 'employee')
                gle = party_gl_dict.copy()
                gle.update({
                    "against_voucher_type": d.reference_doctype,
                    "against_voucher": d.reference_name,
                    "party_type": 'Employee',
                    "party": party,
                    "cost_center": cost_center
                })

                allocated_amount_in_company_currency = flt(flt(d.allocated_amount) * flt(d.exchange_rate),
                    self.precision("paid_amount"))

                gle.update({
                    dr_or_cr + "_in_account_currency": d.allocated_amount,
                    dr_or_cr: allocated_amount_in_company_currency
                })

                gl_entries.append(gle)

            if self.unallocated_amount:
                exchange_rate = self.get_exchange_rate()
                base_unallocated_amount = (self.unallocated_amount * exchange_rate)

                gle = party_gl_dict.copy()

                gle.update({
                    dr_or_cr + "_in_account_currency": self.unallocated_amount,
                    dr_or_cr: base_unallocated_amount
                })

                gl_entries.append(gle)


    def validate_reference_documents(self):
        """
        validate
        """
        if not self.is_employee_expense_entry:
            return super().validate_reference_documents()

    @frappe.whitelist()
    def get_employee_expenses_entry(self):
        expenses = frappe.get_list('Expense Claim', filters={'expense_entry': self.employee_expense_entry, 'docstatus': 1, 'is_paid': 0}, fields=['name', 'grand_total'])
        self.references = None

        for i in expenses:
           expense = {
               'reference_doctype': 'Expense Claim',
               'reference_name': i.name,
               'total_amount': i.grand_total,
               'outstanding_amount': i.grand_total,
               'allocated_amount': i.grand_total,
               'exchange_rate': 1,
           }
           self.append('references', expense)

        self.set_amounts()


    def update_expense_claim(self):
        if not self.is_employee_expense_entry:
            return super().update_expense_claim()
        if self.payment_type in ("Pay"):
            for d in self.get("references"):
                if d.reference_doctype=="Expense Claim" and d.reference_name:
                    doc = frappe.get_doc("Expense Claim", d.reference_name)
                    if self.docstatus == 2:
                        update_reimbursed_amount(doc, -1 * d.allocated_amount)
                    else:
                        update_reimbursed_amount(doc, d.allocated_amount)
