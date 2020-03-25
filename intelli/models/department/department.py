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
    name = fields.Char("Departamento", track_visibility=True, size=20, required=True)
    map = fields.Image("Plano",track_visibility=True)
    instalation = fields.Many2one('intelli.instalation', string='Agente', required=True, default=_get_instalation)
    tower = fields.Many2one('intelli.tower', string='Torre', required=True)
    _sql_constraints = [
        ('unique_name_', 'unique (name)', 'EL nombre no debe repetirse!')
       
    ]

    #Boton
    def button_blinds(self):
       view_id = self.env.ref('intelli.tower_view_form_associate').id
       view = {
           'name': ('Persianas'),
           'view_type': 'form',
           'view_mode': 'form',
           'res_model': 'intelli.tower',
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
        news_blind = []
        for blind in self.blinds:
            blind_images = []
            for image in blind.images:
                new_image = image.copy({'parent_blind':False})
                blind_images.append( (4, new_image.id) )
            new_blind = blind.copy({'parent_tower':False})
            if blind.images:
                new_blind.write({'images':blind_images}  )
            news_blind.append( (4, new_blind.id) )
        if self.blinds:
            res.write({'blinds':news_blind}  )
        return res
    def button_duplicate(self):
       self.copy()


    @api.onchange('map')
    def on_image(self):
        if sys.getsizeof(self.map)  > 1*1000*1000:      
            raise UserError(_("Exediste el tamaño permitido (1mb/10000) para la imagen ."))
   
    """
    def open_one2many_line(self):
        context = self.env.context
        return {
            'type': 'ir.actions.act_window',
            'name': 'Open Line',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': context.get('default_active_id'),
            'target': 'new',
        }}
    """

   