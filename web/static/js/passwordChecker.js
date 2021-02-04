$(document).ready(function () {  
    $('#password1').keyup(function () {  
        $('#strengthMessage').html(checkStrength($('#password1').val()))  
    });
    $("#password2").keyup(function () {
        $('#matchMessage').html(checkPasswordMatch($('#password2').val()))});

    function checkStrength(password) {  
        var strength = 0 
        if (password.length < 7) {  
            $('#strengthMessage').removeClass()  
            $('#strengthMessage').addClass('Short')
            return 'Password too short'
        }  
        if (password.length > 7) strength += 1  
        // If password contains both lower and uppercase characters, increase strength value.  
        if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1  
        // If it has numbers and characters, increase strength value.  
        if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) strength += 1  
        // If it has one special character, increase strength value.  
        if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1  
        // If it has two special characters, increase strength value.  
        if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1  
        // Calculated strength value, we can return messages  
        // If value is less than 2  
        if (strength < 2) {
            $('#strengthMessage').removeClass()
            $('#strengthMessage').addClass('Weak') 
            return 'Weak'  
        } else if (strength == 2) {  
            $('#strengthMessage').removeClass()  
            $('#strengthMessage').addClass('Good')  
            return 'Good'  
        } else {  
            $('#strengthMessage').removeClass()  
            $('#strengthMessage').addClass('Strong')  
            return 'Strong'  
        }  
    }

    function checkPasswordMatch() {
        var password = $("#password1").val();
        var confirmPassword = $("#password2").val();

        if (confirmPassword.length < 7) {
            $('#matchMessage').removeClass();
            $('#matchMessage').addClass('Short');
            return 'Password is too short';
        }
        else if (password != confirmPassword) {
            $('#matchMessage').removeClass();
            $('#matchMessage').addClass('NotMatch');
            return 'Passwords does not match';
        }
        else {
            $('#matchMessage').removeClass();
            $('#matchMessage').addClass('Match'); 
            return 'Passwords matched'; 
        }
    }
});