var Base = (function () {
    function showDiv(el) {
        el.style.display = 'block';
        el.style.visibility = 'visible';
    }

    function hideDiv(el) {
        el.style.display = 'none';
        el.style.visibility = 'hidden';
    }

    function getStyle(el, name) {
        var style;
        if (typeof el.currentStyle != 'undefined'){
            style = el.currentStyle;
        }
        else {
            style = document.defaultView.getComputedStyle(el, null);
        }
        return  style[name];
    }

    function toggleDiv(divId) {
        var el = document.getElementById(divId);
        if (getStyle(el, 'display') == 'none') {
            showDiv(el);
        } else {
            hideDiv(el);
        }
    }

    return {
        toggleDiv: toggleDiv
    };
}());
