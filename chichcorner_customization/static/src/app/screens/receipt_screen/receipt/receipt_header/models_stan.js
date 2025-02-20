/** @odoo-module */
import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    setup(_defaultObj, options) {
        super.setup(...arguments);
        this.stan = this.stan || null;
        this.identite_number = this.identite_number || null;
        this.cheque_number = this.cheque_number || null;
        this.banque = this.banque || null;
        this.cheque_date = this.cheque_date || null;
    },
    init_from_JSON(json) {
        this.set_stan(json.stan);
        this.set_identite_number(json.identite_number);
        this.set_cheque_number(json.cheque_number);
        this.set_banque_name(json.banque);
        super.init_from_JSON(...arguments);
        this.set_cheque_date(json.cheque_date);
    },
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        if (json) {
            json.stan = this.get_stan();
            json.identite_number = this.get_identite_number();
            json.cheque_number = this.get_cheque_number();
            json.banque = this.get_banque_name();
            json.cheque_date = this.get_cheque_date();
        }
        return json;
    },
    set_stan(stan) {
        this.stan = stan;
    },
    get_stan() {
        return this.stan;
    },
    set_identite_number(identite_number) {
        this.identite_number = identite_number;
    },
    set_cheque_date(cheque_date) {
        this.cheque_date = cheque_date;
    },
     get_cheque_date() {
        return this.cheque_date;
    },

    get_identite_number() {
        return this.identite_number;
    },

    set_cheque_number(cheque_number) {
        this.cheque_number = cheque_number;
    },

    get_cheque_number() {
        return this.cheque_number;
    },

    set_banque_name(banque) {
        this.banque = banque;
    },

    get_banque_name() {
        return this.banque;
    },
});
