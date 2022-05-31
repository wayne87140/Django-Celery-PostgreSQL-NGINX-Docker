function refreshPage() {
  $.ajax({
  url: content_URL,
  success: function(data) {
    $('#content').html(data);
  }
  });
};

$(document).ready(function($){
  refreshPage();
  var int = setInterval("refreshPage()", 5000)
});


//var content_URL = "{% url 'main:main' %}";