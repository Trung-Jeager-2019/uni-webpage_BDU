var Admin = (function () {
    function postJSON(url, token, data, callback) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.setRequestHeader('X-CSRF-Token', token);
        xhr.onload = callback;
        xhr.send(JSON.stringify(data));
    }

    function empty(id) {
        document.getElementById(id).innerHTML = '';
    }

    function prepend(id, text) {
        var old = document.getElementById(id).innerHTML;
        document.getElementById(id).innerHTML = text + old;
    }

    function showAddExaminee() {
        prepend('addexaminee-names', this.responseText);
    }

    function addExaminee() {
        var data = {};
        data.fullname = document.getElementById('addexaminee').value;
        data.exam_id = document.getElementById('selectexam').value;
        if (document.getElementById('addexaminee-names').innerHTML) {
            data.button = true;
        }
        postJSON('/users/addexaminee', csrftoken, data, showAddExaminee);
    }

    function showGetScore() {
        document.getElementById('getscore-scores').innerHTML = this.responseText;
    }

    function getExamScore() {
        var data = {};
        data.getscore = document.getElementById('getexamscore').value;
        postJSON('/users/examscore', csrftoken, data, showGetScore);
    }

    function showCheckWrite() {
        document.getElementById('checkwrite').innerHTML = this.responseText;
    }

    function checkWrite() {
        postJSON('/users/checkwriting', csrftoken, '', showCheckWrite);
    }

    function updateGetScore() {
        var text = document.getElementById('getexamscore').innerHTML;
        if (text.indexOf(this.responseText) === -1)
            prepend('getexamscore', '<option>' + this.responseText + '</option>');
    }

    function sendWriteScore(formId) {
        var form = document.getElementById(formId),
            data = {},
            i = 0,
            len = form.length;

        for (i; i < len; ++i) {
            var input = form[i];
            if (input.type === 'text') {
                data[input.name] = input.value;
            }
        }
        postJSON('/users/examwriting', csrftoken, data, updateGetScore);
        document.getElementById(formId).className = 'slide-up';
    }

    return {
        empty: empty,
        addExaminee: addExaminee,
        getExamScore: getExamScore,
        checkWrite: checkWrite,
        sendWriteScore: sendWriteScore
    };
}());
