$(function () {
  process_wizard.enable_tabbable('.next-tab-main', '#main-tab-list', '#submit-modal');

  process_wizard.enable_rich_text('#samples .tab-pane:not(.empty-form) .hallo', 'form');
  process_wizard.make_rich_text_editable($('#info .hallo'));

  var formset = $('#samples div.tab-content .tab-pane').djangoFormset({
    on: {
      formAdded: function(event, form) {
        process_wizard.make_rich_text_editable(form.elem.find('.hallo'));
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
