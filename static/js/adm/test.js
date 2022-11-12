const labels = [
    'Janeiro',
    'Fevereiro',
    'Março',
    'Abril',
    'Maio',
    'Junho',
    'Julho',
    'Agosto',
    'Setembro',
    'Outubro',
    'Novembro',
    'Dezembro',
    ];

    const data = {
    labels: labels,
    datasets: [{
        label: 'Transações',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: [0, 10, 5, 2, 20, 30, 45,30,54,23,76,100],
    }]
    };

    const config = {
    type: 'line',
    data: data,
    options: {}
    };


    const myChart = new Chart(
          document.getElementById('myChart'),
          config
        );
