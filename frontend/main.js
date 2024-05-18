import './style.css'

async function fetchBasicData() {
  const basicDataUrl = `${import.meta.env.VITE_APP_ENDPOINT}basic_analysis`
  fetch(basicDataUrl).then(response => response.json()).then(data => {
    const total_transaction = document.getElementById('total-transaction')
    const fraudulent_amount = document.getElementById('fraudulent-amount')
    const fraudulent_count = document.getElementById('fraudulent-count')
    const fradulent_rate = document.getElementById('fraudulent-rate')
    const highest_fraud_amount = document.getElementById('highest-fraud-tx-amount')
    total_transaction.innerHTML = data.total_transaction
    fraudulent_amount.innerHTML = data.total_fraudulent_amount
    fraudulent_count.innerHTML = data.total_fraudulent
    fradulent_rate.innerHTML = data.fraudulent_rate + '%'
    highest_fraud_amount.innerHTML = data.highest_fraud_amount
  })
}

async function createHypo8PolarGraph() {
  const url = `${import.meta.env.VITE_APP_ENDPOINT}hypothesis_8`
  fetch(url).then(response => response.json()).then(data => {
    const labels = []
    const res_data = []
    data.forEach(item => {
      labels.push(item['age_group'])
      res_data.push(item['count'])
    })
    const highest_age_group = labels[res_data.indexOf(Math.max(...res_data))]
    const config = {
      type: 'polarArea',
      data: {
        labels: labels,
        datasets: [{
          label: 'Person Count',
          data: res_data,
        }]
      },
      options: {}
    }
    new Chart(
      document.getElementById('hypo8-chart'),
      config
    )
    document.getElementById('most-scam-age-group').innerHTML = highest_age_group + ' age'
  })
}

async function createHypo7Graph() {
  const url = `${import.meta.env.VITE_APP_ENDPOINT}hypothesis_7`
  fetch(url).then(response => response.json()).then(data => {
    const labels = []
    const res_data = []
    const total_txs = []
    data.forEach(item => {
      labels.push(item['device_used'])
      res_data.push(item['fraud_count'])
      total_txs.push(item['total_transaction'])
    })
    const config = {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          label: 'Fraud Count',
          data: res_data,
        }]
      },
      options: {}
    }
    new Chart(document.getElementById('hypo7-chart'),config)
    const config2 = {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Total Transaction',
          data: total_txs,
        }, {
          label: 'Fraudulent Transaction',
          data: res_data,
        }]
      },
      options: {}
    }
    new Chart(document.getElementById('hypo7-bar-chart'),config2)
  })
}

async function createHypo1Graph() {
  const url = `${import.meta.env.VITE_APP_ENDPOINT}hypothesis_1`
  fetch(url).then(response => response.json()).then(data => {
    const hour_labels = []
    const month_labels = ["January","February","March","April"]
    const hour_count = []
    const month_count = []
    const tx_by_hour = data['Fraudulent Transactions by Hour']
    const tx_by_month = data['Fraudulent Transactions by Month']
    for (const key in tx_by_hour) {
      hour_labels.push(key)
      hour_count.push(tx_by_hour[key]["Is Fraudulent"])
    }
    for (const key in tx_by_month) {
      month_count.push(tx_by_month[key]["Is Fraudulent"])
    }
    const most_tx_month = month_labels[month_count.indexOf(Math.max(...month_count))]
    const config = {
      type: 'line',
      data: {
        labels: hour_labels,
        datasets: [{
          label: 'Transaction Count',
          data: hour_count,
          fill: false,
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      },
      options: {responsive: true,}
    }
    const mixedConfig = {
      data: {
        labels: month_labels,
        datasets: [{
          type: 'bar',
          label: 'Bar Dataset',
          data: month_count,
          backgroundColor: 'rgba(255, 99, 132, 0.2)'
        }, {
          type: 'line',
          label: 'Line Dataset',
          data: month_count,
          borderColor: 'rgb(75, 192, 192)',
          fill: false,
        }]
      },
      options: {responsive: true,}
    }
    new Chart(document.getElementById('hypo1-chart'),config)
    new Chart(document.getElementById('hypo1-mixed-chart'),mixedConfig)
    document.getElementById('most-transaction-month').innerHTML = most_tx_month
  })

}

async function createHypo9Graph() {
  const url = `${import.meta.env.VITE_APP_ENDPOINT}hypothesis_9`
  fetch(url).then(response => response.json()).then(data => {
    const labels = []
    const fraud_count = []
    const non_fraud_count = []
    data.forEach(item => {
      labels.push(item['product_category'])
      fraud_count.push(item['fraud_count'])
      non_fraud_count.push(item['total_transaction'] - item['fraud_count'])
    })
    const config = {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Non-Fraudulent Transaction',
          data: non_fraud_count,
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }, {
          label: 'Fraudulent Transaction',
          data: fraud_count,
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true
          }
        }
      }
    }
    new Chart(
      document.getElementById('hypo9-chart'),
      config
    )
  })
}

async function createHypo5Graph() {
  const url = `${import.meta.env.VITE_APP_ENDPOINT}hypothesis_5`
  fetch(url).then(response => response.json()).then(data => {
    const labels = []
    const fraud_count = []
    const non_fraud_count = []
    const total_count = []
    const fraud_rate = []
    data.forEach(item => {
      labels.push(item['payment_method'])
      fraud_count.push(item['fraud_count'])
      non_fraud_count.push(item['total_transaction'] - item['fraud_count'])
      total_count.push(item['total_transaction'])
      fraud_rate.push((item['fraud_count'] / item['total_transaction'] * 100).toFixed(2))
    })
    const config = {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          type: 'bar',
          label: 'Fraud Count',
          data: fraud_count,
          backgroundColor: 'rgb(255, 99, 132)',
        }, {
          type: 'bar',
          label: 'Non-Fraud Count',
          data: non_fraud_count,
          backgroundColor: 'rgba(255, 159, 64,.8)',
        }, {
          type: 'line',
          label: 'Total Count',
          data: total_count,
          borderColor: 'rgb(75, 192, 192)',
          fill: false,
        }]
      },
      options: {
        responsive: true,
      }
    }
    const pieConfig = {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          label: 'Fraud Rate',
          data: fraud_rate,
        }]
      },
    }
    new Chart(
      document.getElementById('hypo5-chart'),
      config
    )
    new Chart(
      document.getElementById('hypo5-pie-chart'),
      pieConfig
    )
  })
}

async function createHypo6Graph() {
  const url = `${import.meta.env.VITE_APP_ENDPOINT}hypothesis_6`
  fetch(url).then(response => response.json()).then(data => {
    const country_labels = []
    const fraud_count = []
    const non_fraud_count = []
    const total_count = []
    data.forEach(item => {
      country_labels.push(item['country'])
      fraud_count.push(item['fraud_count'])
      non_fraud_count.push(item['total_transaction'] - item['fraud_count'])
      total_count.push(item['total_transaction'])
    })
    const config = {
      type: 'bar',
      data: {
        labels: country_labels,
        datasets: [{
          label: 'Fraud Count',
          data: fraud_count,
          backgroundColor: 'rgb(5, 155, 255)',
        }, {
          label: 'Non-Fraud Count',
          data: non_fraud_count,
          backgroundColor: 'rgba(255, 99, 132,.8)',
        }, {
          label: 'Total Count',
          data: total_count,
          borderColor: 'rgb(75, 192, 192)',
          fill: false,
        }, {
          type: 'line',
          label: 'Total Count',
          data: total_count,
          borderColor: 'rgb(75, 192, 192)',
          fill: false,
        }]
      },
      options: {
        responsive: true,
      }
    }
    new Chart(
      document.getElementById('hypo6-chart'),
      config
    )
  })
}

async function createHypo2Graph() {
  const url = `${import.meta.env.VITE_APP_ENDPOINT}hypothesis_2`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      const labels = [];
      const fraudulentCounts = [];
      const legitimateCounts = [];

      data = JSON.parse(data);

      // Iterate over the data array
      data.forEach(item => {
        // Push the account age category to labels array
        labels.push(item['Account Age Category']);

        // Check if the item represents fraudulent transactions
        if (item['Is Fraudulent'] === 1) {
          fraudulentCounts.push(item['Count']);
          legitimateCounts.push(0); // Push 0 for legitimate transactions
        } else {
          legitimateCounts.push(item['Count']); // Push count for legitimate transactions
          fraudulentCounts.push(0); // Push 0 for fraudulent transactions
        }
      });

      // Chart configuration
      const config = {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Fraudulent Transactions',
              data: fraudulentCounts,
              backgroundColor: 'rgba(255, 99, 132, 0.8)',
              borderColor: 'rgba(255, 99, 132, 1)',
              borderWidth: 1
            },
            {
              label: 'Legitimate Transactions',
              data: legitimateCounts,
              backgroundColor: 'rgba(75, 192, 192, 0.8)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }
          ]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }
      };

      // Create the chart
      new Chart(document.getElementById('hypo2-bar-chart'), config);
    });
}


async function createHypo3Graph() {
  const url = `${import.meta.env.VITE_APP_ENDPOINT}hypothesis_3`;
  
  fetch(url)
    .then(response => response.json())
    .then(data => {
      // Parse JSON data
      const parsedData = JSON.parse(data);

      // Extract relevant data
      const q3 = parsedData[0]["High Value Threshold"];
      const nonFraudulentCount = parsedData[1]["Transaction Count"];
      const fraudulentCount = parsedData[2]["Transaction Count"];

      // Create chart configuration
      const config = {
        type: 'bar',
        data: {
          labels: ['Non-Fraudulent', 'Fraudulent'],
          datasets: [
            {
              label: 'Transaction Counts',
              data: [nonFraudulentCount, fraudulentCount],
              backgroundColor: [
                'rgba(75, 192, 192, 0.8)', // Blue for non-fraudulent
                'rgba(255, 99, 132, 0.8)', // Red for fraudulent
              ],
              borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)',
              ],
              borderWidth: 1
            }
          ]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          },
          plugins: {
            title: {
              display: true,
              text: `Transaction Counts for High Value Transactions (Q3 Threshold: ${q3})`
            }
          }
        }
      };

      // Create the chart
      new Chart(document.getElementById('hypo3-bar-chart'), config);
    });
}

  
fetchBasicData()
createHypo1Graph()
createHypo5Graph()
createHypo6Graph()
createHypo7Graph()
createHypo8PolarGraph()
createHypo9Graph()
createHypo9Graph()
createHypo2Graph()
createHypo3Graph()
