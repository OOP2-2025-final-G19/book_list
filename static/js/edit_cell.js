function editCell(td, bookId, field) {
    const currentValue = td.innerText;

    // テキストとして入力を受け取る
    const input = document.createElement("input");
    input.type = "text";
    input.value = currentValue;

    td.innerHTML = "";
    td.appendChild(input);
    input.focus();

    input.onblur = () => {
        const value = input.value.trim();

        // 空欄チェック
        if (value === "") {
            alert("空欄にはできません");
            td.innerText = currentValue;
            return;
        }

        // 評価チェック
        if (field === "review") {
            const num = Number(value);
            if (!Number.isInteger(num) || num < 1 || num > 5) {
                alert("評価は1〜5の整数で入力してください");
                td.innerText = currentValue;
                return;
            }
        }

        fetch(`/books/update/${bookId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                field: field,
                value: value
            })
        }).then(res => {
            if (!res.ok) {
                alert("更新に失敗しました");
                td.innerText = currentValue;
                return;
            }
            td.innerText = value;
        });
    };
}
