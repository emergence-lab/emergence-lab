function make_rich_text_editable(elements) {
  elements.each(function() {
    var form_field = $(this);
    var rich_text = $('<div class="richtext"></div>').html('');
    rich_text.insertBefore(form_field);
    form_field.addClass('hidden');

    rich_text.hallo({
      plugins: {
        'halloformat': {},
        'halloheadings': {formatBlocks: ['p', 'h2', 'h3', 'h4', 'h5']},
        'hallolists': {}
      }
    });
  });
}


function submit_form() {
  console.log('submitting form');
}


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
      $(advance_button).html('Submit <span class="glyphicon glyphicon-ok"></span>')
    }
  });
}


$(function () {  
  advance_tab('.next-tab-main', '#main-tab-list', '#submit-modal');

  make_rich_text_editable($('#samples .tab-pane:not(.empty-form) .hallo'));

  $('form').submit(function() {
    $('.richtext').each(function() {
      var text = $(this).html();
      $(this).next().val(text);
    });
  });

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

  var formset = $('#samples div.tab-content .tab-pane').djangoFormset({
    on: {
      formAdded: function(event, form) {
        make_rich_text_editable(form.elem.find('.hallo'));
        form.tab.elem.removeClass('hidden');
        form.tab.elem.find('a').html('<span class="tab-title">Sample ' + (form.index + 1) + '</span><button class="close close-tab" type="button"><span>&times;</span></button>');
        form.tab.elem.find('button').click(function(event) {
          formset.deleteForm(form.index);
          for(var i = 1; i < formset.forms.length; ++i) {
            formset.forms[i].tab.elem.find('.tab-title').text('Sample ' + (i + 1))
          }
        });
      }
    }
  });

  $('a[data-action=add-form]').click(function(event) {
    formset.addForm();
  });

});
