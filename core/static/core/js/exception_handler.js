(function(exports) {

    function exception_handler(url) {
        // collect tags
        tags = [];
        $('input:checked[type="checkbox"][name="tag"]').each(function() {
            tags.push($(this).val());
        });

        // send ajax request
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': '{{csrf_token}}',
                'path': '{{request.path}}',
                'user': '{{user.username}}',
                'title': $('input[name="title"]').val(),
                'complaint': $('#exception-text').val(),
                'tag': tags
            },
            success: function() {
                $('#exception-modal').modal('hide');
                $('input[name="title"]').val('Exception Form Issue');
                $('#exception-text').val('');
                $('input:checked[type="checkbox"][name="tag"]').each(function() {
                    $(this).prop('checked', false);
                });
            },
            error: function(response) {
                console.error(response.message);
            }
        });

        return false;
    }

    exports.enable_exception_handling = function(selector, url) {
        $(selector).click(function() {
            exception_handler.call(this, url);
        });
    }

})(this.exception_handler = {});
