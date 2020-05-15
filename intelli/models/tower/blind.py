from odoo import models, fields, api ,_
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import UserError
import sys
from operator import itemgetter
import itertools
import operator
class Blind(models.Model):
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
    def _get_electronic(self):
        electronic = self.env['intelli.electronic'].search([('name', '=', 'No aplica')], limit=1)
        if not electronic:
             electronic = self.env['intelli.electronic'].create({'name':"No aplica"})
        return electronic.id
        
        
    _name= 'intelli.blind'
    _inherit =  ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    active = fields.Boolean('Active', default=True, track_visibility=True)
    code = fields.Char("Codigo",track_visibility=True, size=20, required=True)
    name = fields.Char("Nombre",track_visibility=True, required=True)
    style = fields.Many2one('intelli.style', string='Estilo',track_visibility=True,required=True,default=_get_style)
    with_w = fields.Float("Ancho max(W)",digits=(16, 3),track_visibility=True,required=True)
    heigth_h = fields.Float("Alto max(H)",digits=(16, 3),track_visibility=True, required=True)
    m2_max = fields.Float("M2 max",digits=(16, 3),track_visibility=True, required=True)
    price_size = fields.Float("Precio m2",digits=(16, 3),track_visibility=True, required=True)
    price =  fields.Float("Precio fijo",digits=(16, 3),track_visibility=True, required=True)
    #cloth_iamges =  iamgenes
    cloth = fields.Many2one('intelli.cloth', string='Tela',required=True,default=_get_cloth)
    blind = fields.Image("Imagen")
    actuation = fields.Many2one('intelli.actuation', string='Accionamiento',required=True,default=_get_actuation)
    electronic = fields.Many2one('intelli.electronic', string='Electrónica',required=True,default=_get_electronic)
    parent_tower =  fields.Many2one('intelli.tower', string='Torre',ondelete='cascade')
    images = fields.One2many (comodel_name='intelli.images',inverse_name='parent_blind',string="Imagenes")


    @api.onchange('blind')
    def on_blind(self):
        if sys.getsizeof(self.blind)  > 1*1000*1000:      
            raise UserError(_("Exediste el tamaño permitido (1mb/10000) para la imagen ."))
    
    #Boton
    def show_blind(self):
       view_id = self.env.ref('intelli.blind_view_form').id
       context = self.env.context
       view = {
           'name': (' Productos'),
           'view_type': 'form',
           'view_mode': 'form',
           'res_model': 'intelli.blind',
           'views':  [(view_id,'form')],
           'type': 'ir.actions.act_window',
           'target': 'new',
        'res_id':self.active_id,
           
       }
       return view 
   
    def button_duplicate_no_open(self):
        self.copy( {'name':self.name+"(copia)" })
    
    #WS
    def products_total(self,data_j):  
       
        data_j = sorted(data_j,  key=operator.itemgetter(0, 2))

        group_data = [ ( key ,sum( x[1] for x in list(group) )  )  for key, group in itertools.groupby(data_j,key=lambda x:( x[0], x[2] ) ) ]
        ids = [ id[0] for id in data_j  ] 
        ids = list(set(ids))
        search = self.env['intelli.blind'].search([('id','in',ids)])
        data = {}
        data['total_card'] = {'iva':0,'total':9,'delivery':0,'subtotal':0}
        data['products'] = []
        data['extra_products'] = []   
        data['video'] = self.env['ir.config_parameter'].sudo().get_param('intelli.url_video')
        data['policy'] = self.env['ir.config_parameter'].sudo().get_param('intelli.description')
        options_avaible =   [x.upper() for x in ['Control 1 Canal','Control 5 Canales','Cargador','Interfase'] ]
        count_products = 0
        for product in group_data:
            id = product[0][1]
            id_product =  product[0][0]
            #depa_area = self.env['intelli.department.area'].search([('id','=',id)])
            if id != -1:
                depa_area = self.env['intelli.department.area'].search([('id','=',id)])
                product_r = depa_area.products_ids.filtered(lambda x: x.id == id_product)
            else:
                product_r = self.env['intelli.blind'].search([('id','=', id_product )])

            if product_r :  
                key  ='extra_products' if product_r.name.upper() in options_avaible and product_r.style.name == 'Electrónica' else 'products'
                adjust = (depa_area.with_w*depa_area.heigth_h*product_r.price_size) if key != 'extra_products' else 0 
                total_product =  ( adjust + product_r.price ) * product[1]
                
                count_products += product[1] if key == "products" else 0
                iva = total_product * 0.16
                data[key].append({
                    'product_id': product_r.id,
                    'product':product_r.name,
                     'price':'{0:,.2f}'.format(total_product+iva),
                     'actuation':product_r.actuation.name,
                      'quantity':product[1]                  
                })     
                data['total_card']['subtotal'] += total_product
                data['total_card']['iva'] += iva
                   
        subtotal = data['total_card']['subtotal']
        iva = data['total_card']['iva']
        total = subtotal + iva
        data['total_card']['total'] =  '{0:,.2f}'.format( total )        
        data['total_card']['subtotal'] =  '{0:,.2f}'.format( subtotal )
        data['total_card']['iva'] =  '{0:,.2f}'.format( iva)
        
        delivery_price = search[0].parent_tower.delivery_price * count_products
        data['total_card']['delivery_price'] =  '{0:,.2f}'.format( delivery_price )
        instalation_price = search[0].parent_tower.instalation_price * count_products
        data['total_card']['instalation_price'] = '{0:,.2f}'.format( instalation_price )
        
        data['total_card']['total_delivery'] = '{0:,.2f}'.format( total+delivery_price)
        data['total_card']['total_instalation'] =  '{0:,.2f}'.format( total + instalation_price)

        
        return [  
                    {
                        
                            'success': 200 if search else 204,
                            'data': data  if search else "null"
                    }
                    ]
  
  
          

   