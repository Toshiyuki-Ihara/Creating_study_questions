function setLoading(isLoading, message = "") {
    const loadingDiv = document.getElementById("loading");
    const loadingText = document.getElementById("loadingText");
    if (isLoading) {
        loadingText.textContent = message;
        loadingDiv.style.display = "block";
    } else {
        loadingDiv.style.display = "none";
    }
    }

    async function startProcessing() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput.files[0];
    const type = document.getElementById('quizType').value;

    if (!file) {
        alert("画像またはPDFを選択してください。");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("type", type);

    setLoading(true, "アップロード中...");

    const res = await fetch("/start_job", {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    const taskId = data.task_id;

    pollStatus(taskId, type);
    }

    async function pollStatus(taskId, type) {
    const statusMessage = {
        queued: "待機中です...",
        extracting: "画像からテキストを抽出中...",
        fixing: "テキストを整形中...",
        splitting: "文を分割中...",
        generating: "問題を生成中...",
        done: "完了しました！",
        error: "エラーが発生しました。"
    };

    const interval = setInterval(async () => {
        const res = await fetch(`/status/${taskId}`);
        const data = await res.json();

        const status = data.status;
        setLoading(true, statusMessage[status] || "処理中...");

        if (status === "done") {
            clearInterval(interval);
            setLoading(true, "結果を取得中...");
            const resultRes = await fetch(`/result/${taskId}`);
            const resultData = await resultRes.json();
            setLoading(false);
            showQuiz(resultData.quizzes, type);
        }

        if (status === "error") {
            clearInterval(interval);
            alert("エラーが発生しました。サーバーログを確認してください。");
            setLoading(false);
        }

        }, 2000);
    }

    function showQuiz(quizzes, type) {
        const container = document.getElementById('quizContainer');
        container.innerHTML = "";

        quizzes.forEach((quiz, i) => {
        const div = document.createElement('div');
        div.className = "question";

        const qText = document.createElement('p');
        qText.textContent = `Q${i + 1}: ${quiz.question}`;
        div.appendChild(qText);

        const resultText = document.createElement('p');
        resultText.className = "result";

        if (type === "choice") {
            const choicesDiv = document.createElement('div');
            choicesDiv.className = "choices";

            quiz.choices.forEach((choice, j) => {
                const btn = document.createElement('button');
                btn.textContent = `${String.fromCharCode(65 + j)}. ${choice}`;
                btn.onclick = () => {
                    if (choice === quiz.answer) {
                        resultText.textContent = "✅ 正解!";
                        resultText.style.color = "green";
                    } else {
                        resultText.textContent = `❌ 不正解... 正解は: ${quiz.answer}`;
                        resultText.style.color = "red";
                    }
                };
                    choicesDiv.appendChild(btn);
            });
            div.appendChild(choicesDiv);
        } else if (type === "writing") {
            const input = document.createElement('input');
            input.type = "text";
            input.placeholder = "ここに答えを入力";

            const checkBtn = document.createElement('button');
            checkBtn.textContent = "解答を確認";
            checkBtn.onclick = () => {
            const userAns = input.value.trim();
            if (userAns === quiz.answer) {
                resultText.textContent = "✅ 正解!";
                resultText.style.color = "green";
            } else {
                resultText.textContent = `❌ 不正解... 正解は: ${quiz.answer}`;
                resultText.style.color = "red";
            }
            };

            div.appendChild(input);
            div.appendChild(checkBtn);
        }
            div.appendChild(resultText);
            container.appendChild(div);
    });
    }
