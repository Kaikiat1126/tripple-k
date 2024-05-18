import './style.css'

async function fetchBasicData() {
  const basicDataUrl = `${import.meta.env.VITE_APP_ENDPOINT}basic_analysis`
  fetch(basicDataUrl).then(response => response.json()).then(data => {
    const total_transaction = document.getElementById('total-transaction')
    const fraudulent_amount = document.getElementById('fraudulent-amount')
    const fraudulent_count = document.getElementById('fraudulent-count')
    const fradulent_rate = document.getElementById('fraudulent-rate')
    total_transaction.innerHTML = data.total_transaction
    fraudulent_amount.innerHTML = data.total_fraudulent_amount
    fraudulent_count.innerHTML = data.total_fraudulent
    fradulent_rate.innerHTML = data.fraudulent_rate + '%'
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
    const hour_count = []
    const tx_by_hour = data['Fraudulent Transactions by Hour']
    for (const key in tx_by_hour) {
      hour_labels.push(key)
      hour_count.push(tx_by_hour[key]["Is Fraudulent"])
    }
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
    new Chart(document.getElementById('hypo1-chart'),config)
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

async function createHypo4Graph() {
  const url = `${import.meta.env.VITE_APP_ENDPOINT}hypothesis_4`;
  
  fetch(url)
    .then(response => response.json())
    .then(data => {
      const labels = [];
      const nonFraudulentCounts = [];
      const fraudulentCounts = [];

      data = JSON.parse(data);

      data.forEach(item => {
        labels.push(item['Product Category']);
        nonFraudulentCounts.push(item['Non-Fraudulent Transactions']);
        fraudulentCounts.push(item['Is Fraudulent']);
      });

      const config = {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Non-Fraudulent Transactions',
              data: nonFraudulentCounts,
              backgroundColor: 'rgba(75, 192, 192, 0.8)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            },
            {
              label: 'Fraudulent Transactions',
              data: fraudulentCounts,
              backgroundColor: 'rgba(255, 99, 132, 0.8)',
              borderColor: 'rgba(255, 99, 132, 1)',
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

      new Chart(document.getElementById('hypo4-bar-chart'), config);
    });
  }



fetchBasicData()
createHypo1Graph()
createHypo8PolarGraph()
createHypo7Graph()
createHypo2Graph()
createHypo3Graph()
createHypo4Graph()
