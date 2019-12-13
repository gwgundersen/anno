$(function() {

    watch_edits();
    handle_images();

    function watch_edits() {
        var $text = $('textarea#edit-field'),
            $preview = $('#edit-preview');

        if ($text.length == 0) {
            return;
        }
        refresh_preview();

        $text.change(refresh_preview);
        $text.keyup(debounce(refresh_preview, 1000));

        function refresh_preview() {
            $.ajax({
                url: '/preview',
                type: 'POST',
                data: {
                    note_text: $text.val()
                },
                success: function(data) {
                    $preview.html(data);
                    MathJax.Hub.Queue(['Typeset', MathJax.Hub]);
                }
            });
        }
    }

    /* Credit: https://davidwalsh.name/javascript-debounce-function.
     */
    function debounce(func, wait, immediate) {
        var timeout;
        return function() {
            var context = this, args = arguments;
            var later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    }

    function handle_images() {
        $('.image-uploader button').click(function(evt) {
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
                        add_uploaded_image_tag(data);
                    }
                }, 'json');
            });
        });
    }

    function add_uploaded_image_tag(imgTag) {
        $('#uploaded-image-tag').show().append(escape_html(imgTag));
    }

    function escape_html(string) {
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
    }
});
