from lib.controller.product_product import ProductProduct as ProductProductController
from lib.model.product_product import ProductProduct as ProductProductModel
from lib.sync.sync_helper import SyncHelper
from datetime import datetime
from pytz import timezone
import pytz

class ProductProduct(SyncHelper):
    
    def __init__(self, controller):
        super(ProductProduct, self).__init__(controller)
        #self.controller = controller
        self.model_name = 'product.product'
        self.productProductModel = ProductProductModel()
        self.productProductController = ProductProductController(self.controller)

    def sync(self):
        print("Sync Product Product")
        sync_process = self.getSyncProcessbyModelName(self.model_name)
        if sync_process:
            print(sync_process.last_sync)
            syncdate = sync_process.last_sync.astimezone(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
            form_data = {
                'syncdate': syncdate
            }
            requestHandling = self.api_post('/api/pos/v1.0/sync', form_data=form_data)
            if not requestHandling.err:
                for product_product in requestHandling.data:
                    print("Product Product")
                    print(product_product)
                    product = self.productProductController.getLocalById(product_product['id'])
                    if product:
                        for key in product_product:
                            print(product_product[key])
                            setattr(product, key, product_product[key])   
                        self.productProductController.updateLocal(product)
                    else:
                        product = ProductProductModel()
                        for key in product_product:
                            print(product_product[key])
                            setattr(product, key, product_product[key])                                   
                        self.productProductController.insertLocal(product)
                        
                self.updateSyncProcessTimeModel(self.model_name)

   