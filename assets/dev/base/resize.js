var resize = function(){
    $('.row.resize').each(function(_i, row){
        cols = $(row).children('div');
        cols.each(function(_j, col){
            $(col).children('.well').outerHeight('auto', true);
        });
        colHeights = cols.map(function(_j, col){
            return Math.max.apply(null, $(col).children('.well').map(function(_i, c){
                return $(c).innerHeight();
            }));
        });
        localMaxHeight = Math.max.apply(null, colHeights);
        cols.each(function(_j, col){
            $(col).children('.well').innerHeight(localMaxHeight);
        });
    });
}
resize();
$(window).resize(resize);