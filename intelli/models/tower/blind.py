from odoo import models, fields, api ,_
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import UserError
import sys
from operator import itemgetter
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
    with_w = fields.Float("Ancho max(W)",digits=(16, 2),track_visibility=True,required=True)
    heigth_h = fields.Float("Alto max(H)",digits=(16, 2),track_visibility=True, required=True)
    m2_max = fields.Float("M2 max",digits=(16, 2),track_visibility=True, required=True)
    price_size = fields.Float("Precio m2",digits=(16, 2),track_visibility=True, required=True)
    price =  fields.Float("Precio fijo",digits=(16, 2),track_visibility=True, required=True)
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
    #WS
    def products_total(self,data_j):  
        #data_j = sorted(data_j, key=itemgetter(1))
        data_j = data_j
        ids = [ id[0] for id in data_j  ]
        
    
        search = self.env['intelli.blind'].search([('id','in',ids)])
        
        for product in data_j:
            value = search.filtered(lambda product_l: product_l.id == product[0])
            #val
            if len(value) == 1:
                product.append( value  )


        data = {}
        data['total_card'] = {'iva':0,'total':9,'delivery':0,'subtotal':0}
        data['products'] = []


        for product in data_j:           
              for prod in range(product[1]):  
                    total_product =  (product[2].with_w*product[2].heigth_h*product[2].price_size) + product[2].price 
                    iva = total_product * 0.16
                    data['products'].append({
                         'product_id': product[2].id,
                         'product':product[2].name,
                         'price':'{0:.2f}'.format(total_product+iva),
                         'actuation':product[2].actuation.name
                                       
                    })     
                    data['total_card']['subtotal'] += total_product
                    data['total_card']['iva'] += iva

        data['total_card']['total'] =  '{0:.2f}'.format( data['total_card']['subtotal'] +   data['total_card']['iva'] )       
        data['total_card']['subtotal'] =  '{0:.2f}'.format( data['total_card']['subtotal'] )
        data['total_card']['iva'] =  '{0:.2f}'.format( data['total_card']['iva'] )
        return [  
                    {
                        
                            'success': 200 if search else 204,
                            'data': data  if search else "null"
                    }
                    ]
    
          

   