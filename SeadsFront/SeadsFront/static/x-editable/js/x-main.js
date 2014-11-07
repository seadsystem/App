$(document).ready(function() {
    //toggle `popup` / `inline` mode
    $.fn.editable.defaults.mode = 'inline';     
    //make username editable

    $('#dev_name').editable({
					type: 'text',
   					 url: '/',  
   					 ajaxOptions: {
   					     type: 'post'
  					  }  
				  });

    $.ajax({
    url: '/',
    response: function(settings) {
        console.log(settings);
       }
    }); 
});