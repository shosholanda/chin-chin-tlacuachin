/**
 * Generamos dinámicamente el carro, pero no se guarda nada hasta q se confirme
 */

var carro = [];

/* Crea un pedido */
async function nuevoItem(gtin, cantidad) {
    let cart = document.getElementById('cart');
    let url = cart.getAttribute('url')

    let producto = await CCT.Request.fetch(url + gtin);

    producto.gtin = gtin;
    producto.cantidad = cantidad;

    for (let item of carro) {
        if (item.gtin === gtin) {
            item.cantidad += cantidad;
            document.getElementById('cantidad-' + item.id.value) = item.cantidad;
            document.getElementById('sub-' + item.id).innerText = "$ " + item.cantidad * item.precio;
            updateTotal();
            resetInput();
            return;
        }
    }


    carro.push(producto);
    let itemString = `<div class="item" id="${producto.id}">
    <div class="item" >
      <div>
  	<div>
  	 ${producto.gtin}
  	</div>
  	<div>
  	  ${producto.nombre}
  	</div>
      </div>
    </div>
    <div>
      <div class="campo">
        <label for="cantidad">Cantidad</label>
        <input type="number" id="cantidad-${producto.id}" name="cantidad" required="true" autocomplete="off" min="1" max="99" value="${producto.cantidad}">
      </div>
        <div>
          Precio:$ ${producto.precio}
        </div>
    </div>
    <div>
      <h5>Subtotal</h5>
      <p id=sub-${producto.id}>$ ${producto.subtotal}</p>
    </div>
    <div>
      <button id="borrar-${producto.id}">Borrar</button>
    </div>
  </div>`
    
    cart.insertAdjacentHTML('beforeend', itemString);
    document.getElementById('comprar').disabled = false;
    document.getElementById('borrar-' + producto.id).addEventListener('click', function () {
        document.getElementById(producto.id).remove();
        for (let i = 0; i < carro.length; i++)
            if (carro[i].id === producto.id) {
                carro.splice(i, 1);
                break;
            }
        if (carro.length === 0)
            document.getElementById('comprar').disabled = true;
        updateTotal();
    });

    document.getElementById('cantidad-' + producto.id).addEventListener('change', function () {
        cant = parseInt(this.value)
        for (let item of carro)
            if (item.id === producto.id)
                item.cantidad = cant
        document.getElementById('sub-' + producto.id).innerText = "$ " + producto.cantidad * producto.precio;
        updateTotal();
    });
    updateTotal();
    resetInput();
}

function borrarItem() { }

function resetInput() {
    document.getElementById('codigo_gtin').value = "";
    document.getElementById('cantidad').value = "1";
}

function updateTotal() {
    let total = document.getElementById('total')
    let x = 0;
    for (let item of carro) {
        x += item.precio * item.cantidad;
    }
    total.value = x;
}

function agregarProducto() {
    let gtin = document.getElementById('codigo_gtin');
    let cant = document.getElementById('cantidad');

    if (!(gtin.value && cant.value)) {
        // document.getElementById('agregar').disabled = true;
        return;
    }

    nuevoItem(gtin.value, parseInt(cantidad.value));
}


function buscaGtin() {
    pseudogtin = this.value.toUpperCase();
    this.value = pseudogtin;
    let suggestions = document.getElementById('suggestions');
    let getGtinsUrl = suggestions.getAttribute('url');
    suggestions.innerHTML = "";

    if (!(pseudogtin)) return;
    fetch(getGtinsUrl + pseudogtin).then(
        response => response.json().then(
            response => {
                let gtins = response['gtins']
                for (const [key, value] of Object.entries(gtins)) {
                    agregaLista(suggestions, key, value);
                }
            }
        )
    ).catch(error => console.log("Error:", error));

}

function agregaLista(uList, value, text) {
    let li = document.createElement('li');
    li.setAttribute('value', value);
    li.addEventListener('click', function () {
        let suggestions = document.getElementById('suggestions');
        let gtin = document.getElementById('codigo_gtin');
        suggestions.innerHTML = "";
        gtin.value = value
    });
    li.textContent = text
    uList.appendChild(li);

}

/**
 * Envia las compras agregadas anteriormente al cart.
 * Crea un JSON con la información colectada por el cart
 */
function sendCart() {
    //Convertir a JSON
    let cartData = [];

    for (let item of carro) {
        let p = item.id;
        let c = item.cantidad;

        let data = {
            id_producto: p,
            cantidad: c
        };
        cartData.push(data);
    }

    let cliente = document.getElementById('cliente');
    let notas = document.getElementById('notas');
    let propina = document.getElementById('propina');
    let total = document.getElementById('total');

    let shop = {
        cart: cartData,
        total: total.value,
        propina: propina.value,
        notas: notas.value,
        cliente: cliente.value
    }


    //Enviar JSON
    fetch('create-venta', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(shop)
    })
        .then(response => {
            // Por JSON
            if (response.redirect) {
                window.location.href = response.redirect;
            } else {
                response.text().then(html => {
                    document.open();
                    document.write(html);
                    document.close();
                })
            }
        })
        .catch((error) => {
            console.log('Error:', error);
        });
}

// Main
window.onload = function () {
    let nueva_venta_button = document.getElementById('nueva-venta');
    let agregar_button = document.getElementById('agregar');
    let codigo_input = document.getElementById('codigo_gtin');
    let cant = document.getElementById('cantidad');
    let comprar = document.getElementById('comprar');
    comprar.disabled = true;

    nueva_venta_button.addEventListener('click', function () {
        let url = this.getAttribute('href');
        window.open(url, '_blank').focus();
    })
    agregar_button.addEventListener('click', agregarProducto);
    codigo_input.addEventListener('input', buscaGtin);
    comprar.addEventListener('click', sendCart);
}

window.addEventListener('beforeunload', function (e) {
    var confirmationMessage = 'Are you sure you want to leave this page?';
    e.returnValue = confirmationMessage;  // Gecko, WebKit, Chrome <34
    return confirmationMessage;           // Gecko, WebKit, Chrome >=34
});

