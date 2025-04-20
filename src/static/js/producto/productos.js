async function generateGtin() {
    let nombre = document.getElementById('name')
    let categoria = CCT.HTML.getSelectedValue('category').text // str
    let tipo_de_producto = CCT.HTML.getSelectedValue('product-type').text // str
    let precio = document.getElementById('price')
    let gtin = document.getElementById('gtin')


    if (!CCT.Text.validateDefined(nombre, categoria, tipo_de_producto, precio)) {
        alert("Ingrese valores válidos en los campos requeridos.")
        return;
    }

    let code = CCT.Text.generateCode(nombre.value, categoria, tipo_de_producto, precio.value)
    gtin.value = code;

    let response = await CCT.Request.fetch({url: 'get-gtin/' + code});
    if (response.gtin) {
        alert(`Ya existe un producto con este código: ${code}\n
            Utiliza otros datos, o cambia manualmente el gtin`);
        CCT.Event.changeDisabled('create-product-button', false)
    }
    return code;
}

async function create_category() {
    let text = document.getElementById('new-category');
    if (text.value) {
        let json = { 'nombre': text.value }
        await CCT.Request.fetch({url: 'create-categoria/', 
                                data: json, 
                                type: 'POST', 
                                redirect: 'manual'});
    } else {
        alert("Especifica una categoria");
    }
}

async function create_type() {
    let text = document.getElementById('new-product-type');
    if (text.value) {
        let json = { 'nombre': text.value };
        await CCT.Request.fetch({url: 'create-tipo-producto/', 
                                data: json, 
                                type: 'POST', 
                                redirect: 'manual'});
    } else {
        alert("Especifica un tipo de producto.");
    }
}

async function create_product() {
    let nombre = document.getElementById('name')
    let categoria = document.getElementById('category') // int
    let tipo_producto = document.getElementById('product-type') //int
    let precio = document.getElementById('price')
    let gtin = document.getElementById('gtin')

    if (CCT.Text.validateDefined(nombre, categoria, tipo_producto, precio, gtin)) {
        let json = {
            'nombre': nombre.value,
            'categoria': categoria.value,
            'tipo_producto': tipo_producto.value,
            'precio': precio.value,
            'gtin': gtin.value
        }
        console.log(json)

        await CCT.Request.fetch({url:'create-producto/', 
                                data: json, 
                                type:'POST', 
                                redirect:'manual'});
    } else {
        alert("Llena todos los campos para el producto");
    }
}

window.onload = async function () {

    document.getElementById('dropdown-holder').addEventListener('click', function () {
        CCT.Event.changeVisibility('dropdown-content');
    });
    document.getElementById('create-new-category-button').addEventListener('click', function () {
        CCT.Event.changeVisibility('category-form');
    });
    document.getElementById('create-new-product-type-button').addEventListener('click', function () {
        CCT.Event.changeVisibility('product-type-form');
    });
    document.getElementById('create-category-button').addEventListener('click', async function(){
        await create_category();
    })
    document.getElementById('create-product-type-button').addEventListener('click', async function() {
        await create_type();
    })

    let gtin_input = document.getElementById('gtin');
    gtin_input.addEventListener('input', async function () {
        this.value = this.value.toUpperCase();
    });

    document.getElementById('new-product-type').addEventListener('input', function(){
        this.value = this.value.toUpperCase();
    })

    /** Crear producto */
    document.getElementById('create-product-button').addEventListener('click', function () {
        create_product();
    });

    document.getElementById('name').addEventListener('input', async function () {
        this.value = CCT.Text.toTitleCase(this.value);
        gtin_input.value = await generateGtin();
    });

    document.getElementById('price').addEventListener('input', async function () {
        gtin_input.value = await generateGtin();
    });

    document.getElementById('category').addEventListener('change', async function () {
        gtin_input.value = await generateGtin();
    });

    document.getElementById('product-type').addEventListener('change', async function () {
        gtin_input.value = await generateGtin();
    });

    let statuses = document.getElementsByName('status');
    let borrars = document.getElementsByName('borrar');
    for (let i = 0; i < statuses.length; i++) {
        borrars[i].addEventListener('click', async function(){
            let gtin = this.closest("tr").id;
            await CCT.Request.fetch({url: 'delete-producto/' + gtin,
                                    redirect: 'manual'})
        });
        statuses[i].addEventListener('change', async function() {
            let gtin = this.closest("tr").id
            await CCT.Request.fetch({url: `change-status/${gtin}`,
                                    redirect: 'manual'})
        });
    }
}

