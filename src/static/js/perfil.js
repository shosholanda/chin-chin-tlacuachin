function getUsuario(){

    let correo = document.getElementById('buscador')

    if (!correo || correo.value === ""){
        return;
    }
    correo = correo.value.replace('\n', '').trim()

    this.setAttribute('href', this.getAttribute('data-url-base') + correo)
    console.log(this.getAttribute('href'))    
}


window.onload = function(){
    
    let admin_button = document.getElementById('administrate')

    if (admin_button)
        admin_button.addEventListener('click', getUsuario)
}