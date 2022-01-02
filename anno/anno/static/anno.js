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
    x.send(data);
};


ANNO.watchEdits = function () {
    var text = document.getElementById('edit-field'),
        preview = document.getElementById('edit-preview'),
        saveMsgTimeout;

    refreshPreview();
    autosave();
    if (text) {
        text.addEventListener('keyup', debounce(refreshPreview, 500));
    }
    window.addEventListener('keydown', function(event) {
        if (event.ctrlKey || event.metaKey) {
            var key = String.fromCharCode(event.which).toLowerCase();
            if (key === 's') {
                event.preventDefault();
                save(false);
            }
        }
    });

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

    function success(data) {
        preview.innerHTML = data;
        ANNO.renderMath();
    }

    function refreshPreview() {
        var data;
        data = new FormData();
        if (text) {
            data.append('note_text', text.value);
            ANNO.ajax('/preview', success, 'POST', data);
        }
    }

    function save(auto) {
        var data = new FormData(),
            elem,
            url;

        if (text) {
            data.append('note_text', text.value);
            url = window.location.pathname.replace('/edit', '/save');
            ANNO.ajax(url, function(d) {
                var i,
                    forms,
                    new_action,
                    new_url;

                d = JSON.parse(d);
                if (d['success']) {
                    success(d['data']);
                    forms = document.getElementsByTagName('form');
                    // Ensure the form action properties are in sync. See:
                    // https://github.com/gwgundersen/anno/issues/19
                    for (i = 0; i < forms.length; i++) {
                        new_action = forms[i].action.replace(
                            d['old_url'],
                            d['new_url']
                        );
                        forms[i].action = new_action;
                    }
                    new_url = '/' + d['new_url'] + '/edit';
                    // Notice that above, the AJAX request is built using the
                    // current URL. I know, this is fantastic state-handling.
                    // So we need to update the URL.
                    window.history.replaceState({}, '', new_url);
                    saveMsgTimeout = setTimeout(function() {
                        elem.innerHTML = '';
                    }, 7000);
                } else {
                    clearTimeout(saveMsgTimeout);
                }
                elem = document.getElementById('flashes');
                if (d['success'] && auto) {
                    elem.innerHTML = 'Auto-saved.';
                } else {
                    elem.innerHTML = d['message'];
                }
            }, 'POST', data);
        }
    }

    function autosave() {
        // Save every 120 seconds:
        // https://github.com/gwgundersen/anno/issues/16
        var SAVE_EVERY = 120000;
        window.setInterval(function() {
            save(true);
        }, SAVE_EVERY);
    }
};


ANNO.addUploadedImageTag = function (imgTag) {
    var elem = document.getElementById('uploaded-image-tag');
    elem.innerHTML = ANNO.escapeHTML(imgTag);
    elem.style.display = 'block';
};


ANNO.handleImages = function () {
    var btn = document.querySelector('#image-uploader button');
    if (btn) {
        btn.addEventListener('click', uploadImage);
    }

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
    try {
        ANNO.watchEdits();
    } catch (e) {}
    try {
        ANNO.handleImages();
    } catch (e) {}
});
