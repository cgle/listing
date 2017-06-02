$(function() {
    var $email_input = $('#register-email-input');
    var $password_input = $('#register-password-input');
    var $password_again_input = $('#register-password-again-input');
    var $register_submit_btn = $('#register-submit-btn');
    var $register_msg_box = $('#register-msg-box');

    function register() {
        var email = $email_input.val();
        var password = $password_input.val();
        var password_again = $password_again_input.val();

        if (email === '' || password === '' || password_again === '') {
            pop_message($register_msg_box, 'Please fill in all fields', 'error');
            return false;
        }

        if (password != password_again) {
            pop_message($register_msg_box, 'Password (again) not match', 'error');
            return false;
        }

        var callback = function(d,e) {
            if (e != null) {
                pop_message($register_msg_box, e.responseText, 'error');
                return false;
            }
            open_page('/');
        }

        send_register(email, password, callback);
    }

    $register_submit_btn.on('click', register);
    on_enter_handler($email_input, register);
    on_enter_handler($password_input, register);
    on_enter_handler($password_again_input, register);
});
