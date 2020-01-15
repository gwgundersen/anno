var ANNO = {};


ANNO.renderMath = function () {
    var math = document.getElementsByClassName('math'),
        el, i;
    for (i = 0; i < math.length; i++) {
        el = math[i];
        if (el.classList[1] === 'inline') {
            katex.render(el.textContent, el, {
                throwOnError: false
            });
        } else {
            katex.render(el.textContent, el, {
                displayMode: true,
                throwOnError: false
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


ANNO.watchEdits = function () {
    var text = document.getElementById('edit-field'),
        preview = document.getElementById('edit-preview');

    refreshPreview();
    text.addEventListener('keyup', debounce(refreshPreview, 500));

    /* Credit: https://davidwalsh.name/javascript-debounce-function.
     */
    function debounce(func, wait) {
        var timeout;
        return function() {
            var context = this,
                args = arguments,
                later;
            later = function() {
                timeout = null;
                func.apply(context, args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (!timeout) {
                func.apply(context, args);
            }
        };
    }

    function refreshPreview() {
        var success,
            data;
        success = function (data) {
            preview.innerHTML = data;
            ANNO.renderMath();
        };
        data = new FormData();
        if (text) {
            data.append('note_text', text.value);
            ANNO.ajax('/preview', success, 'POST', data);
        }
    }
};


ANNO.addUploadedImageTag = function (imgTag) {
    var elem = document.getElementById('uploaded-image-tag');
    elem.innerHTML = ANNO.escapeHTML(imgTag);
    elem.style.display = 'block';
};


ANNO.handleImages = function () {
    var btn = document.querySelector('#image-uploader button');
    btn.addEventListener('click', uploadImage);

    function uploadImage(evt) {
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
                    ANNO.addUploadedImageTag(data);
                }
            }, 'json');
        });
    }
};


document.addEventListener('DOMContentLoaded', function () {
    ANNO.watchEdits();
    ANNO.handleImages();
});
