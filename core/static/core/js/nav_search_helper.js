// When your page loads
$(document).ready(function(){
  $('.navbar-search').hide();

  $('#search-button').click(function(e) {
    $('.navbar-search').show();
    $('#search-entry').focus();
    $('.navbar-button').hide();
  });

  $('#search-entry').focusout(function(e) {
    $('.navbar-search').hide();
    $('.navbar-button').show();
  });

  $('#search-close').click(function(e) {
    e.preventDefault();
    $('.navbar-button').show();
    $('.navbar-search').hide();
  });

});
