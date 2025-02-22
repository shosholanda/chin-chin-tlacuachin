
function closePopUp(answer, url_base, gtin) {
    if (answer){

        CCT.Request.fetch({url: url_base + 'delete-producto/' + gtin , redirect: 'manual'});
    }
    CCT.Event.changeVisibility('overlay');
}


window.onload = function () {
    let product = document.getElementById('product');
    let id_product = product.getAttribute('productID');
    let gtin = product.getAttribute('gtin');
    let url = product.getAttribute('url');

    document.getElementById('delete').addEventListener('click', function () {
        CCT.Event.changeVisibility('overlay', 'flex');
    });

    document.getElementById('status').addEventListener('change', async function(){
        await CCT.Request.fetch({url: url + 'change-status/' + gtin, redirect: 'manual'});
    });
    

    document.getElementById('update').addEventListener('click', function () {
        let precio = document.getElementById('price');
        let json = {
            'id_product': id_product,
            'gtin': gtin,
            'nombre': gtin, // May these two change
            'precio': precio.value
        }
        console.log(json)
        // CCT.Request.fetch({
        //     url: url + 'update-producto/' + id,
        //     type: 'POST',
        //     data: json,
        //     redirect: 'manual'
        // });
    })

    document.getElementById('yes').addEventListener('click', function () {
        closePopUp(true, url, gtin)
    });

    document.getElementById('no').addEventListener('click', function () {
        closePopUp(false, url, gtin)
    });
}