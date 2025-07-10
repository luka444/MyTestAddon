from odoo import fields, models
import pandas as pd
import tempfile
from odoo.exceptions import UserError
import base64


class ImportTestWizard(models.TransientModel):
    _name = "import.test.wizard"
    _description = "Import Test Wizard"

    file = fields.Binary(string="File")
    file_name = fields.Char(string="File Name")

    def action_import(self):
        if not self.file:
            raise UserError("Please select a file to import.")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx").name
        with open(temp_file, "wb") as f:
            f.write(base64.b64decode(self.file))
        try: 
            df = pd.read_excel(temp_file)
        except Exception as e:
            raise UserError(f"Error reading file: {str(e)}")
        for  _, row in df.iterrows():
            vals = {
                'name': row.get('name'),
                'description': row.get('description'),
                'user_id': row.get('user_id'),
            }
            self.env['test.model'].create(vals)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Records imported successfully!',
                'type': 'success',
                'sticky': False,
            }
        }
