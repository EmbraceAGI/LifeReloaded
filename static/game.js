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
        let container = document.querySelector('.markdown-container');
        container.scrollTop = container.scrollHeight;
    }
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
    await isAlive()
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
        return response.json();
    })
    .then(data => {
        let eventValue = data.event;
        let optionValue = data.option
        let resultParagraph = document.getElementById("markdownArea");
        var md = window.markdownit();
        resultParagraph.innerHTML = md.render(eventValue);
        generateButtons(optionValue);
    })
    .catch(error => {
        console.log('There was a problem with the fetch operation:', error.message);
    });
}

async function evaluate(optionNumber) {
    console.log("Selected option:", optionNumber);
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
            btn.innerText = option.trim();
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
        console.log(data)
        if (!data) {
            alert("你死了");
        }
    } else {
        console.error("Error fetching data:", response.statusText);
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
