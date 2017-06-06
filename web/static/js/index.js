$(function() {
    function handle_create_group() {
        var $create_group_btn = $('#create-chat-group-submit-btn');
        var $create_group_input = $('#create-chat-group-input');
        var $message_box = $('#create-chat-group-message-box');
        $create_group_btn.on('click', function() {
            var group_name = $create_group_input.val();
            hide_message($message_box);
            if (group_name === '') {
                pop_message($message_box, 'Empty group name', 'error');
                return false;
            }

            var callback = function(d,e) {
                if (e != null) { 
                    pop_message($message_box, e.responseText, 'error');
                    return false;
                }
                open_page('/');
            }
            
            send_create_group(group_name, callback);
        });
    }
    

    handle_create_group();
});
