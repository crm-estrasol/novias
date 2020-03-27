from odoo import models, fields, api ,_
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import UserError, ValidationError
import sys
class Departent_Area(models.Model):
    _name= 'intelli.department.area'
    _inherit =  ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
   
    def _get_fall(self):
        fall = self.env['intelli.fall'].search([('name', '=', 'No aplica')], limit=1)
        if not fall:
             fall = self.env['intelli.fall'].create({'name':"No aplica"})
        return fall.id 
    def _get_control(self):
        control = self.env['intelli.control'].search([('name', '=', 'No aplica')], limit=1)
        if not control:
             control = self.env['intelli.control'].create({'name':"No aplica"})
        return control.id
    active = fields.Boolean('Active', default=True, track_visibility=True)
    name = fields.Char("Zona",track_visibility=True, required=True)
    with_w = fields.Float("Ancho",digits=(16, 2),track_visibility=True)
    heigth_h = fields.Float("Alto",digits=(16, 2),track_visibility=True) 
    area = fields.Many2one('intelli.area', string='Area',required=True)
    fall = fields.Many2one('intelli.fall', string='Tela',required=True,default=_get_fall)
    control = fields.Many2one('intelli.control', string='Control',required=True,default=_get_control)
    parent_department = fields.Many2one('intelli.department', string='Departamento',readonly=True,ondelete='cascade' )
    parent_tower = fields.Integer(related="parent_department.tower.id")
    blind = fields.Many2one('intelli.blind', string='Cortina',required=True )
    style = fields.Many2one('intelli.style', string='Estilo')
    def button_duplicate(self):
        self.copy()
        view_id = self.env.ref('intelli.department_view_form_associate').id
        view = {
            'name': ('Areas'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'intelli.department',
            'views':  [(view_id,'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context':dict(create = False ),
            'res_id': self.parent_department.id,
            
        }
        return view 
    def button_duplicate_no_open(self):
        self.copy()
   
    @api.onchange('style')
    def on_image(self):
       self.blind = False
       self.with_w = 0
       self.heigth_h = 0
    
    @api.onchange('with_w')
    def on_width(self):
        if self.with_w == 0:
           return 
        if self.with_w > self.blind.with_w:
            res = {}
            self.with_w = 0
            res['warning'] = {
                'title': _('Error'),
                'message': _('Excediste el ancho permitido, ancho maximo '+ str(self.blind.with_w)
)            }
            return res
    @api.onchange('heigth_h')
    def on_heigth(self):
        if self.heigth_h == 0:
           return 
        if self.heigth_h > self.blind.heigth_h:
            res = {}
            self.heigth_h = 0
            res['warning'] = {
                'title': _('Error'),
                'message': _('Excediste el alto permitido, alto maximo '+ str(self.blind.heigth_h))
            }
            return res