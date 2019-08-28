# -*- coding: utf-8 -*-

from odoo import models, fields, api
import os
import os.path
import json

# <editor-fold desc="changer backend code"
def debrand(new_odoo, new_color):
    # check if json file exists
    if os.path.isfile(json_file_name):
        # get company_name
        with open(json_file_name, 'r') as f:
            old_data_store = json.load(f)
        # use it(the company_name from json) as target
        # print(data_store["company_name"]," as target and ",new_odoo," as replacement")

        #debranding_parts(old_data_store["company_name"], new_odoo, new_color)
    #else:
        # use default string "Odoo" as target
        # print("odoo as target and ",new_odoo," as replacement")

        #debranding_parts('Odoo', new_odoo, new_color)

    # write changes
    data_store = {
        "company_name": new_odoo,
        "color": new_color
    }
    with open(json_file_name, 'w') as f:
        json.dump(data_store, f)
    return data_store
# </editor-fold>
# <editor-fold desc="changer config settings">
def get_x_company_name():  # get form json file
    data_store = {
        "company_name": 'Odoo',
        "color": '7C7BAD'
    }
    if os.path.isfile(json_file_name):
        with open(json_file_name, 'r') as f:
            data_store = json.load(f)

        return data_store
    else:
        return data_store


class changer_backend_config(models.TransientModel):
    _inherit = 'res.config.settings'

    x_company_name = fields.Char(string='Branding Name',
                                 store=True,
                                 readonly=False,
                                 required=True)
    x_color = fields.Char(string="Brand Color",
                          store=True,
                          readonly=False,
                          required=True)

    @api.model
    def get_values(self):
        res = super(changer_backend_config, self).get_values()
        data_values = get_x_company_name()
        res.update(
            x_company_name=data_values["company_name"],
            x_color=data_values["color"],
        )
        return res

    @api.multi
    def set_values(self):
        debrand(self.x_company_name, self.x_color)
        super(changer_backend_config, self).set_values()
        self.env.ref('res_config_settings_view_form').write({'x_company_name': self.x_company_name})
        self.env.ref('res_config_settings_view_form').write({'x_color': self.x_color})

# </editor-fold>

# class debranding-project(models.Model):
#     _name = 'debranding-project.debranding-project'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100