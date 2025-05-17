
async function create_type(new_type) {
    if (!CCT.Text.validateString(new_type)){
        alert("Especifica un tipo de gasto.");
        return;
    }

    let url = document.getElementById('create-type-button').getAttribute('url');
    let json = { 'nombre': new_type }
    let response = await CCT.Request.fetch({url: url, type:'POST', data: json});
    CCT.HTML.writeOn({html: response.html, url: response.url})
}


async function create_gasto() {
    let descripcion = document.getElementById('description').value;
    let tipo_gasto = CCT.HTML.getSelectedValue('expense-type').value;
    let cantidad = document.getElementById('quantity').value;
    let fecha = document.getElementById('register-date').value;

    let url = document.getElementById('create-gasto-button').getAttribute('url');

    console.log(descripcion, tipo_gasto, cantidad, fecha, url)

    if (!validaCampos()) {
        alert("Llena todos los campos para crear un nuevo gasto");
        return;
    }
    let json = {
        'tipo_de_gasto': tipo_gasto,
        'cantidad': cantidad,
        'descripcion': descripcion,
        'fecha': fecha
    }


    let response = await CCT.Request.fetch({url: url, type: 'POST', data: json})
    CCT.HTML.writeOn({html: response.html, url: response.url})
}

function validaCampos(){
    let descripcion = document.getElementById('description').value;
    let tipo_gasto = CCT.HTML.getSelectedValue('expense-type').value;
    let cantidad = document.getElementById('quantity').value;
    let fecha = document.getElementById('register-date').value;
    return CCT.Text.validateString(descripcion, fecha) && CCT.Text.validateInt(tipo_gasto) && CCT.Text.validateDouble(cantidad)
}

window.onload = function () {

    let new_expense_button = document.getElementById('dropdown-holder');
    let new_expense_menu = document.getElementById('dropdown-content');

    new_expense_button.addEventListener('click', function () {
        CCT.Event.changeVisibility(new_expense_menu);
    });

    let new_type_expense_button = document.getElementById('create-new-type');
    let new_type_expense_menu = document.getElementById('type-product-form');

    new_type_expense_button.addEventListener('click', function () {
        CCT.Event.changeVisibility(new_type_expense_menu);
    });

    let create_type_expense_button = document.getElementById('create-type-button');
    let new_type_expense_input = document.getElementById('new-expense-type');

    new_type_expense_input.addEventListener('input', function(){
        this.value = this.value.toUpperCase();
    });
    create_type_expense_button.addEventListener('click', function () {
        create_type(new_type_expense_input.value);
    });


    let create_expense_button = document.getElementById('create-gasto-button');
    create_expense_button.addEventListener('click', create_gasto);

    let date = document.getElementById('register-date');
    date.valueAsDate = new Date()
}

