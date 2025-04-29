function updateData(){
    let url = document.getElementById('update-data').getAttribute('url');
    let nombre = document.getElementById('name').value;
    let aP = document.getElementById('first-name').value;
    let aM = document.getElementById('last-name').value;
    let birthday = document.getElementById('birthday').value;

    if (!CCT.Text.validateString(nombre, aP, aM, birthday, url)){
        alert("Llene todos los campos de texto para actualizar correctamente");
        return;
    }
    let json = {'nombre': nombre, 
        'apellido_paterno': aP,
        'apellido_materno': aM,
        'fecha_nacimiento': birthday
    }
    CCT.Request.fetch({url: url, type:'POST', data: json});
}

window.onload = function(){
    let update_info = document.getElementById('update-data');
    let deactivate_button = document.getElementById('deactivate-account');
    let change_password = document.getElementById('password-change-button');
    let password_form = document.getElementById('overlay');
    let cancel = document.getElementById('cancel');

    update_info.addEventListener('click', function(){
        updateData();
    });

    deactivate_button.addEventListener('click', function(){
        if (confirm(`¿Seguro que quieres desactivar esta cuenta?
No podrás volver a iniciar sesión hasta que un administrador te active tu cuenta de nuevo.`)){
            let url = this.getAttribute('url');
            CCT.Request.fetch({url: url, type:'GET'})
        }
    });

    change_password.addEventListener('click', function(){
        CCT.Event.changeVisibility(password_form, type='flex');
    });

    cancel.addEventListener('click', function(){
        CCT.Event.changeVisibility(password_form, type='flex');
    })
}