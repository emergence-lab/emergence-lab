// When your page loads
$(document).ready(function() {

  $('#search-button').click(function(e) {
    $('.navbar-search').removeClass('hidden')
    $('#search-entry').focus();
    $('.navbar-button').addClass('hidden')
  });

  $('#search-entry').focusout(function(e) {
    $('.navbar-search').addClass('hidden')
    $('.navbar-button').removeClass('hidden')
  });

  $('#search-close').click(function(e) {
    e.preventDefault();
    $('.navbar-button').removeClass('hidden')
    $('.navbar-search').addClass('hidden')
  });

});
