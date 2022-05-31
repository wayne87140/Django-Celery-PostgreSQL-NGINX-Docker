$(document).ready(function() {

  var $window = $(window);
  
  showViewportSize();
  $window.resize(function() {
    showViewportSize();
  });

  function showViewportSize() {
    $('#width').text($window.width());
    $('#height').text($window.height());
  }

});