function onlynumber(e) {
    var Evento = e || window.event ;
    var key = Evento.keyCode || Evento.which;
    key = String.fromCharCode(key);
    var regex = /^[0-9]+$/ ;
    if (!regex.test(key)) {
        Evento.returnValue = false ;
        if (Evento.preventDefault) {
            Evento.preventDefault ();
        }
    }
}

function mask(){
    $("#cpf").keypress(function() {
       $(this).mask('000.000.000-00');
    });
}

function verificar() { 
    let senha = document.getElementById("senha").value
    // alert(senha)
      if (senha.length < 10) {
        alert( " senha incorreta");
    }
}