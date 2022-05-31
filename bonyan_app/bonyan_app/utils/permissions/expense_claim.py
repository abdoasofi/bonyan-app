import frappe


def expense_claim_entry_query(user):
    """
    this query to excludeing entry type expense cliam to specific Roles
    """
    return """
    (IFNULL(`is_employee_expense_entry`, '0') = '0' OR
        EXISTS
            (SELECT 1 FROM
                    `tabHas Role` AS `hs`
                INNER JOIN
                    `tabBonyan Settings Roles` AS `bsr`
                ON
                    `hs`.`role` = `bsr`.`role`
                WHERE
                    `hs`.`parent` = {user} AND
                    `hs`.`parentfield` = 'roles' AND
                    `hs`.`parenttype` = 'User' AND
                    `bsr`.`parentfield` = 'expence_claim_roles' AND
                    `bsr`.`parenttype` = 'Bonyan Settings'
            )
    )
    """.format(user=frappe.db.escape(user))
