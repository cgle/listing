function reload_page() {
    location.reload();
}

function open_page(path) {
    var path = path || '/';
    window.open(path, '_self');
}


function pop_message($div, content, level) {
    var level = level || 'normal';
    $div.addClass('message-box ' + level);
    $div.text(content);
    $div.show();
}

function hide_message($div) {
    $div.hide();
}

function on_enter_handler($div, func) {
    $div.keypress(function(e) {
        if (e.which == 13) {
            func();
            return false;
        }
    });
}

function send_ajax(url, data, method, callback) {
    var callback = callback || function(d,e) {
        if (e != null) { alert(e.responseText); return false; }
        console.log(d);
        return true;
    }
    
    var data = JSON.stringify(data);

    $.ajax({
        url: url,
        method: method,
        data: data,
        success: function(d) {
            callback(d,null);
        },
        error: function(e) {
            callback(null,e);
        }
    });
}

function send_login(email, password, callback) {
    var data = {
        email: email,
        password: password
    }
    send_ajax('/login', data, 'POST', callback);
}

function send_register(email, password, callback) {
    var data = {
        email: email,
        password: password
    }
    send_ajax('/register', data, 'POST', callback);
}

function send_create_group(group_name, callback) {
    var data = {
        group_name: group_name
    }
    send_ajax('/chat-groups/create', data, 'POST', callback);    
}

function send_get_groups(is_creator, callback) {
    var data = {
        is_creator: is_creator
    }
    send_ajax('/chat-groups/get', data, 'GET', callback);
}

function send_add_user_to_chat_group(email, group_id, callback) {
    var data = {
        email: email,
        group_id: group_id
    }
    send_ajax('/chat-groups/add-user', data, 'POST', callback);
}

function send_remove_user_from_chat_group(user_id, group_id, callback) {
    var data = {
        user_id: user_id,
        group_id: group_id
    }
    send_ajax('/chat-groups/remove-user', data, 'POST', callback);
}

function handle_popover() {
    var $popover_link = $('.popover-link');
    $popover_link.on('click', function(e) {
        var left = e.clientX + 'px';
        var top = e.clientY + 'px';
        var $popover = $(this.getAttribute('data-target'));
        $popover.toggle();
    });
}


function handle_modal() {
    var $modal_link = $('.open-modal-link');
    $modal_link.on('click', function(e) {
        var $modal = $(this.getAttribute('data-target'));
        $modal.show();
        $modal.off('click');
        $modal.on('click', function(e) {
            if (e.target == $modal[0]) {
                $modal.hide();
            }
        });
    });
}

handle_popover();
handle_modal();
