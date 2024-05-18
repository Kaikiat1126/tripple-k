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

fetchBasicData()
createHypo1Graph()
createHypo8PolarGraph()
createHypo7Graph()