from odoo import models, fields, api ,_
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import UserError
import sys
class Department(models.Model):
    _name= 'intelli.department'
    _inherit =  ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
   
    def _get_instalation(self):
        instalation = self.env['intelli.instalation'].search([('name', '=', 'No aplica')], limit=1)
        if not instalation:
             instalation = self.env['intelli.instalation'].create({'name':"No aplica"})
        return instalation.id

    active = fields.Boolean('Active', default=True, track_visibility=True)
    name = fields.Char("Departamento", track_visibility=True, required=True)
    map = fields.Image("Plano",track_visibility=True)
    instalation = fields.Many2one('intelli.instalation', string='Instalación', required=True, default=_get_instalation)
    tower = fields.Many2one('intelli.tower', string='Torre', required=True,ondelete='cascade')
    department_areas = fields.One2many (comodel_name='intelli.department.area',inverse_name='parent_department',string="Areas")
    _sql_constraints = [
        ('unique_name_', 'unique (name)', 'EL nombre no debe repetirse!')
       
    ]

    #Boton
    def button_areas(self):
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
           'res_id': self.id,
           
       }
       return view 

    def copy(self, default=None):
        self.ensure_one()
        res = super(Department, self).copy({'name':self.name + "(copia)"})
        news_area = []
        for area in self.department_areas:    
            new_area = area.copy({'parent_department':False})
            news_area.append( (4, new_area.id) )
        if self.department_areas:
            res.write({'department_areas':news_area}  )
        return res
    
    def button_duplicate(self):
       self.copy()


    @api.onchange('map')
    def on_image(self):
        if sys.getsizeof(self.map)  > 1*1000*1000:      
            raise UserError(_("Exediste el tamaño permitido (1mb/10000) para la imagen ."))
   
   
   