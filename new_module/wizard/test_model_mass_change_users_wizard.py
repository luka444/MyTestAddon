from odoo import fields, models


class TestModelMassChangeUsersWizard(models.TransientModel):
    _name = "test.model.mass.change.users.wizard"
    _description = "Test Model Mass Change Users Wizard"

    user_id = fields.Many2one(comodel_name="res.users")

    def apply_mass_change(self):
        records = self.env.context.get("active_ids")
        for_change_records = self.env["test.model"].browse(records)
        for_change_records.write({"user_id": self.user_id.id})
