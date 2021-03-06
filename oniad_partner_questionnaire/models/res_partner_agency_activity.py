# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResPartnerAgencyActivity(models.Model):
    _name = 'res.partner.agency.activity'
    _description = 'Res Partner Agency Activity'

    name = fields.Char(
        string="Name"
    )
