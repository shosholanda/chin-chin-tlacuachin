function nuevaVenta(){
    window.open("create-venta", '_blank').focus();
}


function generateTicket(){
    let id = parseInt(this.id.split('-')[1]);
    fetch('print-venta/'+ id).then( response =>
	response.json()
    ).catch(error => console.log(error))
}


window.onload = function() {
    let buttons = document.getElementsByClassName('print')
    for (let b of buttons)
	b.addEventListener('click', generateTicket)
}
