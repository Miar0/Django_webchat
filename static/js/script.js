userId = document.getElementById('userId').value;
roomId = document.getElementById('roomId').value;
ws?.close()
ws = new WebSocket(`ws:${window.location.host}/ws/chat/${roomId}`)

ws.onopen = () => {
    ws.send(JSON.stringify({
        'type': 'connected',
        'userId': userId
    }))
}
ws.onmessage = (data) => {
    let obj = JSON.parse(data.data);
    if (obj.type === 'connected') {
        alertify.success(obj.message.msg)
    } else if (obj.type === 'message') {
        let messageData = JSON.parse(obj.message)
        if (messageData.userId === userId) {
            document.querySelector('.message').innerHTML += `<p class='mb-2 own'><span>${messageData.text}</span></p>`
        } else {
        let avatar = document.getElementById('avatar').src
        document.querySelector('.message').innerHTML += `
        <p class="mb-2 d-flex">
            <img src="${avatar}" class="rounded-circle me-2" width="50">
            <span>
                <b>${messageData.username}</b><br>
                ${messageData.text}
            </span>
        </p>`
        }
    }
    document.querySelector('.message').scrollTo(0, document.querySelector('.message').scrollHeight)
}

document.getElementById('send-message').addEventListener('click', () => {
    sendMsg()
})

document.getElementById('message').addEventListener('keypress', (event) => {
    if (event.keyCode === 13) {
        sendMsg()
    }
})

function sendMsg() {
if (document.getElementById('message').value !== "") {
        ws.send(JSON.stringify({
            'type': 'message',
            'text': document.getElementById('message').value,
            'userId': userId
        }))
        document.getElementById('message').value = ''
    }
}