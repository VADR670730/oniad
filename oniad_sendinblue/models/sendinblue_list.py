# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

from ..sendinblue.web_service import SendinblueWebService

class SendinblueList(models.Model):
    _name = 'sendinblue.list'
    _description = 'Sendinblue List'    
    
    sendinblue_id = fields.Char(        
        string='Sendinblue Id'
    )
    name = fields.Char(        
        string='Name'
    )
    total_blacklisted = fields.Integer(        
        string='Total blacklisted'
    )
    total_subscribers = fields.Integer(        
        string='Total subscribers'
    )
    sendinblue_folder_id = fields.Many2one(
        comodel_name='sendinblue.folder',
        string='Sendinblue Folder'
    )
    
    @api.model    
    def cron_get_lists(self):
        sendinblue_web_service = SendinblueWebService(self.env.user.company_id, self.env)
        return_get_lists = sendinblue_web_service.get_lists()
        if return_get_lists['errors'] == False:
            if return_get_lists['response'].count > 0:
                for list_item in return_get_lists['response'].lists:
                    sendinblue_list_ids = self.env['sendinblue.list'].search(
                        [
                            ('sendinblue_id', '=', list_item['id'])
                        ]
                    )
                    # sendinblue_folder_id
                    sendinblue_folder_id = 0
                    sendinblue_folder_ids = self.env['sendinblue.folder'].search(
                        [
                            ('sendinblue_id', '=', list_item['folderId'])
                        ]
                    )
                    if sendinblue_folder_ids:
                        sendinblue_folder_id = sendinblue_folder_ids[0]['id']
                        
                    if sendinblue_list_ids:
                        sendinblue_list_obj = sendinblue_list_ids[0]
                        
                        sendinblue_list_obj.update({
                            'sendinblue_id': list_item['id'],
                            'name': list_item['name'],
                            'total_blacklisted': list_item['totalBlacklisted'],
                            'total_subscribers': list_item['totalSubscribers'],
                            'sendinblue_folder_id': sendinblue_folder_id,
                        })                        
                    else:
                        vals = {
                            'sendinblue_id': list_item['id'],
                            'name': list_item['name'],
                            'total_blacklisted': list_item['totalBlacklisted'],
                            'total_subscribers': list_item['totalSubscribers'],
                            'sendinblue_folder_id': sendinblue_folder_id                                                                                                                 
                        }                        
                        self.env['sendinblue.list'].sudo().create(vals)