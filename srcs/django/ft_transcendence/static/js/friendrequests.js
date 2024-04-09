////////////////////////////////////////////////////////////////////////////////
//                           FRIEND SYSTEM                                    //
////////////////////////////////////////////////////////////////////////////////

function sendFriendRequest(id, target_url, csrf) {
    payload = {
        "csrfmiddlewaretoken": csrf,
        "receiver_user_id": id,
    }
    $.ajax({
        type: "POST",
        dataType: "json",
        url: target_url,
        timeout: 5000,
        data: payload,
        success: function(data) {
            if (data['response'] == "Friend request sent."){
                onFriendRequestSent(data)
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

function onFriendRequestSent(data) {
    // location.reload();
    var newButton = document.createElement("button");
    newButton.innerHTML = "Invitation Sent**";
    newButton.className = "btn_requests";
    newButton.id = "id_cancel_request_btn"

    var oldButton = document.getElementById("id_send_friend_request_btn");
    oldButton.parentNode.replaceChild(newButton, oldButton);
}

////////////////////////////////////////////////////////////////////////////////

// var cancelFriendRequestBtn = document.getElementById("id_cancel_request_btn")
// if (cancelFriendRequestBtn != null) {
//     cancelFriendRequestBtn.addEventListener("click", function(){
//         cancelFriendRequest("{{id}}", onFriendRequestCanceled);
//     })
// }

function cancelFriendRequest(id, target_url, csrf) {

    payload = {
        "csrfmiddlewaretoken": csrf,
        "receiver_user_id": id,
    }
    $.ajax({
        type: "POST",
        dataType: "json",
        url: target_url,
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
    })
}

function onFriendRequestCanceled() {
    location.reload();
}

////////////////////////////////////////////////////////////////////////////////

function triggerAcceptFriendRequest(friend_request_id) {
    acceptFriendRequest(friend_request_id, onFriendRequestAccepted)
}

var acceptFriendRequestBtn = document.getElementById("id_accept_request_btn")
if (acceptFriendRequestBtn != null) {
    acceptFriendRequestBtn.addEventListener("click", function(){
        acceptFriendRequest("{{user.id}}", onFriendRequestAccepted);
    })
}

function acceptFriendRequest(friend_request_id, uiUpdateFunction) {
    var url = "{% url 'accounts:friend_request_accept' friend_request_id=65464762465764 %}".replace(65464762465764, friend_request_id)
    $.ajax({
        type: "GET",
        dataType: "json",
        url: url,
        timaout: 5000,
        success: function(data) {
            if (data['response'] == "Friend request accepted") {

            }
            else if (data.response != null) {
                alert(data.response)
            }
        },
        error: function(data) {
            alert("Something went wrong: " + data)
        },
        complete: function(data) {
            uiUpdateFunction()
        },
    })
}

function onFriendRequestAccepted() {
    location.reload();
}

////////////////////////////////////////////////////////////////////////////////

function triggerDeclineFriendRequest(friend_request_id) {
    declineFriendRequest(friend_request_id, onFriendRequestDeclined)
}

function declineFriendRequest(friend_request_id, uiUpdateFunction) {
    var url = "{% url 'accounts:friend_request_decline' friend_request_id=65464762465764 %}".replace(65464762465764, friend_request_id)
    $.ajax({
        type: "GET",
        dataType: "json",
        url: url,
        timaout: 5000,
        success: function(data) {
            if (data['response'] == "Friend request declined") {
            }
            else if (data.response != null) {
                alert(data.response)
            }
        },
        error: function(data) {
            alert("Something went wrong: " + data)
        },
        complete: function(data) {
            uiUpdateFunction()
        },
    })
}

function onFriendRequestDeclined() {
    location.reload();
}

////////////////////////////////////////////////////////////////////////////////

var removeFriendBtn = document.getElementById("id_unfriend_btn")
if (removeFriendBtn != null) {
    removeFriendBtn.addEventListener("click", function(){
        removeFriend("{{id}}", onFriendRemoved);
    })
}

function removeFriend(id, uiUpdateFunction) {
    payload = {
        "csrfmiddlewaretoken": "{{csrf_token}}",
        "receiver_user_id": id,
    }
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "{% url 'accounts:remove_friend' %}",
        timeout: 5000,
        data: payload,
        success: function(data) {
            if (data['response'] == "Successfully removed that friend"){
            }
            else if (data['response'] != null) {
                alert(data['response']);
            }
        },
        error: function(data) {
            alert("Something went wrong." + data)
        },
        complete: function(data) {
            uiUpdateFunction()
        }
    })
}

function onFriendRemoved() {
    location.reload();
}

////////////////////////////////////////////////////////////////////////////////

function blockUnblock(id, action) {
    var url = "/accounts/blocking?user_id=738784&action=892893".replace(738784, id).replace(892893, action)
    $.ajax({
        type: "GET",
        dataType: "json",
        url: url,
        timaout: 5000,
        success: function(data) {
            console.log(data['response'], 'Success');
        },
        error: function(data) {
            // alert(data['response'], 'Error');
        },
        complete: function(data) {
            console.log(data['response'], 'Complete')
            location.reload()
        },
    })
}

