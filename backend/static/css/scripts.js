function renderCharts(deptData, conditionData) {
  new Chart(document.getElementById('deptChart'), {
    type: 'bar',
    data: {
      labels: Object.keys(deptData),
      datasets: [{
        label: 'Assets by Department',
        data: Object.values(deptData),
        backgroundColor: '#007bff'
      }]
    }
  });

  new Chart(document.getElementById('conditionChart'), {
    type: 'pie',
    data: {
      labels: Object.keys(conditionData),
      datasets: [{
        label: 'Asset Condition',
        data: Object.values(conditionData),
        backgroundColor: ['#28a745', '#ffc107', '#dc3545']
      }]
    }
  });
}

