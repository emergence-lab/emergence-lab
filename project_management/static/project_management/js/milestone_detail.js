(function(exports) {

    exports.make_rich_text_editable = function(elements) {
        // create div to hook in hallo.js before each rich text editable form
        // field.
        elements.each(function() {
            var form_field = $(this);
            var rich_text = $('<div class="richtext" id="note_hallo_field"></div>').html(form_field.text());
            rich_text.insertBefore(form_field);
            form_field.addClass('hidden');

            rich_text.hallo({
                plugins: {
                    'halloformat': {},
                    'halloheadings': {
                        formatBlocks: ['p', 'h2', 'h3', 'h4', 'h5']
                    },
                    'hallolists': {},
                    'hallolink': {},
                },
                toolbar: 'halloToolbarFixed',
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

})(this.milestone_detail = {});
