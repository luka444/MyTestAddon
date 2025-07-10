from odoo import http
from odoo.http import request

class ProductCatalogController(http.Controller):
    
    @http.route(['/product', '/product/page/<int:page>'], type='http', auth='public', website=True)
    def product_list(self, page=1, **kwargs):
        Product = request.env['product.template'].sudo()
        per_page = 10
        total = Product.search_count([])
        pager = request.website.pager(
            url='/product',
            total=total,
            page=page,
            step=per_page,
        )
        products = Product.search([], limit=per_page, offset=(page - 1) * per_page)
        return request.render('product_catalog.product_list_template', {
            'products': products,
            'pager': pager,
        })
