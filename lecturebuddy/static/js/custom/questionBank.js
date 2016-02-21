$(function (questionBank, $, undefined) {
    
    $('body')
    
        .on('click', '#shortAnswerButton', function() {
            $('.title > h2').html('Short Answer');
            $('#allQuestions').html('');
            var numQuestions = $(this).attr('questions');
            console.log(numQuestions);
            for (numQuestions) {
                var questionForm = new FormData();
                questionForm.append('questionName', );
                questionForm.append('questionID', )
                $.ajax({
                    url: '/getQuestionBank',
                    type: 'POST',
                    contentType: 'application/json',
                    dataType: 'html',
                    success: function(response) {
                       console.log(response);
                    }, 
                    error: function(error) {
                       console.log("error" + JSON.stringify(error));
                    }
                });   
            } 
        })
        
        .on('click', '#mapButton', function() {
            $('.title > h2').html('Map');
            $('#allQuestions').html('');
            var numQuestions = $(this).attr('questions');
            console.log(numQuestions);
        })
        
        .on('click', '#multipleChoiceButton', function() {
            $('.title > h2').html('Multiple Choice');
            $('#allQuestions').html('');
            var numQuestions = $(this).attr('questions');
            console.log(numQuestions);
        })
    
}( window.questionBank = window.questionBank || {}, jQuery ));