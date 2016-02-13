$(function (email, $, undefined) {
    
    $('body')
            .on('click', '#parseEmails', function() {
                var emailList = $('#emailList').val();
                var emailArray = email.parseEmails(emailList);
                $.each(emailArray, function(i) {
                    if (!email.isValidEmailAddress(emailArray[i])) {
                        $('#parsedEmails').append(emailArray[i] + " error" + '\n');
                    } else {
                        $('#parsedEmails').append(emailArray[i] + '\n');   
                    }
                });
                $('#emailList').val('');
            })
            
            .on('click', '#clearEmails', function() {
                $('#parsedEmails').val('');
            })
    
    email.parseEmails = function(emailList) {
        return emailList.split(',');
    }
    
    email.isValidEmailAddress = function (emailAddress) {
        /* from the regex library at https://regex101.com/ */
        var pattern = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
        return pattern.test(emailAddress);
    }
    
}( window.email = window.email || {}, jQuery ));