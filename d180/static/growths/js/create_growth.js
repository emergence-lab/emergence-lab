function advance_tab() {
  $('.next-tab-main').click(function () {
    elem = $('#main-tab-list > li.active');

    // toggle modal if last tab
    if(elem.is(':last-child')) {
      $('#submit-modal').modal('show');
      return
    }

    // else move to next tab
    elem.next().children('a').tab('show');

    // change button to submit for last tab
    if(elem.next().is(':last-child')) {
      $('.next-tab-main').text('Submit');
    }
  });
}


$(function () {  
  advance_tab();

  $('#main-tab-list a').click(function() {
    // clicked last tab
    if($(this).parent().is(':last-child')) {
       $('.next-tab-main').text('Submit');
    }
    else {
      $('.next-tab-main')
        .html('Next Step <span class="glyphicon glyphicon-chevron-right"></span>');
    }
  });

  $('.next-tab-samples').click(function () {
    elem = $('#sample-tab-list > li.active').removeClass('active')
                                            .next().addClass('active');
  });

});
