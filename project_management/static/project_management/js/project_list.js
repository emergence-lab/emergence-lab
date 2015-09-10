$(document).ready(function(){
    $("div[id^='project_panel_body_']").hide();
    $("ul[id^='invest_list_']").hide();
    $("span[id^='expand_proj_']").click(function(e){
        var proj = e.target.id.substr(12);
        var listname = 'invest_list_' + proj;
        var projectname = 'project_panel_body_' + proj;
        //var celldisp = 'current_item_' + cellnum;
        var formattedlistid = "ul[id='" + listname + "']";
        //var formatteddispcell = "p[id='" + celldisp + "']";
        var formattedprojectid = "div[id='" + projectname + "']";
        $(formattedlistid).toggle();
        $(formattedprojectid).toggle();
        //$(formatteddispcell).toggle();
    });
});
