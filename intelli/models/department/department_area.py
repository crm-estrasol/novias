from odoo import models, fields, api ,_
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import UserError
import sys
class Departent_Area(models.Model):
    def _get_style(self):
        style = self.env['intelli.style'].search([('name', '=', 'No aplica')], limit=1)
        if not style:
             style = self.env['intelli.style'].create({'name':"No aplica"})
        return style.id
    def _get_cloth(self):
        cloth = self.env['intelli.cloth'].search([('name', '=', 'No aplica')], limit=1)
        if not cloth:
             cloth = self.env['intelli.cloth'].create({'name':"No aplica"})
        return cloth.id
    def _get_actuation(self):
        actuation = self.env['intelli.actuation'].search([('name', '=', 'No aplica')], limit=1)
        if not actuation:
             actuation = self.env['intelli.actuation'].create({'name':"No aplica"})
        return actuation.id
    
        
        
    _name= 'intelli.blind'
    _inherit =  ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    active = fields.Boolean('Active', default=True, track_visibility=True)
    code = fields.Char("Codigo",track_visibility=True, size=20, required=True)
  
   
    with_w = fields.Float("Ancho max(W)",digits=(16, 2),track_visibility=True,required=True)
    heigth_h = fields.Float("Alto max(H)",digits=(16, 2),track_visibility=True, required=True)
    
    cloth = fields.Many2one('intelli.cloth', string='Tela',required=True,default=_get_cloth)
   