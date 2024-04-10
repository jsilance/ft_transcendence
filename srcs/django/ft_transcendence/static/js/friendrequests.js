////////////////////////////////////////////////////////////////////////////////
//                           FRIEND SYSTEM                                    //
////////////////////////////////////////////////////////////////////////////////

function sendFriendRequest(id, csrf) {
    payload = {
        "csrfmiddlewaretoken": csrf,
        "receiver_user_id": id,
    }
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/accounts/friend_request/",
        timeout: 5000,
        data: payload,
        success: function(data) {
            if (data['response'] == "Friend request sent."){
                onFriendRequestSent(id, csrf)
            }
            else if (data['response'] != null) {
                alert(data['response']);
            }
        },
        error: function(data) {
            alert("Something went wrong." + data)
        },
    })
}

function onFriendRequestSent(id, csrf) {
    var status_bar = document.getElementById("header_status_bar");
    status_bar.innerHTML = "";

    var cancel_request_btn = createCancelFriendRequestBtn(id, csrf);

    status_bar.append(cancel_request_btn);
}

////////////////////////////////////////////////////////////////////////////////

function cancelFriendRequest(id, csrf) {

    payload = {
        "csrfmiddlewaretoken": csrf,
        "receiver_user_id": id,
    }
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/accounts/cancel_friend_request/",
        data: payload,
        timaout: 5000,
        success: function(data) {
            if (data['response'] == "Friend request cancelled") {
                onFriendRequestCanceled()
            }
            else if (data.response != null) {
                alert(data.response)
            }
        },
        error: function(data) {
            alert("Something went wrong: " + data)
        },
        complete: function() {
            
        },
    })
}

function onFriendRequestCanceled() {
    var status_bar = document.getElementById("header_status_bar");
    status_bar.innerHTML = ""
    id = status_bar.getAttribute("data-id")
    csrf = status_bar.getAttribute("data-csrf")

    var addFriendBtn = createAddFriendBtn(id, csrf);
    var blockBtn = createBlockUnblockBtn(id, "block");

    status_bar.append(addFriendBtn, blockBtn);
}

////////////////////////////////////////////////////////////////////////////////

function acceptFriendRequest(friend_request_id, container) {
    var url = "/accounts/accept_friend_request/" + friend_request_id
    $.ajax({
        type: "GET",
        dataType: "json",
        url: url,
        timaout: 5000,
        success: function(data) {
            if (data['response'] == "Friend request accepted") {
                onFriendRequestAccepted(container)
            }
            else if (data.response != null) {
                alert(data.response)
            }
        },
        error: function(data) {
            alert("Something went wrong: " + data)
        },
        complete: function() {
            
        },
    })
}

function onFriendRequestAccepted(origin) {
    container = document.getElementById(origin);
    container.innerHTML = "";
    id = container.getAttribute('data-id');
    csrf = container.getAttribute('data-csrf');
    
    if (origin === "header_status_bar") {
        var unfriend_btn = createUnfriendBtn(id, csrf);
        var dm_btn = createMessageBtn();
        var block_btn = createBlockUnblockBtn(id, "block");
        container.append(unfriend_btn, dm_btn, block_btn);
    } else {
        // TODO: update the friend list widget
        ;
    }
}

////////////////////////////////////////////////////////////////////////////////

function declineFriendRequest(friend_request_id, origin) {
    var url = `/accounts/decline_friend_request/${friend_request_id}`;
    $.ajax({
        type: "GET",
        dataType: "json",
        url: url,
        timaout: 5000,
        success: function(data) {
            if (data['response'] == "Friend request declined") {
                onFriendRequestDeclined(origin);
            }
            else if (data.response != null) {
                alert(data.response)
            }
        },
        error: function(data) {
            alert("Something went wrong: " + data)
        },
        complete: function(data) {
            
        },
    })
}

function onFriendRequestDeclined(origin) {
    var status_bar = document.getElementById(origin);
    status_bar.innerHTML = ""
    id = status_bar.getAttribute("data-id");
    csrf = status_bar.getAttribute("data-csrf");

    if (origin === "header_status_bar") {
        var addFriendBtn = createAddFriendBtn(id, csrf);
        var blockBtn = createBlockUnblockBtn(id, "block");
        status_bar.append(addFriendBtn, blockBtn);
    } else {
        ;
    }
}

////////////////////////////////////////////////////////////////////////////////

function removeFriend(id, csrf) {
    payload = {
        "csrfmiddlewaretoken": csrf,
        "receiver_user_id": id,
    }
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/accounts/friend_remove/",
        timeout: 5000,
        data: payload,
        success: function(data) {
            if (data['response'] == "Successfully removed that friend"){
                onFriendRemoved()
            }
            else if (data['response'] != null) {
                alert(data['response']);
            }
        },
        error: function(data) {
            alert("Something went wrong." + data)
        },
        complete: function(data) {
            
        }
    })
}

function onFriendRemoved() {
    var status_bar = document.getElementById("header_status_bar");
    status_bar.innerHTML = ""
    id = status_bar.getAttribute("data-id");
    csrf = status_bar.getAttribute("data-csrf")
    
    var add_friend_btn = createAddFriendBtn(id, csrf)
    var block_btn = document.createBlockUnblockBtn(id, "block");

    status_bar.append(add_friend_btn, block_btn);
}

////////////////////////////////////////////////////////////////////////////////

function blockUnblock(id, action) {
    var url = `/accounts/blocking?user_id=${id}&action=${action}`
    $.ajax({
        type: "GET",
        dataType: "json",
        url: url,
        timaout: 5000,
        success: function(data) {
            onBlockedUnblocked(action);
        },
        error: function(data) {
            alert(data['response'], 'Error');
        },
        complete: function(data) {
            
        },
    })
}

function onBlockedUnblocked(action) {
    var status_bar = document.getElementById("header_status_bar");
    status_bar.innerHTML = ""
    id = status_bar.getAttribute("data-id");
    csrf = status_bar.getAttribute("data-csrf")

    if (action === "block") {
        unblock_btn = createBlockUnblockBtn(id, "unblock");
        status_bar.append(unblock_btn);
    } else {
        add_friend_btn = createAddFriendBtn(id, csrf);
        block_btn = createBlockUnblockBtn(id, "block");
        status_bar.append(add_friend_btn, block_btn);
    };
}

////////////////////////////////////////////////////////////////////////////////
//                         CREATING HTML ELEMENTS                             //
////////////////////////////////////////////////////////////////////////////////

function createAddFriendBtn(id, csrf) {
    var btn = document.createElement("button");
    target_url = "/accounts/friend_request/"
    btn.innerHTML = "Add Friend";
    btn.className = "btn_requests"
    btn.id = "id_send_friend_request_btn"
    btn.setAttribute("onclick", `sendFriendRequest('${id}', '${csrf}')`); // this
    btn.setAttribute("data-next-url", "/accounts/cancel_friend_request/");
    return btn;
}

function createCancelFriendRequestBtn(id, csrf) {
    var btn = document.createElement("button");
    btn.innerHTML = "Invitation Sent";
    btn.className = "btn_requests";
    btn.id = "id_cancel_request_btn";
    btn.setAttribute("onclick", `cancelFriendRequest('${id}', '${csrf}')`);
    btn.setAttribute("data-next-url", "/accounts/friend_request/");
    return btn;
}

function createUnfriendBtn(id, csrf) {
    var btn = document.createElement("button")
    btn.innerHTML = "Unfriend";
    btn.id = "id_unfriend_btn";
    btn.className = "btn_requests";
    btn.setAttribute('onclick', `removeFriend('${id}', '${csrf}')`);
    return btn;
}

function createBlockUnblockBtn(id, type) {
    var btn = document.createElement("button");
    btn.innerHTML = capitalize(type)
    btn.className = "btn_requests"
    btn.setAttribute('onclick', `blockUnblock("${id}", "${type}")`)
    return btn
}

function createMessageBtn() {
    var dm_btn = document.createElement("button");
    dm_btn.innerHTML = "Message";
    dm_btn.className = "btn_requests";

    var anchor = document.createElement("a");
    anchor.href = "/chatapp";
    anchor.appendChild(dm_btn);

    return anchor;
}

////////////////////////////////////////////////////////////////////////////////
//                            HELPER FUNCTIONS                                //
////////////////////////////////////////////////////////////////////////////////

function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}