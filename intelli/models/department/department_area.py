from odoo import models, fields, api ,_
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
from odoo.exceptions import UserError, ValidationError
import sys
import itertools
from operator import itemgetter

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
    fall = fields.Many2one('intelli.fall', string='Caída',required=True,default=_get_fall)
    control = fields.Many2one('intelli.control', string='Control',required=True,default=_get_control)
    parent_department = fields.Many2one('intelli.department', string='Departamento',readonly=True,ondelete='cascade' )
    parent_tower = fields.Integer(related="parent_department.tower.id")
    #blind = fields.Many2one('intelli.blind', string='Cortina',required=True )
    style = fields.Many2one('intelli.style', string='Estilo')
    products_ids = fields.Many2many(comodel_name='intelli.blind', relation='table_many_products', column1='blind_id', column2='', domain="['&',('parent_tower', '=', parent_tower),('style', '=', style)]")
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
       self.products_ids = False
    @api.onchange('with_w','heigth_h')
    def on_size(self):
       self.products_ids = False
  
    """
    @api.onchange('with_w')
    def on_width(self):
        if self.with_w == 0:
           return 
        m2_max = self.with_w * self.heigth_h
        if m2_max > self.blind.m2_max:
            res = {}
            self.with_w = 0
            self.heigth_h = 0
            
            res['warning'] = {
                'title': _('Error'),
                'message': _('Excediste  M2  permitido, m2 maximo '+ str(self.blind.m2_max)
                                )            
                                }
            return res

        if self.with_w > self.blind.with_w:
            res = {}
            self.with_w = 0
           
            
            res['warning'] = {
                'title': _('Error'),
                'message': _('Excediste el ancho permitido, ancho maximo '+ str(self.blind.with_w)
                                    )            }
            return res
   """
    @api.onchange('products_ids')
    def on_products_ids(self):
        products_not_a =""
        product_exced_w =""
        product_exced_h =""
        for product in self.products_ids:
           
            m2_max = self.with_w * self.heigth_h
            if m2_max > product.m2_max:
                res = {}
                self.products_ids = [(3,product.id)]    
                products_not_a += product.name+","
            elif self.with_w > product.with_w:
                res = {}
                self.products_ids = [(3,product.id)]    
                product_exced_w += product.name+","
            elif self.heigth_h > product.heigth_h:
                res = {}
                self.products_ids = [(3,product.id)]    
                product_exced_h += product.name+","

        if  products_not_a != "":
            res['warning'] = {
            'title': _('Error'),
            'message': _(' Producto(s) '+products_not_a+' exceden  M2  permitido.'
                                        )   }
            return res
        if  product_exced_w != "":
            res['warning'] = {
            'title': _('Error'),
            'message': _(' Producto(s) '+product_exced_w+' exceden  ancho(W)  permitido. '
                                        )   }
            return res
        if  product_exced_h != "":
            res['warning'] = {
            'title': _('Error'),
            'message': _(' Producto(s) '+product_exced_h+' exceden  alto(H) permitido. '
                                        )   }
            return res  
           
           
            #if self.heigth_h > self.blind.heigth_h:
            #    res = {}
            #    self.heigth_h = 0
            #    res['warning'] = {
            #        'title': _('Error'),
            #        'message': _('Excediste el alto permitido, alto maximo '+ str(self.blind.heigth_h))
            #    }
            #    return res


    def product_areas(self,id):  
       
        search = self.env['intelli.department.area'].search(['id','=',id], order='area asc, style asc ,name asc')
                
        data = []
        if search:
            for key, group in itertools.groupby(search, key=lambda x:( x['area'], x['style'] ) ):
                new_area = {
                                'area':key[0].name,
                            
                                'style':key[1].name,                    
                        }
                new_area['zones']= [    {
                                            'zone':key_z,
                                            'products': self._get_products(group_z)

                                        }        
                                        for key_z, group_z in itertools.groupby(group, key=lambda x: x['name']  )  ]           
                            
                data.append(new_area)
            
        
        data_end = {
            'areas': data,
            'extra_products':[]

        } if search else "null"     
        
     
        _logger.info("-----------------------------------"+str( data_end) )
        return [  
                    {
                        
                            'success': 200 if search else 204,
                            'data': data_end  if search else "null"
                    }
                    ]
    def _get_products(self,group):
         
        all_products = []
        for producs in group:
            for product  in producs.products_ids:           
                    all_products.append(
                    {
                         'product_id': product.id,
                         'product':product.name,
                         'price':product.price
                                      
                    }
                    )
                    

        return all_products