// Import the functions you need from the SDKs you need
import {initializeApp} from "https://www.gstatic.com/firebasejs/10.6.0/firebase-app.js";
import {getAnalytics} from "https://www.gstatic.com/firebasejs/10.6.0/firebase-analytics.js";
import {getDatabase, ref, onValue,runTransaction,get} from "https://www.gstatic.com/firebasejs/10.6.0/firebase-database.js";
// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyA7ot8doQLRJ83hK5xz15HZCvSKKZl2U9E",
  authDomain: "projetoiot-6f20f.firebaseapp.com",
  databaseURL: "https://projetoiot-6f20f-default-rtdb.firebaseio.com",
  projectId: "projetoiot-6f20f",
  storageBucket: "projetoiot-6f20f.appspot.com",
  messagingSenderId: "313644760979",
  appId: "1:313644760979:web:662c5f33109b45d8ebf266",
  measurementId: "G-247KV0XP91"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const database = getDatabase(app);
const LDR = ref(database, 'LDR');
const LDR2 = ref(database, 'LDRATUAL');
const ldrChartCanvas = document.getElementById('ldrChart').getContext('2d');
let ldrChart;

onValue(LDR2, onNewData('valorLDR'));

function onNewData(currentValueEl) {
  return function(snapshot) {
    var readings = snapshot.val();
    if (readings) {
      var currentValue;
      var data = [];
      var labels = [];
      for (var key in readings) {
        currentValue = readings[key];
        var formattedValue = currentValue.toFixed(2);  // Limita para 2 casas decimais
        data.push(formattedValue);
        labels.push(key);
      }
      document.getElementById(currentValueEl).innerText = "Voltagem Atual " + formattedValue + 'V';
    }
  };
}

onValue(LDR, onNewDataLDRGraph('valorLDR'));

function onNewDataLDRGraph(currentValueEl) {
  return function (snapshot) {
    var readings = snapshot.val();
    if (readings) {
      var currentValue;
      var data = [];
      var labels = [];

      var currentDate = new Date();
      var last24Hours = new Date(currentDate.getTime() - 24 * 60 * 60 * 1000);

      for (var key in readings) {
        currentValue = readings[key];
        var dataDate = new Date(key);
        if (dataDate >= last24Hours) {
          data.push(currentValue);
          labels.push(dataDate.toLocaleTimeString('pt-BR', { hour: 'numeric', minute: 'numeric' }));
        }
      }

      // Atualize o gráfico com os novos dados
      updateChart(data, labels);
    }
  };
}


function toggleLight() {
  const database = getDatabase();
  const lightRef = ref(database, 'luz');

  runTransaction(lightRef, (currentValue) => {
    // Verifica se o valor atual é nulo ou undefined
    if (currentValue == null) {
      return false; // Define como falso se o valor for nulo ou undefined
    }

    // Inverte o valor
    return !currentValue;
  }).then((transactionResult) => {
    if (transactionResult.committed) {
      console.log('Transação realizada com sucesso!');
      // Atualiza o status da luz após a transação
      updateLightStatus();
    } else {
      console.log('A transação foi abortada.');
    }
  }).catch((error) => {
    console.error('Erro durante a transação:', error);
  });
}

function updateLightStatus() {
  const lightRef = ref(database, 'luz');
  // Lê o valor diretamente do Firebase
  get(lightRef).then(function(snapshot) {
    var isLightOn = snapshot.val();
    var statusElement = document.getElementById('lightStatus');

    if (isLightOn !== null && isLightOn !== undefined) {
      statusElement.innerText = 'Status da Luz: ' + (isLightOn ? 'Acesa' : 'Apagada');
    } else {
      statusElement.innerText = 'Status da Luz: Aguardando atualização...';
    }
  }).catch(function(error) {
    console.error('Erro ao ler o status da luz:', error);
  });
}


function updateChart(data, labels) {
  if (!ldrChart) {
    // Se o gráfico ainda não foi inicializado, crie-o
    ldrChart = new Chart(ldrChartCanvas, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Voltagem do LDR',
          data: data,
          fill: false,
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          x: {
            type: 'category',
            labels: labels,
            maxRotation: 0, // Ajusta a rotação dos rótulos
            minRotation: 0,
            ticks: {
              stepSize: 1, // Ajusta o espaçamento entre os rótulos
              maxTicksLimit: 6 // Define o número máximo de rótulos exibidos
            }
          },
          y: {
            beginAtZero: true
          }
        }
      }
    });
  } else {
    // Se o gráfico já foi inicializado, atualize os dados
    ldrChart.data.labels = labels;
    ldrChart.data.datasets[0].data = data;
    ldrChart.update();
  }
}



document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('toggleButton').addEventListener('click', toggleLight);

  // Adiciona uma chamada inicial para updateLightStatus
  updateLightStatus();
  const lightRef = ref(database, 'luz');
  // Monitora mudanças no valor do nó 'luz' em tempo real
  onValue(lightRef, function(snapshot) {
    updateLightStatus();
  });
});