window.onload = function() {
    var beginDiv = document.querySelector('.begin');
    beginDiv.style.display = 'block';

    document.getElementById('start-button').style.display = 'none';

    var gameDiv = document.querySelector('.game');
    gameDiv.style.display = 'none';

    generateOpening();

    const sessionId = localStorage.getItem('session_id');
    console.log(sessionId);
}

function displayTextByLetter(text, container, interval, callback) {
    let i = 0;
    let lastTime = Date.now();
    function nextLetter() {
        requestAnimationFrame(() => {
            let currentTime = Date.now();
            if (currentTime - lastTime >= interval) {
                if (i < text.length) {
                    container.textContent += text.charAt(i);
                    i++;
                    lastTime = currentTime;
                } else {
                    if (callback && typeof callback === 'function') {
                        callback();
                    }
                    return;
                }
            }
            nextLetter();
        });
    }
    nextLetter();
}

function generateOpening() {
    // 获取要显示文本的容器
    const textContainer = document.getElementById('opening');
    const text = "欢迎来到《人生重启模拟器》，一个简约的世界，等待你来编织命运。在这里，每个选择都是重生的机会，每个对话都能开辟生活的新路径。用你的智慧探索无数可能，用你的决定定义未来。现在，深呼吸，按下“开始游戏”，让我们一起探索人生的无限可能吧！";
    displayTextByLetter(text, textContainer, 50, function() { // 50ms per word
        // 文本显示完毕后，显示开始按钮
        document.getElementById('start-button').style.display = 'inline';
      });
}

function beginGame() {
    var beginDiv = document.querySelector('.begin');
    beginDiv.style.display = 'none';

    var gameDiv = document.querySelector('.game');
    gameDiv.style.display = 'block';

    getBackground()
}

function initPlayer() {
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
            if (data && data["性别"]) {
                // 插入数据到HTML中
                document.getElementById('gender').textContent = data["性别"];
                document.getElementById('city').textContent = data["城市"];
                document.getElementById('age').textContent = data["年龄"];
                document.getElementById('personality').textContent = data["性格"];
                document.getElementById('charm').textContent = data["属性"]["魅力"];
                document.getElementById('intelligence').textContent = data["属性"]["智力"];
                document.getElementById('health').textContent = data["属性"]["健康"];
                document.getElementById('wealth').textContent = data["属性"]["富裕"];
                document.getElementById('happiness').textContent = data["属性"]["幸福度"];

                // 显示卡片
                document.querySelector('.card').style.display = 'flex';
            }
        })
        .catch(error => {
            console.error('Error fetching the init API:', error);
        });
}

async function getBackground() {
    initPlayer()

    let resultParagraph = document.getElementById("markdownArea");
    var md = window.markdownit();
    // disable buttons
    const background_btn = document.querySelector('#backgroundButton');
    const event_btn = document.querySelector('#eventButton');
    background_btn.disabled = true;
    event_btn.disabled = true;

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
        cache_string += text
        resultParagraph.innerHTML = md.render(cache_string);
        let container = document.querySelector('.markdown-container');
        container.scrollTop = container.scrollHeight;
    }

    background_btn.disabled = false;
    event_btn.disabled = false;
}

async function getEvent() {
    let resultParagraph = document.getElementById("markdownArea");
    var md = window.markdownit();
    var cache_string = "";
    const sessionId = localStorage.getItem('session_id');

    const response = await fetch('/life-reload/event/', {
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
        cache_string += text
        resultParagraph.innerHTML = md.render(cache_string);
        let container = document.querySelector('.markdown-container');
        container.scrollTop = container.scrollHeight
    }
}

async function getLifeEvent() {
    // disable buttons
    const background_btn = document.querySelector('#backgroundButton');
    const event_btn = document.querySelector('#eventButton');
    background_btn.disabled = true;
    event_btn.disabled = true;

    const flag = await isAlive();
    if (!flag) {
        var eventButton = document.getElementById('eventButton');
        var backgrounButton = document.getElementById('backgroundButton');
        eventButton.disabled = true;
        backgrounButton.disabled = false;
        return ;
    }

    updatePerson()
    await getEvent()
    const response = fetch('/life-reload/parsed_event/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            session_id: sessionId
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        background_btn.disabled = false;
        event_btn.disabled = false;
        return response.json();
    })
    .then(data => {
        let eventValue = data.event;
        let optionValue = data.option
        let resultParagraph = document.getElementById("markdownArea");
        var md = window.markdownit();
        resultParagraph.innerHTML = md.render(eventValue);
        generateButtons(optionValue);
        background_btn.disabled = false;
        event_btn.disabled = false;
    })
    .catch(error => {
        console.log('There was a problem with the fetch operation:', error.message);
        background_btn.disabled = false;
        event_btn.disabled = false;
    });
}

async function evaluate(optionNumber) {
    // disable buttons
    const background_btn = document.querySelector('#backgroundButton');
    const event_btn = document.querySelector('#eventButton');
    background_btn.disabled = true;
    event_btn.disabled = true;

    let resultParagraph = document.getElementById("markdownArea");
    var md = window.markdownit();
    var cache_string = "";
    const sessionId = localStorage.getItem('session_id');

    const response = await fetch('/life-reload/evaluation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            session_id: sessionId,
            selection: optionNumber
        })
    });
    const reader = response.body.getReader();

    while (true) {
        const { done, value } = await reader.read();
        if (done) {
            break;
        }
        const text = new TextDecoder().decode(value);
        cache_string += text
        resultParagraph.innerHTML = md.render(cache_string);
        let container = document.querySelector('.markdown-container');
        container.scrollTop = container.scrollHeight
    }

    background_btn.disabled = false;
    event_btn.disabled = false;
}

function generateButtons(inputStr) {
    let parent_container = document.getElementById("markdownArea");
    let newDiv = document.createElement('div');
    newDiv.id = 'option-container';
    parent_container.appendChild(newDiv)
    const container = document.getElementById("option-container");
    let markdown_container = document.querySelector('.markdown-container');

    // 使用正则表达式匹配选项
    const regex = /(\d+\.)[^0-9]*(?=\d+\.|$)/g;
    const matches = inputStr.match(regex);

    if (matches) {
        matches.forEach((option, index) => {
            const btn = document.createElement("button");
            btn.innerHTML = strongText(option.trim());
            btn.onclick = () => evaluate(index + 1);
            container.appendChild(btn);
            markdown_container.scrollTop = markdown_container.scrollHeight
        });
    }
}

async function isAlive() {
    const sessionId = localStorage.getItem('session_id');

    const response = await fetch('/life-reload/is_alive/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            session_id: sessionId
        })
    });

    if (response.ok) {
        const data = await response.json();
        if (!data) {
            await generateEpitaph()
        }
        return data
    } else {
        console.error("Error fetching data:", response.statusText);
    }

}

async function generateEpitaph() {
    var cache_string = "";
    const sessionId = localStorage.getItem('session_id');
    let resultParagraph = document.getElementById("markdownArea");
    var md = window.markdownit();

    const response = await fetch('/life-reload/epitaph/', {
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
        cache_string += text
        resultParagraph.innerHTML = md.render(cache_string);
        let container = document.querySelector('.markdown-container');
        container.scrollTop = container.scrollHeight;
    }
}

async function updatePerson() {
    const response = fetch('/life-reload/get_person/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            session_id: sessionId
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // 以"性别"字段为例，检查是否存在，你可以根据需要增加更多的检查条件
        if (data && data["性别"]) {
            // 插入数据到HTML中
            document.getElementById('gender').textContent = data["性别"];
            document.getElementById('city').textContent = data["城市"];
            document.getElementById('age').textContent = data["年龄"];
            document.getElementById('personality').textContent = data["性格"];
            document.getElementById('charm').textContent = data["属性"]["魅力"];
            document.getElementById('intelligence').textContent = data["属性"]["智力"];
            document.getElementById('health').textContent = data["属性"]["健康"];
            document.getElementById('wealth').textContent = data["属性"]["富裕"];
            document.getElementById('happiness').textContent = data["属性"]["幸福度"];

            // 显示卡片
            document.querySelector('.card').style.display = 'flex';
        }
    })
    .catch(error => {
        console.log('There was a problem with the fetch operation:', error.message);
    });
}

function strongText(text) {
    return text.replace(/\*\*(.*?)\*\*/g, '<span id="bold-text">$1</span>');
}
