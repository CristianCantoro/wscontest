$(document).ready(function() {
    "use strict";

    $('#license').click(function (e) {
        e.preventDefault();
        $("#license-text").slideToggle('slow');
        return false;
    });

    $("#license-text").hide();

    $("#inputform").submit(function(e) {

        e.preventDefault();

        $('#submit').attr('disabled', 'disabled');
        $('#change-password').attr('disabled', 'disabled');
       
        $.ajax({
            type: "POST",
            data: $(this).serialize(),
            success: function(post_response) {
                $('#submit').removeAttr('disabled');
                $('#change-password').removeAttr('disabled');
                $('#results-placeholder').hide().html(post_response).fadeIn(1500);
            },
        });

        return false;
    });

});
