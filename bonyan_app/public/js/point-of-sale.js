pos_on_page_load = frappe.pages["point-of-sale"].on_page_load
pos_refresh = frappe.pages["point-of-sale"].refresh

frappe.pages["point-of-sale"].on_page_load = function(wrapper){
  x = pos_on_page_load.call(this, wrapper);
  repeat_work(setItemCart, 3000);
  return x;
}

frappe.pages["point-of-sale"].refresh = function(wrapper){
  repeat_work(set_pos_cart, 3000);
  repeat_work(set_pos_payment, 3000);
  
  if (pos_refresh){
    return pos_refresh.call(this, wrapper)
  }
}

function repeat_work(callback, timeout = 5000){
  if (callback()){
    setTimeout(() => {repeat_work(callback, timeout)}, timeout);
  }
}

function setItemCart(){
  if (erpnext.PointOfSale.ItemCart){
    erpnext.PointOfSale.ItemCart.prototype.render_cart_item = render_cart_item;
    let old_make_customer_selector = erpnext.PointOfSale.ItemCart.prototype.make_customer_selector;
    erpnext.PointOfSale.ItemCart.prototype.make_customer_selector = function(){
      old_make_customer_selector.apply(this);
      set_customer_button.apply(this);
    };

    return false;
  }
  else {
    return true;
  }
}

function set_pos_payment(){
  if (frappe.pages['point-of-sale'].pos && frappe.pages['point-of-sale'].pos.payment){
    frappe.pages['point-of-sale'].pos.payment.$component.off('click', '.submit-order-btn');
    frappe.pages['point-of-sale'].pos.payment.$component.on('click', '.submit-order-btn', complete_order);
    return false;
  }
  else {
    return true;
  }
}

function set_pos_cart(){
  if (frappe.pages['point-of-sale'].pos && frappe.pages['point-of-sale'].pos.cart){
    frappe.pages['point-of-sale'].pos.cart.reset_customer_selector();
    frappe.pages['point-of-sale'].pos.cart.$component.off('click', '.checkout-btn');
    frappe.pages['point-of-sale'].pos.cart.$component.on('click', '.checkout-btn', checkout_order);
    return false;
  }
  else {
    return true;
  }
}


function set_customer_button(){
  $(".customer-section").prepend("<button type='button' class='btn btn-primary btn-xs' onclick='set_customer()'>" +
  __("Scan Customer Barcode") + "</button>");
}

function set_customer(){
  let customer_field = "Customer"
  let scanner = new frappe.ui.Scanner({
            dialog: true, // open camera scanner in a dialog
            multiple: false, // stop after scanning one value
            on_scan(data) {
              handle_scanned_customer(customer_field, data.decodedText);
            }
       });
}

function handle_scanned_customer(customer_field, decodedText){

  let field = document.querySelector("[data-target=" + customer_field + "]");
  frappe.db.get_value("Customer", {"id": ["Like", "%data-barcode-value=_" + decodedText + "%"]}, "name").then((r) => {
    if (r.message.name){
       field.value = r.message.name;
       field.focus();
       field.blur();
    }
    else {
      frappe.db.get_value("Customer", {"id": decodedText}, "name").then((r) => {
        if (r.message.name){
           field.value = r.message.name;
           field.focus();
           field.blur();
        }
        else {
          frappe.msgprint(__("No Customer has Barcode: ") + decodedText)
        }
      });
    }
  });
}


function render_cart_item(item_data, $item_to_update) {
	const currency = this.events.get_frm().doc.currency;
	const me = this;
	item_data.qty = get_qty(this.customer_info, item_data);
	if (!$item_to_update.length) {
		this.$cart_items_wrapper.append(
			`<div class="cart-item-wrapper" data-row-name="${escape(item_data.name)}"></div>
			<div class="seperator"></div>`
		)
		$item_to_update = this.get_cart_item(item_data);
	}
	$item_to_update.html(
		`${get_item_image_html()}
		<div class="item-name-desc">
			<div class="item-name">
				${item_data.item_name}
			</div>
			${get_description_html()}
		</div>
		${get_rate_discount_html()}`
	)

	set_dynamic_rate_header_width();

	function set_dynamic_rate_header_width() {
		const rate_cols = Array.from(me.$cart_items_wrapper.find(".item-rate-amount"));
		me.$cart_header.find(".rate-amount-header").css("width", "");
		me.$cart_items_wrapper.find(".item-rate-amount").css("width", "");
		let max_width = rate_cols.reduce((max_width, elm) => {
			if ($(elm).width() > max_width)
				max_width = $(elm).width();
			return max_width;
		}, 0);

		max_width += 1;
		if (max_width == 1) max_width = "";

		me.$cart_header.find(".rate-amount-header").css("width", max_width);
		me.$cart_items_wrapper.find(".item-rate-amount").css("width", max_width);
	}

	function get_rate_discount_html() {
		if (item_data.rate && item_data.amount && item_data.rate !== item_data.amount) {
			return `
				<div class="item-qty-rate">
					<div class="item-qty"><span>${item_data.qty || 0}</span></div>
					<div class="item-rate-amount">
						<div class="item-rate">${format_currency(item_data.amount, currency)}</div>
						<div class="item-amount">${format_currency(item_data.rate, currency)}</div>
					</div>
				</div>`
		} else {
			return `
				<div class="item-qty-rate">
					<div class="item-qty"><span>${item_data.qty || 0}</span></div>
					<div class="item-rate-amount">
						<div class="item-rate">${format_currency(item_data.rate, currency)}</div>
					</div>
				</div>`
		}
	}

function get_description_html() {
			if (item_data.description) {
				if (item_data.description.indexOf('<div>') != -1) {
					try {
						item_data.description = $(item_data.description).text();
					} catch (error) {
						item_data.description = item_data.description.replace(/<div>/g, ' ').replace(/<\/div>/g, ' ').replace(/ +/g, ' ');
					}
				}
				item_data.description = frappe.ellipsis(item_data.description, 45);
				return `<div class="item-desc">${item_data.description}</div>`;
			}
			return ``;
		}

		function get_item_image_html() {
			const { image, item_name } = item_data;
			if (!me.hide_images && image) {
				return `
					<div class="item-image">
						<img
							onerror="cur_pos.cart.handle_broken_image(this)"
							src="${image}" alt="${frappe.get_abbr(item_name)}"">
					</div>`;
			} else {
				return `<div class="item-image item-abbr">${frappe.get_abbr(item_name)}</div>`;
			}
		}
}


function complete_order(){
    const payment = frappe.pages['point-of-sale'].pos.payment;
    const doc = payment.events.get_frm().doc;
    const paid_amount = doc.paid_amount;
    const items = doc.items;
    if (!items.length) {
        const message = __("You cannot submit empty order.");
        frappe.show_alert({ message, indicator: "orange" });
        frappe.utils.play_sound("error");
        return;
    }
    submit_invoice();
}


function checkout_order(){
  if ($(this).attr('style').indexOf('--blue-500') == -1) return;
  complete_order();
  frappe.pages['point-of-sale'].pos.cart.toggle_checkout_btn(false);

}


function submit_invoice(){
  debugger;
  frappe.pages['point-of-sale'].pos.frm.savesubmit()
  .then((r) => {
    frappe.pages['point-of-sale'].pos.order_summary.events.new_order();
    frappe.show_alert({
      indicator: 'green',
      message: __('POS invoice {0} created succesfully', [r.doc.name])
    });
  });
}


function get_qty(customer, item){
    var qty;
    frappe.call({
        method: 'bonyan_app.bonyan_app.overrides.point_of_sale.get_qty',
        args: {
            customer,
            item
        },
        async: false,
        callback: (r) => {
            if(!r.exc) {
                qty = r.message;
            }
        }
    });

    return qty;
}
