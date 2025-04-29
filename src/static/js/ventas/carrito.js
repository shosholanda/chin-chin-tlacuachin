/**
 * Generamos dinámicamente el carro, pero no se guarda nada hasta q se confirme
 * Se me que un objeto internamente maneje todo esto en lugar de estar llamando a funciones
 * y hacer document.getelement cada 2 lineas.
 */

var carro = [];

/**
 * Añade un nuevo item a la lista del carro, actualiza si ya lo tiene.
 * @returns nada
 */
async function nuevoItem() {

    let cart = document.getElementById('cart');
    let gtin = document.getElementById('gtin-code').value;
    let cant = parseInt(document.getElementById('quantity').value);
    if (cant <= 0) {
        alert("WTF amigo vos estas reloco")
        resetInput();
        return;
    }

    // Si ya existe el producto, solo actualizamos
    for (let item of carro) {
        if (item.gtin === gtin) {
            item.cantidad += cant;
            document.getElementById('c' + item.id).value = item.cantidad;
            document.getElementById('s' + item.id).innerHTML = "$ " + item.cantidad * item.precio;
            item.html = document.getElementById(item.id).outerHTML
            updateTotal();
            resetInput();
            return;
        }
    }

    let url = cart.getAttribute('url');
    url = url.slice(0, -2) + gtin + "&" + cant;
    let producto = await CCT.Request.fetch({ url: url });
    carro.push(producto);

    cart.insertAdjacentHTML('beforeend', producto.html);

    let remove = document.getElementById('e' + producto.id);
    remove.addEventListener('click', function () {
        borrarItem(producto.id);
        updateTotal();
    });

    document.getElementById('c' + producto.id).addEventListener('change', function () {
        cant = parseInt(this.value)
        if (cant <= 0) {
            alert("Otra vez amigo watafak como vas a vender 0 cafes?");
            for (let item of carro) if (item.id === producto.id) this.value = item.cantidad;
            return;
        }
        for (let item of carro)
            if (item.id === producto.id) {
                item.cantidad = cant
                break;
            }
        document.getElementById('s' + producto.id).innerText = "$ " + producto.cantidad * producto.precio;
        updateTotal();
    });
    updateTotal();
    resetInput();
}

function borrarItem(id) {
    let item = document.getElementById(id);
    item.remove();
    for (let i = 0; i < carro.length; i++)
        if (carro[i].id === id) {
            carro.splice(i, 1);
            break;
        }
    if (carro.length === 0)
        document.getElementById('buy-cart').disabled = true;
}

function resetInput() {
    document.getElementById('gtin-code').value = "";
    document.getElementById('quantity').value = "1";
    verifyInputs();
}

function updateTotal() {
    let total = document.getElementById('total');
    let x = 0;
    for (let item of carro) x += item.precio * item.cantidad;
    total.value = x;
}

function verifyInputs() {
    let g = document.getElementById('gtin-code');
    let c = document.getElementById('quantity');
    let b = document.getElementById('add-cart');
    b.disabled = !(CCT.Text.validateString(g.value) && CCT.Text.validateInt(c.value));
    verifyCart();
}

function verifyCart() {
    let b = document.getElementById('buy-cart');
    let total = parseInt(document.getElementById('total').value);
    // let payment = document.getElementById('payments');
    b.disabled = (carro.length === 0) || (total <= 0)// || (CCT.HTML.getRadioValue(payment) === null);
}


/**
 * Busca el código gtin, validando que exista
 * @param {*} gtinCode el código a validar
 * @returns el conjunto de productos que coinciden con el gtin, null en otro caso.
 */
async function buscaGtin(gtinCode) {
    let suggestions = document.getElementById('suggestions');
    let getGtinsUrl = suggestions.getAttribute('url');

    let response = await CCT.Request.fetch({ url: getGtinsUrl + gtinCode });
    let gtins = response['gtins'];
    if (CCT.Text.validateString(gtinCode) && CCT.Text.validateObject(gtins))
        return gtins;
    suggestions.style.display = 'none';
    return null;
}

/**
 * Muestra las opciones disponibles para código gtin como un menu
 * @param {*} products 
 */
function displayOptions(products) {
    let suggestions = document.getElementById('suggestions');
    let list = document.getElementById('suggestions-list');
    let gtinInput = document.getElementById('gtin-code');

    suggestions.style.display = 'block';
    CCT.HTML.cleanInnerHTML(list);

    for (const [gtin, description] of Object.entries(products)) {
        let attribs = { 'value': gtin }
        let selectItem = function () {
            list.innerHTML = "";
            gtinInput.value = gtin;
            verifyInputs();
            suggestions.style.display = 'none';
        }
        let li = CCT.HTML.createElement('li', attribs, description, 'click', selectItem);
        list.appendChild(li);
    }

}

/**
 * Envia las compras agregadas anteriormente al cart.
 * Crea un JSON con la información colectada por el cart
 */
async function sendCart() {
    //Convertir a JSON
    let cartData = [];

    for (let item of carro) {
        let data = {
            product_id: item.id,
            quantity: item.cantidad
        };
        cartData.push(data);
    }

    let cliente = document.getElementById('client');
    let notas = document.getElementById('notes');
    let propina = document.getElementById('tip');
    let total = document.getElementById('total');
    let tipo_pago = document.getElementById('payments');
    tipo_pago = CCT.HTML.getRadioValue(tipo_pago);
    tipo_pago = tipo_pago ? parseInt(tipo_pago.value) : null;
    let url = document.getElementById('buy-cart').getAttribute('url')

    let shop = {
        cart: cartData,
        total: parseFloat(total.value),
        tip: parseFloat(propina.value),
        notes: notas.value,
        client: cliente.value,
        payment: tipo_pago

    }

    CCT.Request.fetch({ url: url, data: shop, type: 'POST'});
}

// Main
window.onload = function () {
    let nueva_venta_button = document.getElementById('new-venta');
    let agregar_button = document.getElementById('add-cart');
    let codigo_input = document.getElementById('gtin-code');
    let cantidad = document.getElementById('quantity');
    let comprar = document.getElementById('buy-cart');
    let tipo_pago = document.getElementById('payments').getElementsByTagName('input');

    verifyInputs();
    verifyCart();

    nueva_venta_button.addEventListener('click', function () {
        let url = this.getAttribute('href');
        window.open(url, '_blank').focus();
    })
    cantidad.addEventListener('change', verifyInputs)
    codigo_input.addEventListener('input', async function () {
        this.value = this.value.toUpperCase().trim();
        products = await buscaGtin(this.value);
        verifyInputs();
        if (products != null)
            displayOptions(products)
    });
    agregar_button.addEventListener('click', nuevoItem);
    comprar.addEventListener('click', function () {
        this.disabled = true;
        sendCart();
    });

    for (let i = 0; i < tipo_pago.length; i++) {
        tipo_pago[i].addEventListener('click', function () {
            verifyCart();
        });
    }
}

window.addEventListener('beforeunload', function (e) {
    var confirmationMessage = 'Are you sure you want to leave this page?';
    e.returnValue = confirmationMessage;  // Gecko, WebKit, Chrome <34
    return confirmationMessage;           // Gecko, WebKit, Chrome >=34
});

