const form = document.getElementById("form")
const nameUser = document.getElementById("name-user")
const cpf = document.getElementById("cpf")
const gender = document.getElementById("gender")
const birthDate = document.getElementById("birth-date")
const cep = document.getElementById("cep")
const address = document.getElementById("address")
const district = document.getElementById("district")
const numberAddress = document.getElementById("number-address")
const state = document.getElementById("state")
const complement = document.getElementById("complement")
const city = document.getElementById("city")
const cell = document.getElementById("cell")
const email = document.getElementById("email")
const password = document.getElementById("password")
const passwordConfirmation = document.getElementById("password-confirmation")
const typeAccount = document.getElementById("type-account")

form.addEventListener('submit', (e) => {

   valida = checkInputs();

   if (valida === false){
    e.preventDefault();
   }
});

function checkInputs() {
    const nameValue = nameUser.value;
    const cpfValue = cpf.value;
    const genderContent = gender.value;
    const birthDateValue = birthDate.value;
    const cepValue = cep.value;
    const addressValue = address.value;
    const districtValue = district.value;
    const numberAddressValue = numberAddress.value;
    const complementValue = complement.value;
    const stateValue = state.value;
    const cityValue = city.value;
    const cellValue = cell.value;
    const emailValue = email.value;
    const passwordValue = password.value;
    const passwordConfirmationValue = passwordConfirmation.value;
    const typeAccountValue = typeAccount.value;

    if(nameValue === ""){
        setErrorFor(nameUser, "O nome é obrigatório.");
    } else {
        setSuccessFor(nameUser)
    }

    if(cpfValue === ""){
        setErrorFor(cpf, "O CPF é obrigatório.");
    } else {
        setSuccessFor(cpf)
    }

    if (emailValue === "") {
        setErrorFor(email, "O email é obrigatório.");
    } else if (!checkEmail(emailValue)) {
        setErrorFor(email, "Por favor, insira um email válido.");
    } else {
        setSuccessFor(email);
    }

    if(genderContent === ""){
        setErrorFor(gender, "O gênero é obrigatório.");
    } else {
        setSuccessFor(gender)
    }

    if(birthDateValue === ""){
        setErrorFor(birthDate, "A data de nscimento é obrigatória.");
    } else {
        setSuccessFor(birthDate)
    }
    
    if(cellValue === ""){
        setErrorFor(cell, "O celular é obrigatório.");
    } else {
        setSuccessFor(cell)
    }

    if(typeAccountValue === ""){
        setErrorFor(typeAccount, "Por favor, escolha um tipo de conta.");
    } else {
        setSuccessFor(typeAccount)
    }

    if (passwordValue === "") {
        setErrorFor(password, "A senha é obrigatória.");
    } else if (passwordValue.length < 7) {
        setErrorFor(password, "A senha precisa ter no mínimo 7 caracteres.");
    } else {
        setSuccessFor(password);
    }
    
    if (passwordConfirmationValue === "") {
        setErrorFor(passwordConfirmation, "A confirmação de senha é obrigatória.");
    } else if (passwordConfirmationValue !== passwordValue) {
        setErrorFor(passwordConfirmation, "As senhas não conferem.");
    } else {
        setSuccessFor(passwordConfirmation);
    }

    if(cepValue === ""){
        setErrorFor(cep, "O CEP é obrigatório.");
    } else if (cepValue.length !== 9) {
        setErrorFor(cep, "Por favor, insira um CEP válido.");
    } else {
        setSuccessFor(cep)
    }

    if(stateValue === ""){
        setErrorFor(state, "Por favor, verifique o CEP.");
    } else {
        setSuccessFor(state)
    }
        
    if(cityValue === ""){
        setErrorFor(city, "Por favor, verifique o CEP.");
    } else {
        setSuccessFor(city)
    }
    
    if(districtValue === ""){
        setErrorFor(district, "Por favor, verifique o CEP.");
    } else {
        setSuccessFor(district)
    }

    if(addressValue === ""){
        setErrorFor(address, "Por favor, verifique o CEP.");
    } else {
        setSuccessFor(address)
    }

    if(numberAddressValue === ""){
        setErrorFor(numberAddress, "O número da residência é obrigatório.");
    } else {
        setSuccessFor(numberAddress)
    }
    
    if(complementValue === ""){
        setSuccessFor(complement);
    } else {
        setSuccessFor(complement)
    }
    
    const formControls = form.querySelectorAll(".mb-3")
    const formIsValid = [...formControls].every(mb3 => {
        return (mb3.className === "mb-3 success");
    });

    // Validação do submit
    if (formIsValid) {
        return true;
    } else {
        return false;
    }

}

function setErrorFor(input, message) {
    const formControl = input.parentElement;
    const small = formControl.querySelector("small");
    
    // Adicionar a mensagem de erro
    small.innerText = message;

    // Adicionar a classe de erro
    formControl.className = "mb-3 error";
}

function setSuccessFor(input) {
    const formControl = input.parentElement;

    // Adicionar a classe de sucesso
    formControl.className = "mb-3 success";
}

// Checar validação do e-mail
function checkEmail(email) {
    return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
}


// Checar validação de Idade
function validadata(){
    var data = document.getElementById("birth-date").value; // pega o valor do input
    data = data.replace(/\//g, "-"); // substitui eventuais barras (ex. IE) "/" por hífen "-"
    var data_array = data.split("-"); // quebra a data em array
    
    // para o IE onde será inserido no formato dd/MM/yyyy
    if(data_array[0].length != 4){
       data = data_array[2]+"-"+data_array[1]+"-"+data_array[0]; // remonto a data no formato yyyy/MM/dd
    }
    
    // comparo as datas e calculo a idade
    var hoje = new Date();
    var nasc  = new Date(data);
    var idade = hoje.getFullYear() - nasc.getFullYear();
    var m = hoje.getMonth() - nasc.getMonth();
    if (m < 0 || (m === 0 && hoje.getDate() < nasc.getDate())) idade--;
    
    if(idade < 18){
       alert("Infelizmente ainda não é possivel abrir uma conta para você, pessoas menores de 18 não podem se cadastrar. "
            +"Volte quando completar 18 anos", window.location.href = "/");
       return false;

    }
}