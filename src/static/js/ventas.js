let referencia = 0;

function showRFC(){
    document.getElementById('overlay').style.display = 'flex';
    let id = parseInt(this.id.split('-')[1]);
    referencia = id;
}

function closePopUp(answer){
    printTicket(answer)
    document.getElementById('overlay').style.display = 'none';
}


function printTicket(rfc){

    json = {'referencia': referencia,
	    'rfc': rfc}

    fetch('print-venta/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(json)
    }
	 ).then( response =>
	     response.json().then( response =>
		 console.log(response)
	)
    ).catch(error => console.log(error))
}


window.onload = function() {
    document.getElementById('yes').addEventListener('click', function(){
	closePopUp(true)
    });
						   
    document.getElementById('no').addEventListener('click', function(){
	closePopUp(false)
    });

    document.getElementById('cancelar').addEventListener('click', function(){
	document.getElementById('overlay').style.display = 'none';
    });
    
    let buttons = document.getElementsByClassName('print')
    for (let b of buttons)
	b.addEventListener('click', showRFC)
}
