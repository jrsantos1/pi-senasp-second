

function get_config_chart(value){

    console.log(value)

    let extrato_data = []
    let valor = []

    for (let item of value){
        console.log(item)
        extrato_data.push(item.extrato_data)
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