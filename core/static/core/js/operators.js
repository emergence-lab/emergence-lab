function deactivate_object(csrf_token, url) {
    $.ajax({
        data: "csrfmiddlewaretoken=" + csrf_token + "&action=deactivate&id=" + $(this).parents('.list-group-item').data('pk'),
        type: "post",
        url: url,
        success: function(response) {
            objects = JSON.parse(response.objects)
            items = []
            $.each(objects, function(i, item) {
                $('[data-pk="' + item.pk + '"]').appendTo('#former').children('.ajax-deactivate').remove()
            })
            $('.alert').html(response.message);
            $('.alert').removeClass('alert-info alert-warning').addClass('alert-success');
        },
        error: function(response) {
            $('.alert').html(response.message);
            $('.alert').removeClass('alert-info alert-success').addClass('alert-warning');
        }
    });
    return false;
}


function delete_object(csrf_token, url) {
    $.ajax({
        data: "csrfmiddlewaretoken=" + csrf_token + "&action=delete&id=" + $(this).parents('.list-group-item').data('pk'),
        type: "post",
        url: url,
        success: function(response) {
            objects = JSON.parse(response.objects)
            items = []
            $.each(objects, function(i, item) {
                $('[data-pk="' + item.pk + '"]').remove()
            })
            $('.alert').html(response.message);
            $('.alert').removeClass('alert-info alert-warning').addClass('alert-success');
        },
        error: function(response) {
            $('.alert').html(response.message);
            $('.alert').removeClass('alert-info alert-success').addClass('alert-warning');
        }
    });
    return false;
}


function create_object(csrf_token, url) {
    $.ajax({
        data: $(this).serialize() + "&action=create",
        type: $(this).attr("method"),
        url: $(this).attr("action"),
        success: function(response) {
            $('#add-operator-modal').modal("toggle");
            $('#id_name').val('')
            objects = JSON.parse(response.objects)
            base = $('#current .list-group-item').last()
            items = []
            $.each(objects, function(i, item) {
                tmp = base.clone()
                tmp = tmp.data('pk', item.pk)
                tmp.children('.name').html(item.fields.name)
                items.push(tmp)
            })
            $('#current').append(items)
            $('.ajax-deactivate').click(function() {
                return deactivate_object(csrf_token, url)});
            $('.ajax-delete').click(function() {
                return deactivate_object(csrf_token, url)});
            $('.alert').html(response.message);
            $('.alert').removeClass('alert-info alert-warning').addClass('alert-success');
        },
        error: function(response) {
            $('.alert').html(response.message);
            $('.alert').removeClass('alert-info alert-success').addClass('alert-warning');
        }
    });
    return false;
}
