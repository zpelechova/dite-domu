//Author: Jan Matoušek
//Contact: matousek.vr@gmail.com
//License: GPL

 $(function(){

    $('.czechMap-area').hover(function(){

        $('#czechMap-overlap').attr('src', $(this).attr('data-img') );

    },function(){

        $('#czechMap-overlap').attr('src', 'none.png');
    });

 });

