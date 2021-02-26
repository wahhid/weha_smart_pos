class ServerFields():

    res_company = [ 'currency_id', 'email', 'website', 'company_registry', 
                'vat', 'name', 'phone', 'partner_id' , 'country_id', 
                'state_id', 'tax_calculation_rounding_method']

    decimal_precision = ['name','digits']

    uom_uom = []

    res_country_state = ['name', 'country_id']

    res_country =  ['name', 'vat_label', 'code']

    account_tax = ['name','amount', 'price_include', 
                'include_base_amount', 'amount_type', 
                'children_tax_ids']

    res_partner = ['name','street','city','state_id','country_id','vat',
                 'phone','zip','mobile','email','barcode','write_date',
                 'property_account_position_id','property_product_pricelist']

    pos_session = ['id', 'name', 'user_id', 'config_id', 'start_at', 'stop_at', 'sequence_number', 'payment_method_ids']

    pos_config = ['name', 'company_id', 'currency_id', 'pricelist_id']

    res_users = ['name','company_id', 'id', 'groups_id']

    product_pricelist = ['name', 'display_name', 'discount_policy']

    product_pricelist_item = []
    
    product_category =  ['name', 'parent_id']

    res_currency = ['name','symbol','position','rounding','rate']

    pos_category = ['id', 'name', 'parent_id', 'child_id']

    product_product =  ['display_name', 'lst_price', 'standard_price', 'categ_id', 'pos_categ_id', 'taxes_id',
                 'barcode', 'default_code', 'to_weight', 'uom_id', 'description_sale', 'description',
                 'product_tmpl_id','tracking']

    pos_payment_method = ['name', 'is_cash_count', 'use_payment_terminal']

    account_fiscal_position = []

    account_fiscal_position_tax = []



    
    