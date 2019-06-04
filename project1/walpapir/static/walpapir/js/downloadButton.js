(function($){
    $(function() {
        $('.downloadButton a').on('click', function(e){

            var hrefPath = $(this).attr('href');
            var fileName = $(this).attr('href').replace(/\\/g,'/').replace( /.*\//, '' );

            $target = $(e.target);
            $target.attr({
                download: fileName,
                href: hrefPath
            });

        });
    });
})(jQuery);
