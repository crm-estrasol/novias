from odoo import models, fields, api ,_
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import UserError
import sys
class Tower(models.Model):
    _name= 'intelli.tower'
    _inherit =  ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
   
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'MX')], limit=1)
        return country


    active = fields.Boolean('Active', default=True, track_visibility=True)
    name = fields.Char("Nombre", track_visibility=True, size=20, required=True)
    street = fields.Char("Calle 1",track_visibility=True, size=50, required=True)
    street2 = fields.Char("Calle 2",track_visibility=True, size=50)
    location  = fields.Char("Locación",track_visibility=True, size=30)
    zip = fields.Char("Codigo postal",change_default=True,track_visibility=True, size=10, required=True)
    city = fields.Char("Ciudad",track_visibility=True, size=20, required=True)
    #email = fields.Char("Email")
    state_id = fields.Many2one("res.country.state", string='Estado', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Pais', ondelete='restrict', default=_get_default_country)
    tower_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    tower_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))
    #
    instalation_price = fields.Float("Instalación por pieza",digits=(16, 2),track_visibility=True)
    delivery_price = fields.Float("Envio por pieza",digits=(16, 2),track_visibility=True)
    password = fields.Char("Contrato",track_visibility=True, size=20, required=True)
    tower_picture = fields.Image("Imagen torre",required=True,track_visibility=True)
    background_picture = fields.Image("Imagen fondo",required=True,track_visibility=True)
    logo = fields.Image("Logo",track_visibility=True)
    agent = fields.Many2one('res.partner', string='Agente', index=True,required=True)
    email_agent = fields.Char(related='agent.email', readonly=True, string='Email',track_visibility=True)
    currency_id = fields.Many2one("res.currency", string="Tipo cambio",required=True,track_visibility=True)
    blinds = fields.One2many (comodel_name='intelli.blind',inverse_name='parent_tower',string="Persianas")
    _sql_constraints = [
        ('unique_name', 'unique (name)', 'EL nombre no debe repetirse!')
       
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
        res = super(Tower, self).copy({'name':self.name + "(copia)"})
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


    @api.onchange('logo')
    def on_image(self):
        if sys.getsizeof(self.logo)  > 1*1000*1000:      
            raise UserError(_("Exediste el tamaño permitido (1mb/10000) para la imagen ."))
    @api.onchange('tower_picture')
    def on_tower_picture(self):
        if sys.getsizeof(self.tower_picture)  > 1*1000*1000:          
            raise UserError(_("Exediste el tamaño permitido (1mb/10000) para la imagen ."))
    @api.onchange('background_picture')
    def on_background_picture(self):
        if sys.getsizeof(self.background_picture)  > 1*1000*1000:         
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