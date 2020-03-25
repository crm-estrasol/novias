# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    url_video = fields.Char("Url youtube")

    
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            my_custom_field1_id = self.env['ir.config_parameter'].sudo().get_param('your_custom_module_name.my_custom_field1_id'),
            my_custom_field2_id = self.env['ir.config_parameter'].sudo().get_param('your_custom_module_name.my_custom_field2_id'),
        )
        return res

      def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            my_custom_field1_id = self.env['ir.config_parameter'].sudo().get_param('your_custom_module_name.my_custom_field1_id'),
            my_custom_field2_id = self.env['ir.config_parameter'].sudo().get_param('your_custom_module_name.my_custom_field2_id'),
        )
        return res
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        field1 = self.my_custom_field1_id and self.my_custom_field1_id.id or False
        field2 = self.my_custom_field2_id and self.my_custom_field2_id.id or False

        param.set_param('your_custom_module_name.my_custom_field1_id', field1)
        param.set_param('your_custom_module_name.my_custom_field2_id', field2)