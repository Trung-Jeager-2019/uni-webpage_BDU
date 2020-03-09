var Exam = (function () {
    function postJSON(url, token, data) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        xhr.setRequestHeader('X-CSRF-Token', token);
        xhr.send(JSON.stringify(data));
    }

    function updateResults() {
        var form = document.forms[0],
            data = {},
            i = 0,
            len = form.length,
            token = document.getElementById('token').value;

        for (i; i < len; ++i) {
            var input = form[i];
            if (input.type === 'radio' && input.checked) {
                data[input.name] = input.value;
            }
            if (input.type === 'textarea') {
                data[input.name] = input.value;
            }
        }
        postJSON('/users/exam/update_results', token, data);
    }

    function counter(time_limit) {
        var form = document.forms[0],
            countdown = document.getElementById('countdown'),
            target_date = new Date().getTime() + time_limit * 1000 * 60;

        setInterval(function () {
            var current_date, seconds_left, hours, minutes;

            current_date = new Date().getTime();
            if (current_date > target_date) {
                countdown.style.display = 'none';
                form.submit();
            }
            seconds_left = (target_date - current_date) / 1000;
            if (seconds_left < 900) {
                countdown.className = 'deadline';
            }
            hours = parseInt(seconds_left / 3600, 10);
            seconds_left = seconds_left % 3600;
            minutes = ('0' + parseInt(seconds_left / 60, 10)).slice(-2);
            countdown.innerHTML = 'Time remaining: ' + hours + ':' + minutes;
        }, 1000 * 30);
    }

    function start(time_limit) {
        var audio = document.getElementById('listening'),
            exam = document.getElementById('exam-body'),
            slide = document.querySelector('.slide');

        exam.style.display = 'block';
        slide.classList.add('slide-up');
        time_limit = (time_limit === undefined) ? 180 : time_limit,
        counter(time_limit);
        if (audio) {
            audio.play();
        }
        setInterval(function () {
            updateResults();
        }, 1000 * 60);
    }

    function overlay() {
        el = document.getElementById('overlay');
        el.style.visibility = (el.style.visibility == 'visible') ? 'hidden' : 'visible';
    }

    return {
        start: start,
        overlay: overlay
    };
}());
