$('p').each(function(index, item) {
    if($.trim($(item).text()) === "") {
        $(item).slideUp(); // $(item).remove();
    }
});
