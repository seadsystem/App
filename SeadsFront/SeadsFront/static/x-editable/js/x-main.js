$(document).ready(function() {
    $.fn.editable.defaults.mode = 'inline';     
    $('.modify').editable({
    				name: "modify",
   					url: '../dashboard/',   					
				  });
});