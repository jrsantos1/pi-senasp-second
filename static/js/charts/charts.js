

function get_config_chart(value){

    console.log(value)

    let extrato_data = []
    let valor = []

    for (let item of value){
        console.log(item)
        extrato_data.push(item.extrato_datas)
        valor.push(item.valor)
    }
    const labels = extrato_data
    const data = {
    labels: labels,
    datasets: [{
        label: 'Saldo Histórico',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: valor,}]
    };

    const config = {
        type: 'line',
        data: data,
        options: {}
    };
    return config
}
function get_chart_despesas(value){
    console.log(value)

     let categoria = []
     let valor = []

    for (let item of value){
        console.log(item)
        categoria.push(item.categoria)
        valor.push(item.valor)
    }
    const data = {
      labels: categoria,
      datasets: [{
        label: 'My First Dataset',
        data: valor,
        backgroundColor: [
          'rgb(255, 99, 132)',
          'rgb(54, 162, 235)',
          'rgb(255, 205, 86)',
            'rgb(000, 205, 000)',,
            'rgb(000, 000, 150)',
            'rgb(000, 205, 50)',
            'rgb(255, 205, 86)',
            'rgb(100, 000, 86)',
            'rgb(10, 10, 86)',
            'rgb(30, 250, 250)',
        ],
        hoverOffset: 4
      }]};

    const config = {
      type: 'pie',
      data: data,
    };

    return config
}
function get_chart_mov_user(value){

    console.log(value)

    let categoria = []
    let valor = []

    for (let item of value){
        console.log(item)
        categoria.push(item.nome)
        valor.push(item.valor)
    }

    const labels = categoria;
    const data = {
      labels: labels,
      datasets: [{
        label: 'Valor movimentado por usuário',
        data: valor,
        backgroundColor: [
          'rgba(99, 99, 232, 0.5)',
          // 'rgba(255, 159, 64, 0.2)',
          // 'rgba(255, 205, 86, 0.2)',
          // 'rgba(75, 192, 192, 0.2)',
          // 'rgba(54, 162, 235, 0.2)',
          // 'rgba(153, 102, 255, 0.2)',
          // 'rgba(201, 203, 207, 0.2)'
        ],
        borderColor: [
          'rgb(99, 99, 232)',
          // 'rgb(255, 159, 64)',
          // 'rgb(255, 205, 86)',
          // 'rgb(75, 192, 192)',
          // 'rgb(54, 162, 235)',
          // 'rgb(153, 102, 255)',
          // 'rgb(201, 203, 207)'
        ],
        borderWidth: 1
      }]
    };

    const config = {
      type: 'bar',
      data: data,
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      },
    };

    return config

}
function get_transacoes_dia_qtd(value){

    console.log(value)

    let data_transacoes = []
    let valor = []

    for (let item of value){
        console.log(item)
        data_transacoes.push(item.data)
        valor.push(item.valor)
    }
    const labels = data_transacoes
    const data = {
    labels: labels,
    datasets: [{
        label: 'Histórico - Transações por dia ',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: valor,}]
    };

    const config = {
        type: 'line',
        data: data,
        options: {}
    };
    return config
}