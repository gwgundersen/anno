var ANNO = {};


ANNO.renderMath = function () {
    var math = document.getElementsByClassName('math'),
        el, i;
    for (i = 0; i < math.length; i++) {
        el = math[i];
        if (el.classList[1] === 'inline') {
            katex.render(el.textContent, el);
        } else {
            katex.render(el.textContent, el, {
                displayMode: true
            });
        }
    }
};


ANNO.escapeHTML = function (string) {
    var entityMap = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': '&quot;',
        "'": '&#39;',
        "/": '&#x2F;'
    };
    return String(string).replace(/[&<>"'\/]/g, function (s) {
        return entityMap[s];
    });
};


/* Credit: https://davidwalsh.name/javascript-debounce-function.
 */
ANNO.debounce = function (func, wait, immediate) {
    var timeout;
    return function () {
        var context = this,
            args = arguments,
            later, callNow;
        later = function () {
            timeout = null;
            if (!immediate) {
                func.apply(context, args);
            }
        };
        callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) {
            func.apply(context, args);
        }
    };
};


ANNO.ajax = function (url, callback, method, data) {
    var async = true;
    var x = new XMLHttpRequest();
    x.open(method, url, async);
    x.onreadystatechange = function () {
        if (x.readyState === 4) {
            callback(x.responseText)
        }
    };
    x.send(data)
};


document.addEventListener('DOMContentLoaded', function () {

    watch_edits();
    handle_images();

    function watch_edits() {
        var $text = $('textarea#edit-field'),
            $preview = $('#edit-preview');

        if ($text.length === 0) {
            return;
        }
        refreshPreview();

        $text.change(refreshPreview);
        $text.keyup(ANNO.debounce(refreshPreview, 1000));

        function refreshPreview() {
            var success,
                data;
            success = function(data) {
                $preview.html(data);
                ANNO.renderMath();
            };
            data = new FormData();
            data.append('note_text', $text.val());
            ANNO.ajax('/preview', success, 'POST', data);
        }
    }

    function handle_images() {
        $('.image-uploader button').click(function (evt) {
            evt.preventDefault();
            var $uploader = $(evt.target).parent(),
                $input = $uploader.find('input#image-upload-btn');

            $(':file').unbind('change');
            $('#uploaded-image-tag').empty();
            $input.trigger('click');

            $(':file').change(function () {
                var file = $input[0].files[0],
                    formData;
                formData = new FormData();
                formData.append('file', file);
                $.ajax({
                    url: '/image',
                    type: 'POST',
                    data: formData,
                    cache: false,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        addUploadedImageTag(data);
                    }
                }, 'json');
            });
        });
    }

    function addUploadedImageTag(imgTag) {
        var elem = document.getElementById('uploaded-image-tag');
        elem.innerHTML = ANNO.escapeHTML(imgTag);
        elem.style.display = 'block';
    }
});
