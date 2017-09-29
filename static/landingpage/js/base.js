$(document).ready(function() {

  $(".various").fancybox({
    maxWidth  : 800,
    maxHeight : 600,
    fitToView : false,
    width   : '70%',
    height    : '70%',
    autoSize  : false,
    closeClick  : false,
    openEffect  : 'none',
    closeEffect : 'none'
  });

  /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) && ($(".m-mainVideo").remove(), $(".m-mainVideoContainer").append('<div class="m-mainVideo__image"></div>')), $("a[href*=#]").on("click", function(e) {
      e.preventDefault();
      var i = $.attr(this, "href");
      $("html,body").animate({
          scrollTop: $(this.hash).offset().top
      }, 500, function() {
          window.location.hash = i
      })
  }), $(".m-carouselItem > div:gt(0)").hide(), setInterval(function() {
      $(".m-carouselItem > div:first").fadeOut(1e3).next().delay(1e3).fadeIn(1e3).end().appendTo(".m-carouselItem")
  }, 5e3)

});

function trackClick (category, action, label) {
  ga('send', {
    hitType: 'event',
    eventCategory: category,
    eventAction: action,
    eventLabel: label
  });
}

function goToByScroll(id){
  // Remove "link" from the ID
  id = id.replace("link", "");
      // Scroll
  $('html,body').animate({
    scrollTop: $("#"+id).offset().top},
  'slow');
}

$('.m-blogPost').hover(function () {
  console.log($(this).find('.mainButton__link'));
  $(this).find('.mainButton__link').addClass('hover');
}, function () {
  console.log($(this).find('.mainButton__link'));
  $(this).find('.mainButton__link').removeClass('hover');
});

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-59179808-6', 'auto');
ga('send', 'pageview');