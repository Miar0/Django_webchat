const userId = document.getElementById('userId').value;
const roomId = document.getElementById('roomId').value;
let ws = new WebSocket(`ws:${window.location.host}/ws/chat/${roomId}`)

ws.onopen = () => {
    ws.send(JSON.stringify({
        'type': 'connected',
        'userId': userId
    }))
}
ws.onmessage = (data) => {
    let obj = JSON.parse(data.data);
    if (obj.type === 'connected') {
        document.querySelector('.message').innerHTML += `<b>Bot: </b><span>${obj.message.msg}</span>`
    } else if (obj.type === 'message') {
        let messageData = JSON.parse(obj.message)
        document.querySelector('.message').innerHTML += `<b>${messageData.username}</b><span>${messageData.text}</span>`
    }
}

document.getElementById('send-message').addEventListener('click', () => {
    if (document.getElementById('message').value !== "") {
        ws.send(JSON.stringify({
            'type': 'message',
            'text': document.getElementById('message').value,
            'userId': userId
        }))
    }
})