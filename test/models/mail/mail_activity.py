# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from odoo.tools.misc import clean_context
class NoviasMailActivity(models.Model):
    _inherit = "mail.activity"
    selection_actividades = fields.Selection([('var','Fecha prueba'),('var2','Ajuste taller')],string="Actividad") 
    flagsh_shedule = fields.Boolean() 
    flagdeliv_shedule = fields.Boolean()
    test_date = fields.Datetime('Fecha prueba',tracking=True) 
    #ON BUTTON ACTIONS
    def action_confirm_sheddule(self):
        sale = self.env["sale.order"].search([('id','=',self.res_id)])
        sale.shedule_confirm = 1 

        return  {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                }
    def action_sheddule_fth(self):
            sale = self.env["sale.order"].search([('id','=',self.res_id)])
            stages = self.env["crm.stage"].search([('name','like','Apartado(Reservado)')])
            
            sale.date_sheddule = self.test_date
            sale.opportunity_id.stage_id = stages[0].id
            self.flagsh_shedule = 0
            #_logger.info("-----------------------------------"+str(self.env.user.warehouse_id.name ) )
            user = self.env['res.users'].search( [('id','=',self.env.user.id)] )
            context = self._context

            current_uid = context.get('uid')

            user = self.env['res.users'].browse(current_uid)
            #_logger.info("-----------------------------------"+str(user.name) )               
            #_logger.info("-----------------------------------"+str(cr.dictfetchall() ) )  
            #_logger.info("-----------------------------------"+str(cr.fetchall()) )
            return  {
                        'type': 'ir.actions.client',
                        'tag': 'reload',
                    }
    def action_sheddule_scd(self):
            sale = self.env["sale.order"].search([('id','=',self.res_id)])
            stages = self.env["crm.stage"].search([('name','like','Taller(Correcciones)')])
            sale.opportunity_id.stage_id = stages[0].id
            sale.date_workshop = self.test_date
            sale.comment_workshop = self.note
            self.flagdeliv_shedule = 0 
            #s
            
            template_id = self.env.ref('test.mail_template_sheddule_work').id
            lang = self.env.context.get('lang')
            template = self.env['mail.template'].browse(template_id)
            taller = self.env["res.partner"].search([('name','like','Taller')])
            if template.lang:
                lang = template._render_template(template.lang, 'sale.order', sale.id)
            ctx = {
                'default_model': 'sale.order',
                'default_res_id': sale.id,
                'default_use_template': bool(template_id),
                'default_template_id': template_id,
                'default_composition_mode': 'comment',
                'default_partner_ids': [(4, taller.id)],
                'mark_so_as_sent': True,
                'proforma': self.env.context.get('proforma', False),
                'force_email': True,
                'model_description': sale.with_context(lang=lang).type_name,
            }
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'mail.compose.message',
                'views': [(False, 'form')],
                'view_id': False,
                'target': 'new',
                'context': ctx,
            }
            #template_id = self.env.ref('test.mail_template_sheddule_work').id
            #template =self.env['mail.template'].browse(template_id)
            #template.send_mail(sale.id, force_send=True)
            #return  {
            #            'type': 'ir.actions.client',
            #            'tag': 'reload',
            #       }
    #ON BUTTON ACTIONS END
    #ON CHANGE
    @api.onchange('test_date')
    def _on_test_date(self):
      if self.test_date:

        self.date_deadline = self.test_date.strftime('%Y-%m-%d')