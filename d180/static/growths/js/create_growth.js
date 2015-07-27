$(function () {
  process_wizard.enable_tabbable('.next-tab-main', '#main-tab-list', '#submit-modal');

  process_wizard.enable_rich_text('#samples .tab-pane:not(.empty-form) .hallo', 'form');
  process_wizard.make_rich_text_editable($('#comment-modal .hallo'));

  // Set up first tab
  process_wizard.set_up_sample_radio(
    '#id_sample-0-existing_or_new_2',
    '#id_sample-0-existing_or_new_1',
    '#new-sample_sample-0',
    '#existing-sample_sample-0')
  // Only select a default if none is selected
  checked = $('#id_sample-0-existing_or_new_1').attr('checked')
            || $('#id_sample-0-existing_or_new_2').attr('checked');
  if(checked !== 'checked') {
    $('#id_sample-0-existing_or_new_1').attr('checked', true).trigger('click');
  }


  var formset = $('#samples div.tab-content .tab-pane').djangoFormset({
    on: {
      formAdded: function(event, form) {
        // Fix ids that were not updated
        form.elem.find('[id$=__prefix__]').each(function() {
          current = $(this).attr('id');
          updated = current.replace('sample-__prefix__', 'sample-' + form.index);
          console.log('replacing: ' + current + ' with ' + updated);
          $(this).attr('id', updated);
        });

        // Activate radio switching
        process_wizard.set_up_sample_radio(
          '#id_sample-' + form.index + '-existing_or_new_2',
          '#id_sample-' + form.index + '-existing_or_new_1',
          '#new-sample_sample-' + form.index,
          '#existing-sample_sample-' + form.index)
        form.elem.find('#id_sample-' + form.index + '-existing_or_new_1').attr('checked', true).trigger('click');

        // Activate hallojs on rich text fields
        process_wizard.make_rich_text_editable(form.elem.find('.hallo'));

        // Set up tab
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
