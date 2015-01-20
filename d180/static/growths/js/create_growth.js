function advance_tab(advance_button, tab_list, submit_modal) {
  $(advance_button).click(function () {
    var elem = $(tab_list + ' > li.active');

    // toggle modal if last tab
    if(elem.is(':last-child')) {
      $(submit_modal).modal('show');
      return
    }

    // else move to next tab
    elem.next().children('a').tab('show');

    // change button to submit for last tab
    if(elem.next().is(':last-child')) {
      $(advance_button).html('Submit <span class="glyphicon glyphicon-ok"></span>');
    }
  });
}


function close_tab(tab) {
  var content_id = tab.parent().attr('href');
  var is_active = tab.parent().parent().hasClass('active')

  tab.parent().parent().remove();

  if(!is_active) {
    $('#sample-tab-list li:not(#new-sample) a:last').tab('show');
  }

  $(content_id).remove();
}

function get_next_sample_number() {
  // get sorted list of used numbers
  var used_numbers = []
  $('.sample-tab').each(function() {
    used_numbers.push(parseInt($(this).attr('id').split('-')[1]));
  });
  used_numbers.sort();

  // find missing sequential numbers
  for(var i = 0; i < used_numbers.length; ++i) {
    if(i + 1 !== used_numbers[i]) {
      return i + 1;
    }
  }
  return used_numbers.length + 1
}

function new_sample() {
  var source_content = $('#sample-blank');
  var parent = source_content.parent();
  var num_samples = $('.sample-tab').length;
  var sample_number = get_next_sample_number();
  var content_id = 'sample-' + sample_number;

  if(num_samples === 10) {
    console.log('Max number of samples reached');
    return;
  }

  var new_content = source_content.clone().attr('id', content_id).removeClass('hidden').addClass('sample-tab');
  parent.append(new_content);

  var tab_list = $('#sample-tab-list ul');
  var source_tab = tab_list.children('li').first();
  var new_tab = source_tab.clone().removeClass('active');

  $('a[href=#sample-' + (sample_number - 1) + ']').parent().after(new_tab);
  // $('#new-sample').before(new_tab);
  var tab_title = 'Sample ' + sample_number + ' <button class="close close-tab" type="button"><span>&times;</span></button>'
  new_tab.children('a').attr('href', '#' + content_id).html(tab_title).click(function() {
    $(this).tab('show');
  }).tab('show').children('button').click(function() {
    close_tab($(this));
  });
}


$(function () {  
  advance_tab('.next-tab-main', '#main-tab-list', '#submit-modal');

  $('#main-tab-list a').click(function() {
    // clicked last tab
    if($(this).parent().is(':last-child')) {
       $('.next-tab-main').html('Submit <span class="glyphicon glyphicon-ok"></span>');
    }
    else {
      $('.next-tab-main')
        .html('Next Step <span class="glyphicon glyphicon-chevron-right"></span>');
    }
  });

  $('#sample-tab-list li:not(#new-sample) a').click(function () {
    $(this).tab('show');
  }).children('button').click(function () {
    close_tab($(this));
  });

  $('#new-sample a').click(function () {
    new_sample();
  });

});
