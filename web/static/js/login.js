$(function() {
    
    var $email_input = $('#login-email-input');
    var $password_input = $('#login-password-input');
    var $login_submit_btn = $('#login-submit-btn');
    var $login_msg_box = $('#login-msg-box');
    
    function login() {
        var email = $email_input.val();
        var password = $password_input.val();
        
        if (email === '' || password === '') {
            pop_message($login_msg_box, 'Please type both email and password', 'error');
            return false;
        }

        function callback(d,e) {
            if (e != null) { 
                pop_message($login_msg_box, e.responseText, 'error');
                return false;
            }
            open_page('/');
        }
        
        send_login(email, password, callback);
    };


    $login_submit_btn.on('click', login);
    on_enter_handler($email_input, login);
    on_enter_handler($password_input, login);

});
