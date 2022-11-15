// male datapoint converter
const male = [3, 6, 6, 9, 12, 13, 19];
const maleData = [];
male.forEach(e => maleData.push(e * -1));

//  block tooltip
const tooltip2 = {
    yAlign: 'bottom',
    titleAlign: 'center',
    callbacks: {
        label: function(context) {
            return `${context.dataset.label} ${Math.abs(context.raw)}`;
        }
    }
};

// config 
const config2 = {
    type: 'bar',
    data: {
        labels: ['65+', '56 - 65', '46 - 55', '36 - 45', '26 - 35', '19 - 25', '18'],
        datasets: [{
            label: 'Masculino',
            data: maleData,
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            borderRadius: 5
        },
        {
            label: 'Feminino',
            data: [4, 7, 9, 10, 13, 14, 20],
            backgroundColor: 'rgba(255, 26, 104, 0.5)',
            borderColor: 'rgba(255, 26, 104, 1)',
            borderWidth: 1,
            borderRadius: 5
        }]
    },
    options: {
        indexAxis: 'y',
        scales: {
            x: {
                stacked: true,
                ticks:{
                    callback: function(value, index, values){
                        return Math.abs(value);
                    }
                }
            },
            y: {
                beginAtZero: true,
                stacked: true
            }
        },
        plugins: {
            tooltip2,
        }
    }
};

// render init block
const PiramideChart = new Chart(
document.getElementById('PiramideChart'),
config2
);