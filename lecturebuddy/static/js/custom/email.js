$(function (email, $, undefined) {
    
    $('body')
    
        .on('click', '#parseEmails', function() {
            $('#parsedEmails > tbody').html('');
            var emailList = $('#emailList').val();
            var emailArray = email.parseEmails(emailList);
            if (emailArray != "") {
               $('#parsedEmails').show();
                $.each(emailArray, function(i) {
                    console.log(emailArray[i]);
                    if (!email.isValidEmailAddress(emailArray[i])) {
                        $('#parsedEmails > tbody').append("<tr><td>" + emailArray[i] + "</td>" + 
                            "<td>" + lb.generateSVG("error", "emailStatusIcon invalidEmail") + "</td></tr>")
                    } else {
                        $('#parsedEmails > tbody').append("<tr><td class='emailEntry'>" + emailArray[i] + "</td>" +
                            "<td>" + lb.generateSVG("check", "emailStatusIcon validEmail") + "</td></tr>");
                    }
                });
                if ($('#parsedEmails > tbody').find('.invalidEmail').length) {
                    $('#sendEmails').prop('disabled', true);   
                } else {
                    $('#sendEmails').prop('disabled', false);   
                }
            }
        })
        
        .on('click', '#clearEmails', function() {
            $('#parsedEmails > tbody').html('');
            $('#parsedEmails').hide();
        })
        
        .on('click', '#sendEmails', function() {
            var emailArray = [];
            var emailsForm = new FormData();
            var emailTable = $('#parsedEmails');
            emailTable.find('.emailEntry').each(function() {
                emailArray.push($(this).html());
            })
            emailsForm.append('emails', emailArray);
            $.ajax({
                url: '/sendEmails',
                data: emailsForm,
                type: 'POST',
                processData: false,
                contentType: false,
                success: function(response) {
                    if (response['message'] == 'success') {
                        $('#emailInviteWrapper').append("<span class='byline'><font color='green'>All emails have sent successfully</font></span>")
                    }
                },
                error: function(error) {
                    return("error" + JSON.stringify(error));
                }
            })
        })
    
    email.parseEmails = function(emailList) {
        return $.map(emailList.split(','), $.trim);
    }
    
    email.isValidEmailAddress = function (emailAddress) {
        /* from the regex library at https://regex101.com/ */
        var pattern = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
        return pattern.test(emailAddress);
    }
    
}( window.email = window.email || {}, jQuery ));