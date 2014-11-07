$(document).ready(function() {
    $.fn.editable.defaults.mode = 'inline';     
    $('#modify').editable({
   					url: '../dashboard/',   					
				  });
});