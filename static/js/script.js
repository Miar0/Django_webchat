let ws = new WebSocket(`ws:${window.location.host}/ws/chat`)
const userId = document.getElementById('userId').value;

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
    }
}