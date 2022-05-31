/* chartjsvariables is a dict type. Keys 
=>'title','tick_max','tick_min','labels','data','legend','ylable_name' */

const color = ['rgb(255, 0, 0)', 'rgb(0, 102, 0)', 'rgb(255, 128, 0)'];
const labels_timestamp = variables_from_DJ.labels;
const variables_from_DJ_data = variables_from_DJ.data;

var datasets = [];
var labels = [];
var index;


// x labels
for (index = 0; index<labels_timestamp.length; index++){
  labels.push(new Date(labels_timestamp[index]*1000));
}


// datasets in data
for (index = 0; index<variables_from_DJ_data.length; index++){
  var each_data = {'borderWidth': 2};
  each_data['label'] = variables_from_DJ.legend[index];
  each_data['backgroundColor'] = color[index];
  each_data['borderColor'] = color[index];
  each_data['data'] = variables_from_DJ.data[index];
  if (variables_from_DJ.legend[index].split("_")[0]==="Temperature"){
//     'legend': ['Temperature_PV', 'Humin_PV', ...]
    each_data['yAxisID'] = 'y';
  } else {   
    each_data['yAxisID'] = 'y2';
  }
  datasets.push(each_data);
}

var data = {
    labels: labels,
    datasets: datasets,
};


var config = {
    type: 'line',
    data,
    options: 
    {
      radius:0, <!-- remove circle on data point -->
      aspectRatio: 1.5,
      plugins:
      {
        legend:
        {
          position: 'top',
      
          labels:
          {
            font:
            {
              size:20  <!-- size of labels -->
            },
      color: 'rgb(252, 224, 45)',
          }
        },
        title:<!-- title of charts     -->
        {
          display:true,
          color: 'rgb(252, 224, 45)',
          text: variables_from_DJ.title,
          font:
          {
            size:20  <!-- size of labels -->
          }     
        }
      },
      interaction:
        {
        intersect: false,
        },
      scales:
      {
        x:
        {
          max: new Date(variables_from_DJ.tick_max),
          min: new Date(variables_from_DJ.tick_min),
          type:'time',
          time: {
          // Luxon format string
          tooltipFormat: 'LLL',
          },
          title:
          {
          display: true,
          text: 'Time(H)',
          color:'rgb(252, 224, 45)',
          font:
          {
            size:30  <!-- size of ticks -->
          }
          },
          ticks: 
          {
            color: 'rgb(252, 224, 45)',
            font:
            {
              size:20  <!-- size of ticks -->
            },
          },
          grid: 
          { 
            borderWidth: 3,
            borderColor: 'rgb(0, 191, 191)',
            <!-- drawBorder: true, -->
            borderDash: [8, 4],
            color: 'rgb(156, 109, 251)',
          },
        },
        y:
        {
          type: 'linear',
          position: 'left',
          display:true,
          title:
          {
            display: true,
            text: 'Temperature(C)',
            color: 'rgb(255, 0, 0)',
            font:
            {
              size:30  <!-- size of ticks -->
            }
          },
          ticks: 
          {
            color: 'rgb(255, 0, 0)',
            font:
            {
              size:20  <!-- size of ticks -->
            }
          },
          grid: 
          { 
            borderWidth: 3,
            borderColor: 'rgb(0, 192, 192)',
            <!-- drawBorder: true, -->
            borderDash: [8, 4],
            color: 'rgb(156, 109, 251)',
    
          },
        },
      }
    }
};

if (variables_from_DJ.ylable_name.length >1 ){
  config.options.scales['y2']={
      type: 'linear',
      display:true,
      position: 'right',
      title:
      {
        display: true,
        text: 'Humidity(%)',
        color: 'rgb(0, 102, 0)',
        font:
        {
          size:30  <!-- size of ticks -->
        }   
      },
      ticks:
      {
        color: 'rgba(0, 102, 0)',
        font:
        {
          size:20  <!-- size of ticks -->
        }
      },
      grid: 
      { 
        drawOnChartArea: false, // only want the grid lines for one axis to show up
      },
  };  
}

var ctx = document.getElementById('myChart');
ctx.style.backgroundColor = 'rgb(0, 0, 0)';

var myChart = new Chart(
ctx,
config
);