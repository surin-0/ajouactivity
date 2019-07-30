(function($) {
  "use strict"; // Start of use strict
  
  // home 화면에서만 기능하도록
    if($(location).attr('pathname') == "/"){
        
    // scroll event를 감지하여서 navbar 숨기고 색 변경시키는 함수
    var headerHeight = $('#mainNav').height();
    $(document).ready(function() {
        $('#mainNav').removeClass('bg-dark');
        
        // main 화면 search 버튼 연동 함수    
        // document ready 후에 연동이 되는 듯
        $('#search_btn').on('click',function(){
            alert('click!');
            console.log('click!');
        })
    });
    $(window).on('scroll', {
        previousTop: 0
      },
      function() {
        var currentTop = $(window).scrollTop();
        //check if user is scrolling up
        if (currentTop < this.previousTop) {
          //if scrolling up...
          if (currentTop > 0) {
            $('#mainNav').addClass('bg-dark');
          } else {
            $('#mainNav').removeClass('bg-dark');
          }
        } else if (currentTop > this.previousTop) {
          //if scrolling down...
          $('#mainNav').addClass('bg-dark');
        }
        this.previousTop = currentTop;
      });
    }
})(jQuery); // End of use strict
