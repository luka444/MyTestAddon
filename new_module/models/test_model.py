from odoo import api, fields, models


class TestModel(models.Model):
    _name = "test.model"
    _description = "Test Model"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char()
    description = fields.Text()
    user_id = fields.Many2one(comodel_name="res.users")
    is_admin_user = fields.Boolean(compute="_compute_is_admin_user", store=True)
    leave_ids = fields.Many2many(
        comodel_name="hr.leave", 
        compute="_compute_leave_ids",
        readonly=False,
        domain="[('employee_id', '=', employee_id)]",
    )
    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        compute="_compute_employee_id",
    )
    story_point = fields.Integer()
    is_manager = fields.Boolean(compute="_compute_is_manager")

    @api.depends_context("uid")
    def _compute_is_manager(self):
        self.is_manager = self.env.user.has_group("new_module.new_module_manager")

    def _compute_employee_id(self):
        for rec in self:
            rec.employee_id = rec.user_id.employee_id if rec.user_id else False

    def _compute_leave_ids(self):
        for rec in self:
            active_leaves = self.env["hr.leave"].search([("user_id", "=", rec.user_id.id)])
            rec.leave_ids = active_leaves

    @api.depends("user_id")
    def _compute_is_admin_user(self):
        for rec in self:
            is_admin = rec.user_id.groups_id.filtered(lambda s: s.name == "Access Rights" and s.category_id.name == "Administration")
            if is_admin:
                rec.is_admin_user = True
            else:
                rec.is_admin_user = False

    def open_change_users_wizard(self):
        return {
            "name": "Change Users",
            "type": "ir.actions.act_window",
            "res_model": "test.model.mass.change.users.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"active_ids": self.ids},
        }
