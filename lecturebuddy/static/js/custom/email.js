$(function (email, $, undefined) {
    
    $("#parsedEmails").height($('#emailList').height());
    
    $('body')
    
        .on('click', '#parseEmails', function() {
            var emailList = $('#emailList').val();
            var emailArray = email.parseEmails(emailList);
            if (emailArray != "") {
               $('#parsedEmails').show();
                $.each(emailArray, function(i) {
                    if (!email.isValidEmailAddress(emailArray[i])) {
                        $('#parsedEmails > tbody').append("<tr><td>" + emailArray[i] + "</td>" + 
                            "<td>" + lb.generateSVG("error", "invalidEmail") + "</td></tr>")
                    } else {
                        $('#parsedEmails > tbody').append("<tr><td>" + emailArray[i] + "</td>" +
                            "<td>" + lb.generateSVG("check", "validEmail") + "</td></tr>");
                    }
                });
                $('#emailList').val(''); 
            }
        })
        
        .on('click', '#clearEmails', function() {
            $('#parsedEmails > tbody').html('');
            $('#parsedEmails').hide();
        })
        
        .on('click', '#sendEmails', function() {
            console.log('send emails');
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