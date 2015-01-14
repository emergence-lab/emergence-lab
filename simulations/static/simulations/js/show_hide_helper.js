$(document).ready(function(){
    $('#device input[type="radio"]').click(function(){
        if($(this).attr("value")=="upload"){
            $("#device .box").hide();
            $("#device .upload").show();
        }
        if($(this).attr("value")=="edit"){
            $("#device .box").hide();
            $("#device .edit").show();
        }
    });
    $('#materials input[type="radio"]').click(function(){
        if($(this).attr("value")=="upload"){
            $("#materials .box").hide();
            $("#materials .upload").show();
        }
        if($(this).attr("value")=="edit"){
            $("#materials .box").hide();
            $("#materials .edit").show();
        }
    });
    $('#physics input[type="radio"]').click(function(){
        if($(this).attr("value")=="upload"){
            $("#physics .box").hide();
            $("#physics .upload").show();
        }
        if($(this).attr("value")=="edit"){
            $("#physics .box").hide();
            $("#physics .edit").show();
        }
    });
    $('#file_tabs a').click(function (e) {
        e.preventDefault()
        $(this).tab('show')
})
});

