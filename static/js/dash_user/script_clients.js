const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");

const containerTable = document.querySelector(".container-table");
const tableTransactions = document.querySelector(".transactions");

const tipo = document.getElementById("tipo");
const categoria = document.querySelector("#categoria");
const valor = document.querySelector("#valor");
const dest = document.querySelector("#dest");
const date = document.querySelector("#date");

const alterarEmail = document.querySelector("#alterar-email");
const email = document.querySelector("#email");
const senha = document.querySelector("#senha");
const cancelar = document.querySelector("#cancelar");
const confirmar = document.querySelector("#confirmar");
const ok = document.querySelector("#ok");

function ontype(){
    if(tipo.value !== "null"){
        categoria.style.display = "flex";
        valor.style.display = "flex";
    }
    if(tipo.value === "doc" || tipo.value === "ted" || tipo.value === "pix"){
        dest.style.display = "flex";
        date.style.display = "flex";
    }
}

alterarEmail.addEventListener('click', () => {
    alterarEmail.style.display = "none";
    ok.style.display = "none";
    senha.style.display = "flex";
    cancelar.style.visibility = "visible";
    confirmar.style.visibility = "visible";
    email.removeAttribute("disabled");
})

// Show sidebar
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = "block";
})

// Close sidebar
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = "none";
})

if(window.matchMedia("(max-width: 768px)").matches){
    sideMenu.addEventListener('click', () => {
        sideMenu.style.display = "none";
    })
}

// Change theme
themeToggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-variables');

    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');

})

// Active Buttons
const dashboard = document.querySelector("#dashboard");
const contatos = document.querySelector("#contatos");
const extrato = document.querySelector("#extrato");
const analytics = document.querySelector("#analytics");
const transactions = document.querySelector("#transactions");
const settings = document.querySelector("#settings");

contatos.addEventListener('click', () => {
    contatos.classList.add('active');
    dashboard.classList.remove('active', 'active');
    extrato.classList.remove('active');
    analytics.classList.remove('active');
})
extrato.addEventListener('click', () => {
    extrato.classList.add('active');
    dashboard.classList.remove('active', 'active');
    contatos.classList.remove('active');
    analytics.classList.remove('active');
})
analytics.addEventListener('click', () => {
    analytics.classList.add('active');
    dashboard.classList.remove('active', 'active');
    contatos.classList.remove('active');
    extrato.classList.remove('active');
})


//circle insigths percent
var circle = document.querySelector('.insights circle');
var radius = circle.r.baseVal.value;
var circumference = radius * 2 * Math.PI;

circle.style.strokeDasharray = `${circumference} ${circumference}`;
circle.style.strokeDashoffset = `${circumference}`;

function setProgress(percent) {
  const offset = circumference - percent / 100 * circumference;
  circle.style.strokeDashoffset = offset;
}

const pct = document.querySelector('.insights .percent');
setProgress(pct.textContent);

pct.addEventListener('change', function(e) {
  if (pct.textContent < 101 && pct.textContent > -1) {
    setProgress(pct.textContent);
  }  
})

//circle expenses percent
var circle = document.querySelector('.expenses circle');
var radius = circle.r.baseVal.value;
var circumference = radius * 2 * Math.PI;

circle.style.strokeDasharray = `${circumference} ${circumference}`;
circle.style.strokeDashoffset = `${circumference}`;

function setProgress(percent) {
  const offset = circumference - percent / 100 * circumference;
  circle.style.strokeDashoffset = offset;
}

const pct2 = document.querySelector('.expenses .percent');
setProgress(pct2.textContent);

pct.addEventListener('change', function(e) {
  if (pct2.textContent < 101 && pct2.textContent > -1) {
    setProgress(pct2.textContent);
  }  
})

//circle income percent
var circle = document.querySelector('.income circle');
var radius = circle.r.baseVal.value;
var circumference = radius * 2 * Math.PI;

circle.style.strokeDasharray = `${circumference} ${circumference}`;
circle.style.strokeDashoffset = `${circumference}`;

function setProgress(percent) {
  const offset = circumference - percent / 100 * circumference;
  circle.style.strokeDashoffset = offset;
}

const pct3 = document.querySelector('.income .percent');
setProgress(pct3.textContent);

pct.addEventListener('change', function(e) {
  if (pct3.textContent < 101 && pct3.textContent > -1) {
    setProgress(pct3.textContent);
  }  
})