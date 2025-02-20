/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";

patch(PosStore.prototype, {
   getReceiptHeaderData() {
       const order = this.get_order();
       const product = order.get_orderlines()?.[0]?.get_product(); // get the first product in orderlines
       return {
           ...super.getReceiptHeaderData(...arguments),
           partner: this.get_order().get_partner(),
           default_code: product ? product.default_code : null,
       };
   },
});