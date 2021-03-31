(function ($) {
    "use strict"


    //todo list
    $(".tdl-new").on('keypress', function (e) {

        var code = (e.keyCode ? e.keyCode : e.which);

        if (code == 13) {

            var v = $(this).val();

            var s = v.replace(/ +?/g, '');

            if (s == "") {

                return false;

            } else {

                $(".tdl-content ul").append("<li><label><input type='checkbox'><i></i><span>" + v + "</span><a href='#' class='ti-trash'></a></label></li>");

                $(this).val("");

            }

        }

    });






    // for dynamically created a tags

    $(".tdl-content").on('click', "a", function () {

        var _li = $(this).parent().parent("li");

        _li.addClass("remove").stop().delay(100).slideUp("fast", function () {

            _li.remove();

        });

        return false;

    });








})(jQuery);



function slimScroll() {
    "use strict"

    $('#todo_list').slimscroll({
        position: "right",
        size: "5px",
        height: "250px",
        color: "transparent"
    });

    $('#activity').slimscroll({
        position: "right",
        size: "5px",
        height: "390px",
        color: "transparent"
    });





};

slimScroll()