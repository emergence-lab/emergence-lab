// When your page loads
$(document).ready(function(){
   // When the toggle areas in your navbar are clicked, toggle them
   $("#search-form").hide();
   $("#search-close").hide();


   $("#search-button").click(function(e){
       e.preventDefault();
       $("#search-form").toggle();
       $("#search-close").toggle();
       $("#search-entry").focus();
       $("#homelink").toggle();
       $("#create-button").toggle();
       $("#apps-dropdown").toggle();
       $("#notifications").toggle();

       $("#search-button").toggle();

       $("#search-form").focusout(function(f){
         $("#search-form").toggle();
         $("#search-entry").focus();
         $("#homelink").toggle();
         $("#create-button").toggle();
         $("#apps-dropdown").toggle();
         $("#search-close").toggle();
         $("#notifications").toggle();

         $("#search-button").toggle();
       });

   });
   $("#search-close").click(function(g){
      $("#search-form").hide();
      $("#homelink").toggle();
      $("#create-button").toggle();
      $("#apps-dropdown").toggle();
      $("#search-close").hide();
      $("#notifications").toggle();
      $("#search-button").toggle();
    });
})
