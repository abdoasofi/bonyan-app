from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import (
    cint,
    date_diff,
    flt,
)
from erpnext.hr.doctype.leave_application.leave_application import get_holidays

from erpnext.hr.doctype.leave_application.leave_application import (
    LeaveApplication,
    get_leave_balance_on,
    is_lwp,
)

import datetime

class CustomLeaveApplication(LeaveApplication):
    """
    this custom class for custom leave applicion
    """

    def validate_balance_leaves(self):
        if self.from_date and self.to_date:
            self.total_leave_days = get_number_of_leave_days(
                self.employee,
                self.leave_type,
                self.from_date,
                self.to_date,
                self.half_day,
                self.is_furlough,
                self.half_day_date,
                hours_furlough=self.hours_furlough,
                from_time=self.from_time,
                to_time=self.to_time
                
            )
            if self.total_leave_days <= 0:
                frappe.throw(
                    _(
                        "The day(s) on which you are applying for leave are holidays. You need not apply for leave. %s"
                        %  self.total_leave_days
                    )
                )

            if not is_lwp(self.leave_type):
                self.leave_balance = get_leave_balance_on(
                    self.employee,
                    self.leave_type,
                    self.from_date,
                    self.to_date,
                    consider_all_leaves_in_the_allocation_period=True,
                )
                if self.status != "Rejected" and (
                    self.leave_balance < self.total_leave_days or not self.leave_balance
                ):
                    if frappe.db.get_value(
                        "Leave Type", self.leave_type, "allow_negative"
                    ):
                        frappe.msgprint(
                            _(
                                "Note: There is not enough leave balance for Leave Type {0}"
                            ).format(self.leave_type)
                        )
                    else:
                        frappe.throw(
                            _(
                                "There is not enough leave balance for Leave Type {0}"
                            ).format(self.leave_type)
                        )


@frappe.whitelist()
def get_number_of_leave_days(
    employee,
    leave_type,
    from_date,
    to_date,
    half_day=None,
    is_furlough=None,
    half_day_date=None,
    holiday_list=None,
    hours_furlough=None,
    from_time=None,
    to_time=None
):
    number_of_days = 0
    if cint(half_day) == 1 and not is_furlough:
        if from_date == to_date:
            number_of_days = 0.5
        elif half_day_date and half_day_date <= to_date:
            number_of_days = date_diff(to_date, from_date) + 0.5
        else:
            number_of_days = date_diff(to_date, from_date) + 1
    elif is_furlough:
        working_hours_on_day = get_shift_hours_daily(employee, from_date, to_date)
        hours_furlough = get_hours(to_time, from_time)
        number_of_days = date_diff(to_date, from_date) + (
            flt(hours_furlough) / working_hours_on_day
        )
    else:
        number_of_days = date_diff(to_date, from_date) + 1
    if not frappe.db.get_value("Leave Type", leave_type, "include_holiday"):

        number_of_days = flt(number_of_days) - flt(
            get_holidays(employee, from_date, to_date, holiday_list=holiday_list)
        )
    return number_of_days


def get_shift_hours_daily(employee, from_date, to_date):
    """
    check if employee has shift assingment bettween from date to date
    else return default shift and get working hours
    """
    assign_shift = frappe.get_list(
        "Shift Assignment",
        filters={
            "docstatus": 1,
            "employee": employee,
            "start_date": ["<=", from_date],
            "end_date": [">=", to_date],
        },
        fields=["shift_type"],
    )
    if assign_shift:
        shift = frappe.get_doc("Shift Type", assign_shift[0]["shift_type"])
        return shift.working_hours_per_day
    else:
        employee = frappe.get_doc("Employee", employee)
        if employee.default_shift:
            shift = frappe.get_doc("Shift Type", employee.default_shift)
            return shift.working_hours_per_day
    return 8



def get_hours(to_time, from_time):
    """
    this is fun for hours
    """
    if to_time and from_time:

        FMT = '%H:%M:%S'
        tdelta = datetime.datetime.strptime(str(to_time), FMT) - datetime.datetime.strptime(str(from_time), FMT)
        return flt(tdelta.seconds/ (60*60))
    else:
        return None