async function getBackground() {
    let resultParagraph = document.getElementById("markdownArea");
    var md = window.markdownit();
    var cache_string = "";
    const sessionId = localStorage.getItem('session_id');

    const response = await fetch('/life-reload/begin/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            session_id: sessionId
        })
    });
    const reader = response.body.getReader();

    while (true) {
        const { done, value } = await reader.read();
        if (done) {
            break;
        }
        const text = new TextDecoder().decode(value);
        // TODO need to be commented when launching this project
        // console.log(text)
        cache_string += text
        resultParagraph.innerHTML = md.render(cache_string);
    }
}

window.onload = function() {
    const sessionId = localStorage.getItem('session_id');
    fetch('/life-reload/init/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            session_id: sessionId
        })
    })
        .then(response => response.json())
        .then(data => {
            // 以"性别"字段为例，检查是否存在，你可以根据需要增加更多的检查条件
            if (data && data["性别"]) {
                // 插入数据到HTML中
                document.getElementById('gender').textContent += data["性别"];
                document.getElementById('city').textContent += data["城市"];
                document.getElementById('age').textContent += data["年龄"];
                document.getElementById('personality').textContent += data["性格"];
                document.getElementById('charm').textContent += data["属性"]["魅力"];
                document.getElementById('intelligence').textContent += data["属性"]["智力"];
                document.getElementById('health').textContent += data["属性"]["健康"];
                document.getElementById('wealth').textContent += data["属性"]["富裕"];
                document.getElementById('happiness').textContent += data["属性"]["幸福度"];

                // 显示卡片
                document.querySelector('.card').style.display = 'flex';
            }
        })
        .catch(error => {
            console.error('Error fetching the init API:', error);
        });
}
