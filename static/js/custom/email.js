$(function (email, $, undefined) {
    
    $('body')
                .on('click', '#parseEmails', function() {
                    var emailList = $('#emailList').val();
                    var emailArray = email.parseEmails(emailList);
                    $.each(emailArray, function(i) {
                        $('#parsedEmails').append(emailArray[i] + '\n');
                    });
                })
                
                .on('click', '#clearEmails', function() {
                    $('#parsedEmails').empty();
                })
    
    email.parseEmails = function(emailList) {
        return emailList.split(',');
    }
    
}( window.email = window.email || {}, jQuery ));