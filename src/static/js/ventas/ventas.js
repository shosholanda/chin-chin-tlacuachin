let referencia = 0;

function popUp(answer){
    if (answer === true || answer === false)
        printTicket(answer);
    CCT.Event.changeVisibility('overlay', type='flex');
}

async function printTicket(rfc){
    json = {'referencia': referencia,
            'rfc': rfc}

    await CCT.Request.fetch({url: "print-venta/", data: json, type: 'POST'});
}


window.onload = function() {
    document.getElementById('yes').addEventListener('click', function(){
        popUp(true);
    });
						   
    document.getElementById('no').addEventListener('click', function(){
	    popUp(false)
    });

    document.getElementById('cancel').addEventListener('click', function(){
        popUp(undefined)
    });
    
    let buttons = document.getElementsByClassName('print')
    for (let b of buttons)
	    b.addEventListener('click', function(){
            referencia = parseInt(this.id.split('-')[1]);    
            popUp(undefined);
        })
}
