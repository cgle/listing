function ChatClient(group_id, protocol) {
    
    var protocol = protocol || 'ws://';
    var user_id = user_id;
    var group_id = group_id;
    var url = protocol + location.host + '/ws/chat?group_id=' + group_id;

    var ws = new Websocket(url) || null;

    ws.onopen = on_open;
    ws.onerror = on_error;
    ws.onmessage = on_message;
    ws.onclose = on_close;

    function on_close(e) {
    }

    function on_open(e) {
    }

    function on_error(e) {

    }

    function on_message(e) {
        var message = JSON.parse(e.data);
        switch (message.msg_type) {
            case 'new_message_update':
                break;
            case 'history':
                break;
            default:
                break;
        }
    }

    function send(msg_type, data) {
        var message = {
            msg_type: msg_type,
            data: data
        }
        ws.send(JSON.stringify(message));
    }

    function init() {
        // clear old messages
    };

    $.extend(this, {
        init: init
    });
}
