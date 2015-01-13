$(document).ready(function(){
    $('#new_item_form').hide();
    $("div[id^='update_item_']").hide();
    $("ul[id^='invest_list_']").hide();
    $("a[id^='expand_proj_']").click(function(e){
        var proj = e.target.id.substr(12);
        var listname = 'invest_list_' + proj;
        //var celldisp = 'current_item_' + cellnum;
        var formattedlistid = "ul[id='" + listname + "']";
        //var formatteddispcell = "p[id='" + celldisp + "']";
        $(formattedlistid).toggle();
        //$(formatteddispcell).toggle();
    });
    $("a[id^='edit_item_']").click(function(e){
        var cellnum = e.target.id.substr(10);
        var cellname = 'update_item_' + cellnum;
        var celldisp = 'current_item_' + cellnum;
        var formattededitcell = "div[id='" + cellname + "']";
        var formatteddispcell = "p[id='" + celldisp + "']";
        $(formattededitcell).toggle();
        $(formatteddispcell).toggle();
    });
    $('#add_item_button').click(function (e) {
        $('#new_item_form').toggle();
        $('#new_action_comment').focus();
        $('#new_action_comment').focusout(function(f){
            $('#new_item_form').hide();
        });
    });
});
$(function(){
  var hash = window.location.hash;
  hash && $('ul.nav a[href="' + hash + '"]').tab('show');

  $('.nav-tabs a').click(function (e) {
    $(this).tab('show');
    var scrollmem = $('body').scrollTop();
    window.location.hash = this.hash;
    $('html,body').scrollTop(scrollmem);
  });
});
