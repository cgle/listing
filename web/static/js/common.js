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
