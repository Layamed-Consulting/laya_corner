from odoo import http
import xmlrpc.client
import json
from odoo.http import request


ODOO_URL = 'http://135.125.204.41:10018'
ODOO_DB = 'ChicCorner_Prod'
ODOO_USERNAME = 'mehdi.benjebara@outlook.com'


class ProductAPI(http.Controller):

    @http.route('/api/get_product_details', type='http', auth='none', methods=['GET'], csrf=False)
    def get_product_details(self, **kwargs):
        try:
            # Get the API key from the Authorization header
            api_key = request.httprequest.headers.get('Authorization')

            # Check if the API key is provided
            if not api_key:
                return http.Response(
                    json.dumps({'error': 'API key is missing in the request header'}),
                    status=403, content_type='application/json'
                )

            # Use XML-RPC to search for the API key in the correct database
            common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
            uid = common.authenticate(ODOO_DB, ODOO_USERNAME, api_key, {})
            if not uid:
                return http.Response(
                    json.dumps({'error': 'Unauthorized, invalid or inactive API key'}),
                    status=403, content_type='application/json'
                )

            models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')

            # Fetch product details
            products = models.execute_kw(
                ODOO_DB, uid, api_key, 'product.template', 'search_read',
                [[]],
                {'fields': [
                    'name', 'barcode', 'default_code', 'x_studio_item_id',
                    'standard_price', 'x_studio_hs_code', 'x_studio_origine_pays',
                    'x_studio_composition', 'detailed_type', 'invoice_policy',
                    'available_in_pos'
                ]}
            )

            product_data = []

            # Iterate over products
            for product in products:

                # Fetch supplier information for the product
                suppliers = models.execute_kw(
                    ODOO_DB, uid, api_key, 'product.supplierinfo', 'search_read',
                    [[('product_tmpl_id', '=', product['id'])]],
                    {'fields': ['display_name', 'price', 'currency_id']}
                )

                # Create supplier info list
                supplier_info = [
                    {
                        "Nom du fournisseur": supplier['display_name'] if 'display_name' in supplier and supplier['display_name'] else "not existe",
                        "Prix": supplier['price'] if 'price' in supplier and supplier['price'] else "0",
                        "Devise": supplier['currency_id'][1] if 'currency_id' in supplier and supplier['currency_id'] else ""
                    }
                    for supplier in suppliers
                ]

                # Fetch stock data for the product
                stock_records = models.execute_kw(
                    ODOO_DB, uid, api_key, 'stock.quant', 'search_read',
                    [[('product_id.product_tmpl_id', '=', product['id'])]],
                    {'fields': ['location_id', 'quantity']}
                )

                # Create stock quantities mapping
                stock_quantities = {}
                for stock in stock_records:
                    location_name = stock['location_id'][1] if 'location_id' in stock and stock['location_id'] else "Unknown Location"
                    stock_quantities[location_name] = stock['quantity']

                # Fetch product price from pricelist
                pricelist_items = models.execute_kw(
                    ODOO_DB, uid, api_key, 'product.pricelist.item', 'search_read',
                    [[('product_tmpl_id', '=', product['id'])]],
                    {'fields': ['fixed_price']}
                )

                # Get the price from the pricelist (if exists)
                product_price = pricelist_items[0]['fixed_price'] if pricelist_items else "Price not found"

                # Append product data to the list
                product_data.append({
                    "Nom du Produit": product.get('name') if product.get('name') else "",
                    "Code barre": product.get('barcode') if product.get('barcode') else "existe pas",
                    "default_code": product.get('default_code') if product.get('default_code') else "existe pas",
                    "Item ID": product.get('x_studio_item_id') if product.get('x_studio_item_id') else "existe pas",
                    "Cout": product.get('standard_price') if product.get('standard_price') else "existe pas",
                    "Prix de vente": product_price,  # Added product price from pricelist
                    "HS Code": product.get('x_studio_hs_code') if product.get('x_studio_hs_code') else "existe pas",
                    "Collection": product.get('x_studio_origine_pays') if product.get('x_studio_origine_pays') else "existe pas",
                    "Composition": product.get('x_studio_composition') if product.get('x_studio_composition') else "existe pas",
                    "Type de produit": product.get('detailed_type') if product.get('detailed_type') else "existe pas",
                    "Politique de fabrication": product.get('invoice_policy') if product.get('invoice_policy') else "existe pas",
                    "Disponible en POS": product.get('available_in_pos') if product.get('available_in_pos') else "0",
                    "Stock selon l'emplacement": stock_quantities,
                    "Informations fournisseur": supplier_info,

                })

            # Return the product data as JSON
            return http.Response(json.dumps(product_data, ensure_ascii=False), content_type='application/json')

        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), status=500, content_type='application/json')
