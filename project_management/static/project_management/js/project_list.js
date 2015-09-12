$(document).ready(function(){
    $("div[id^='project_panel_body_']").hide();
    $("ul[id^='invest_list_']").hide();
    $("a[id^='project_deactivate_']").hide();
    $("a[id^='project_edit_']").hide();
    $("span[id^='expand_proj_']").click(function(e){
        var proj = e.target.id.substr(12);
        var listname = 'invest_list_' + proj;
        var projectname = 'project_panel_body_' + proj;
        var deactivate_button_name = 'project_deactivate_' + proj;
        var edit_button_name = 'project_edit_' + proj;
        //var celldisp = 'current_item_' + cellnum;
        var formattedlistid = "ul[id='" + listname + "']";
        //var formatteddispcell = "p[id='" + celldisp + "']";
        var formattedprojectid = "div[id='" + projectname + "']";
        var formatteddeactivateid = "a[id='" + deactivate_button_name + "']";
        var formattededitid = "a[id='" + edit_button_name + "']";
        $(formattedlistid).toggle();
        $(formattedprojectid).toggle();
        $(formatteddeactivateid).toggle();
        $(formattededitid).toggle();

        //$(formatteddispcell).toggle();
    });
});
