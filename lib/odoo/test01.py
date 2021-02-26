import odoorpc

# Prepare the connection to the server
odoo = odoorpc.ODOO('178.128.51.74', port=8069)

# Check available databases
print(odoo.db.list())

# Login
odoo.login('pos-dev', 'admin', 'pelang1')

# Current user
user = odoo.env.user
print(user.name)            # name of the user connected
print(user.company_id.name) # the name of its company

# Simple 'raw' query
#user_data = odoo.execute('res.users', 'read', [user.id])
#print(user_data)

if 'product.product' in odoo.env:
    Product = odoo.env['product.product']
    product_ids = Product.search([('name','=','Voucher')])
    for product in Product.browse(product_ids):
        print(product.name)