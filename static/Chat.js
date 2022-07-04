var socket;
window.onload = function() {
    var input = document.getElementById("text");
    input.addEventListener("keyup", function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        document.getElementById("send").click();
    }
    });
    if(document.getElementById("newmsg")){
        document.getElementById("No_msg").style.display="none";
    }
    socket.emit('users');
    socket.on('usersData', function (data) {
    $('#users').remove();
    const users = document.createElement("div");
    users.setAttribute("id","users")
    document.getElementById("leftVerDiv").appendChild(users);
    for(let i= 0 ; i< data.len;i++){
    var div = document.createElement("div");
    var text = document.createTextNode(data.data[i][0]);
    div.appendChild(text)
    // image
    var img = document.createElement("img");
    img.src = data.data[i][1];
    document.getElementById("users").appendChild(div);
    document.getElementById("users").appendChild(img);
    div.setAttribute("id", data.data[i][0]);
    document.getElementById("users").appendChild(document.createElement("br"));
    }
    });
};
$(document).ready(function(){
    $( "#horizLeft" ).mouseenter(function() {
        $("#horizLeft").css({top: 10, position:'absolute'});
    });
    $( "#leftVerDiv" ).mouseenter(function() {
            $("#horizLeft").css({top: 10,left:100, position:'absolute'});
            $('#horizLeft').css({'transform' : 'rotate('+ 270 +'deg)'});
            $('#ChatImage').css({top: 100,left:70, position:'absolute'});
            $('#usernameLSide').css({top: 118,left:135, position:'absolute'});
            document.getElementById('usernameLSide').style.display= "block";
        })
        .mouseleave(function() {
            $("#horizLeft").css({top: 300,left:0, position:'absolute'});
            $('#horizLeft').css({'transform' : 'rotate('+ 180 +'deg)'});
            $('#ChatImage').css({top: 0,left:0, position:'absolute'});
            document.getElementById('usernameLSide').style.display= "none";
        });

        socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
        socket.on('connect', function() {
        socket.emit('join', {});
        socket.emit('users');
        });
        socket.on('newUser', function (data) {
        var div = document.createElement("div");
        var text = document.createTextNode(data.username);
        div.appendChild(text)
        // image
        var img = document.createElement("img");
        img.src = data.image;
        document.getElementById("users").appendChild(div);
        document.getElementById("users").appendChild(img);
        div.setAttribute("id", data.username);
        document.getElementById("users").appendChild(document.createElement("br"));
    });
        socket.on('status', function (data) {
        $('#hold_chat').scrollTop($('#hold_chat')[0].scrollHeight);
        var div = document.createElement("div");
        var br = document.createElement("br");
        div.className = "newuser";
        div.style.background = "gray";
        div.style.color = "white";
        div.innerHTML = data.msg;
        document.getElementById("hold_chat").appendChild(div);
        document.getElementById("hold_chat").appendChild(br);
    });

        socket.on('message', function(data) {  
        $('#hold_chat').scrollTop($('#hold_chat')[0].scrollHeight);
        document.getElementById("No_msg").style.display = "none";
        var div = document.createElement("div");
        var br = document.createElement("br");
        div.className = "newmsg";
        div.style.background = "green";
        div.style.color = "white";
        div.innerHTML = data.msg;
        document.getElementById("hold_chat").appendChild(div);
        document.getElementById("hold_chat").appendChild(br);
            //$('#chat').val($('#chat').val() + data.msg + '\n');
            //$('#chat').scrollTop($('#chat')[0].scrollHeight);
        });
        $('#send').click(function(e) {
                text_spaces = $('#text').val().replace(/\s+/g, '')
                if(text_spaces != ""){
                text = $('#text').val().trim();
                socket.emit('text', {msg: text});
                document.getElementById('text').value = '';
                }
        });
});
function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();
        // go back to the login page
        window.location.href = window.location.origin;
    });
}