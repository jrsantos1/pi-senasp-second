// Validation (only numbers)
function onlynumber(evt) {
   var theEvent = evt || window.event;
   var key = theEvent.keyCode || theEvent.which;
   key = String.fromCharCode( key );
   var regex = /^[0-9]+$/;
   if( !regex.test(key) ) {
      theEvent.returnValue = false;
      if(theEvent.preventDefault) theEvent.preventDefault();
   }
}


// Busca CEP
function viacep() {
   $.ajax({
      url: "http://viacep.com.br/ws/" + $("#cep").val() + "/json/",
      dataType: "json",
      success: function (resposta) {
         console.log(resposta);
         $("#address").val(resposta.logradouro);
         $("#district").val(resposta.bairro);
         $("#city").val(resposta.localidade);
         $("#state").val(resposta.uf);
         $("#number-address").focus();
      },
   });
}


 // Mask 
function mask(){

   $("#cpf").keypress(function() {
      $(this).mask('000.000.000-00');
   });

   $("#birth-date").keypress(function() {
      $(this).mask('00/00/0000');
   });

   $("#cep").keypress(function() {
      $(this).mask('00000-000');
   });

   $( "#cell" ).keypress(function() {
      $(this).mask('(00) 0 0000-0000');
   }); 

}
