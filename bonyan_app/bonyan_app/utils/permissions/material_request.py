import frappe


def material_request_query(user):
    """
    this query to limit material_request list by excludeing `Material Transfer`,
        `Manufacturing` ...etc to specific Roles
    """
    return """
    (`material_request_type` in ('Purchase', 'Material Issue') OR
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
                    `bsr`.`parentfield` = 'material_request_roles' AND
                    `bsr`.`parenttype` = 'Bonyan Settings'
            )
    )
    """.format(user=frappe.db.escape(user))
