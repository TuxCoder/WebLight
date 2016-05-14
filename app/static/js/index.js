
var strict;

index={};
index.Init = function () {
    $('a').on('click',function () {
        $.get($(this).attr('href'));
        return false;
    });

    $('form').ajaxForm();
};