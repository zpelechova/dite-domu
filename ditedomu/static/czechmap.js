//Author: Jan Matoušek
//Contact: matousek.vr@gmail.com
//License: GPL

  $(function(){
     var czechMapOverlap = $('#czechMap-overlap'),
         czechMap = $('#czechMap'); 
     
     // map hover 
     $('.czechMap-area').hover(function(){
         
         czechMapOverlap.attr('src', $(this).attr('data-img') );
         czechMapOverlap.hide(0).stop(false, true);
         czechMapOverlap.fadeIn(500);
         
     },function(){
         
         czechMapOverlap.attr('src', '/static/none.png');
         czechMapOverlap.show(0);
     });
     
     // links hover
     $('#czechMapLinks a').hover(function(){
     
         czechMapOverlap.attr('src', czechMap.find('[href="' + $(this).attr('href') + '"]').attr('data-img') );
         czechMapOverlap.hide(0).stop(false, true);
         czechMapOverlap.fadeIn(300);
         
     },function(){
         
         czechMapOverlap.attr('src', '/static/none.png');
         czechMapOverlap.show(0);
         
     });
  });