function setupDescription() {
    $('.book .info .description').each(function() {
        if($(this).height() > 100) {
            $(this).addClass('scrollshadow');
            $(this).click(function() {
                $(this).toggleClass('scrollshadow');
            });
        }
   });
}

$(function() {
   setupDescription();
});