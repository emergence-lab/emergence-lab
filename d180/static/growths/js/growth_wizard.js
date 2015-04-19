(function(exports) {

    exports.make_rich_text_editable = function(elements) {
        // create div to hook in hallo.js before each rich text editable form
        // field.
        elements.each(function() {
            var form_field = $(this);
            var rich_text = $('<div class="richtext"></div>').html(form_field.html());
            rich_text.insertBefore(form_field);
            form_field.addClass('hidden');

            rich_text.hallo({
                plugins: {
                    'halloformat': {},
                    'halloheadings': {
                        formatBlocks: ['p', 'h2', 'h3', 'h4', 'h5']
                    },
                    'hallolists': {}
                }
            });
        });
        
    }

    exports.enable_rich_text = function(elements_selector, form_selector) {
        exports.make_rich_text_editable($(elements_selector))

        // on form submission, copy the text from the hallo.js divs into the
        // actual form fields.
        $(form_selector).submit(function() {
            $('.richtext').each(function() {
                var text = $(this).html();
                $(this).next().val(text);
            });
        });
    }


    exports.enable_tabbable = function(advance_selector, tab_list_selector, modal_selector) {
        // move tabs when button is clicked and set text approprately for last
        // tab.
        $(advance_selector).click(function() {
            var elem = $(tab_list_selector + ' > li.active');

            // if last tab, toggle modal
            if(elem.is(':last-child')) {
                $(modal_selector).modal('show');
                return
            }

            // else move to next tab
            elem.next().children('a').tab('show');

            // change button to submit for last tab
            if(elem.next().is(':last-child')) {
                $(advance_selector)
                    .html('Submit <span class="glyphicon glyphicon-ok"></span>');
            }
        });

        // change text when tab itself is clicked if needed.
        $(tab_list_selector).on('click', 'a', function() {
            if($(this).parent().is(':last-child')) {
                $(advance_selector)
                    .html('Submit <span class="glyphicon glyphicon-ok"></span>');
            }
            else {
                $(advance_selector)
                    .html('Next Step <span class="glyphicon glyphicon-chevron-right"></span>')
            }
        });
    }

})(this.growth_wizard = {});
