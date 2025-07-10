from odoo import http
from odoo.http import request

class ProductCatalogController(http.Controller):
    
    @http.route(['/product', '/product/page/<int:page>'], type='http', auth='public', website=True)
    def product_list(self, page=1, **kwargs):
        search_query = kwargs.get('search') or ''
        Product = request.env['product.template'].sudo()
        domain = []
        if search_query:
            domain.append(('name', 'ilike', search_query))
        per_page = 10
        total = Product.search_count(domain)
        pager = request.website.pager(
            url='/product',
            total=total,
            page=page,
            step=per_page,
            url_args={'search': search_query}
        )
        products = Product.search(domain, limit=per_page, offset=(page - 1) * per_page)
        return request.render('product_catalog.product_list_template', {
            'products': products,
            'pager': pager,
            'search': search_query,
        })
