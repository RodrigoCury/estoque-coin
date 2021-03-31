completeToDo = (id) => {
    url = '/todo/complete/' + id
    fetch(url, {
        method: 'GET',
    })
}

delTodo = (id) => {

    let _li = $("#" + id).parent("li");

    console.log(_li)

    _li.addClass("remove").stop().delay(100).slideUp("fast", function () {

        _li.remove();

    });

    return false;

};


addTodo = (e) => {
    let code = (e.keyCode ? e.keyCode : e.which);

    if (code == 13) {
        e.preventDefault();
        let form = document.querySelector("#todo-form")
        let input = $('#id_activity')
        let url = '/todo/add'

        let v = input.val();

        let s = v.replace(/ +?/g, '');

        if (s == "") {

            return false;

        } else {

            const data = new URLSearchParams();
            for (const pair of new FormData(form)) {
                data.append(pair[0], pair[1]);
            }
            console.log(data)
            fetch(url, {
                method: 'post',
                body: data,
            })
                .then((r) => r.json())
                .then((r) => {
                    $(".tdl-content ul").append(`
                <li class='d-flex flex-row align-items-center justify-content-between mr-2'>
                    <label>
                    <input type='checkbox' onchange='completeToDo(${r.id})'>
                    <i></i>
                    <span>${v}</span>
                    </label>
                    <a id='todo${r.id}' href='#' onclick="deleteToDo(${r.id})" class='ti-trash'></a>
                </li>`);

                    input.val("")
                }).catch()

        }

    }
}


deleteToDo = (id) => {
    url = '/todo/delete/' + id
    fetch(url, {
        method: 'GET',
    })
        .then(delTodo("todo" + id))
        .catch(err => console.log(err))
}
