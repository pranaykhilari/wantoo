(function(exports, user) {

    var companyName = user.company,
    firstName = user.firstName;

    /* ==================================================================== *
    * 
    * ===========  All functions for exports
    *
    * =================================================================== */

    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

    // ga('set', 'page', '/new-page.html');
    // ga('send', 'pageview');

    function isUserAuthed() {
      var auth = $('#auth');
      if(auth.data('authed') === "True") {
        return true;
      } else {
        return false;
      }
    }

    //console.log('Authed: ' + $('#auth').data('authed') );

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function csrfSafeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sendRequest(name, val) {
      var data = {}, endpoint = '/api/v1/' + companyName + '/company/';
      data[name] = val;

      // console.log('SendRequest('+name+', '+val+')');
      // console.log( data );

      $.ajax({
        method: "POST",
        url: endpoint,
        data: data
      }).success(function(resp) {
        console.log("Success: " + resp);
      });
      
    }

    function createCompany(name, val) {
      var data = {}, endpoint = '/api/v1/company/';
      data[name] = val;

      console.log('SendRequest('+name+', '+val+')');
      console.log( data );
        console.log( endpoint );

      $.ajax({
        method: "POST",
        url: endpoint,
        data: data
      }).success(function(resp) {

        console.log("Success: " + resp);

        companyName = JSON.parse(resp).slug;

        console.log('UPDATED companyName: '+companyName);

        $('#_modal-Summary .send-to-home a').attr('href', '/'+companyName);
        $('#_modal-Summary #email_button').attr('href', "mailto:?subject="+firstName+" wants your idea. &body="+firstName+" has launched an Idea Board to hear from people like you.%0D%0A%0D%0AMake your voice heard, and add your ideas here: http://wantoo.io/"+companyName);



      }).fail(function(resp){
        console.log("Failure: " + resp);
        location.href="http://wantoo.io/404.html";
      });
      
    }

    function changeModal(m1, m2) {
      var map = {
        "#_modal-Title" : "title",
        "#_modal-Profile": "logo",
        "#_modal-Question" : "question",
        "#_modal-Theme" : "theme",
        "#_modal-Summary" : "get-started"
      };
      newState(map[m2]);
      $(m1).modal('hide');
      $(m2).modal('show');
    }

    function trackClick (category, action, label) {
      ga('send', {
        hitType: 'event',
        eventCategory: category,
        eventAction: action,
        eventLabel: label
      });
    }

    //Question dynamic editing
    $('#id_question').on('keyup keydown focusout',function() {
        if ($('#id_question').val().length == 0)
            $('.introView__questionWrap--text').text("We\'d love your feedback. Tell us what you want.");
        else 
            $('.introView__questionWrap--text').text($('#id_question').val());
    });

    if(isUserAuthed())
      var csrftoken = getCookie('csrftoken');
    // console.log('CSR: ' + csrftoken);

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    function startWelcome() {

      console.log('companyName: '+companyName);
        $('#_modal-Title').modal('show'); 
      // if (companyName == undefined) {
      //   history.pushState('title', null, 'title');
      //   $('#_modal-Title').modal('show'); 
      // } else {
      //   var url = window.location.href;
      //   url = url.substring(url.lastIndexOf('/')+1);
      //   console.log(url);
      //   var map = {
      //     "title": "#_modal-Title",
      //     "logo": "#_modal-Profile",
      //     "question": "#_modal-Question",
      //     "theme": "#_modal-Theme",
      //     "get-started": "#_modal-Summary"
      //   };
      //   if (url !== "") {
      //       console.log("map: "+ map[url]);
      //       changeModal('.modal', map[url]);
      //   } else {
      //     history.pushState('logo', null, 'logo');
      //     $('#_modal-Profile').modal('show');
      //   }
      // }

    } 

    function newState(state) {
      ga('set', 'page', 'welcome/'+state);
      ga('send', 'pageview');
      history.pushState(state, null, state);
    }

    window.onpopstate = function(e) {
      var map = {
        "title": "#_modal-Title",
        "logo": "#_modal-Profile",
        "question": "#_modal-Question",
        "theme": "#_modal-Theme",
        "get-started": "#_modal-Summary"
      };
      console.log(map[e.state]);
      if (map[e.state] !== "title")
      changeModal('.modal', map[e.state]);
    };

    $('#id_title').on('keyup', function(){
      console.log('key up');
      if($(this).val().trim().length >= 3) {
        $('#id_title_button').prop('disabled', false);
      } else if($(this).text().trim().length < 3) {
        $('#id_title_button').prop('disabled', true);
      }
    });


    /* ==================================================================== *
    * 
    * ===========  All modalActions exports   
    *
    * =================================================================== */

    
    // exports.introUpdate = function() {
    //   changeModal('#_modal-Intro', '#_modal-Title');
    // }

    exports.titleUpdate = function() {
      if( $('#id_logo_url').val().length !== 0 ) {
        $('.introView__logoWrap--image').attr('src', $('#id_logo_url').val());
      }
      changeModal('#_modal-Title', '#_modal-Profile');
      createCompany("title", $('#id_title').val() );

      trackClick('link', 'Title Update from Welcome Page', 'Signup Funnel')
      mixpanel.track('Title updated / welcome');  

    }

    exports.logoUpdate = function() {
      
      if( $('#id_logo_url').val().length !== 0 ) {
        sendRequest("logo_url", $('#id_logo_url').val() );
        mixpanel.track('Logo updated / welcome'); 
        $('.introView__logoWrap--image').attr('src', $('#id_logo_url').val());
      } else {
        sendRequest("logo_url", "https://wantoo.io/static/dashboard/img/company_logos/sample-logo.jpg");
        mixpanel.track('Logo skipped / welcome'); 
      }

      $('.introView__questionWrap--text').removeClass('intro-hide');
      changeModal('#_modal-Profile', '#_modal-Question');
      trackClick('link', 'Logo Update from Welcome Page', 'Signup Funnel')

    }

    exports.questionUpdate = function() {
      changeModal('#_modal-Question', '#_modal-Theme');
      if ($('#id_question').val().length == 0) {
        sendRequest("question", "We\'d love your feedback. Tell us what you want.");
        mixpanel.track('Question skipped / welcome'); 
      } else {
        sendRequest("question", $('#id_question').val() );
        mixpanel.track('Question updated / welcome'); 
      }

      trackClick('link', 'Question Update from Welcome Page', 'Signup Funnel')

    }

    exports.lastUpdate =  function() {
      // $('.body1, .introView__backgroundFooter').hide();
      // $('.body2').show();
      // changeModal('#_modal-Theme', '#_modal-Summary');
      sendRequest("color", $('#id_color').val() );

      window.location.href = '/' + companyName + '/manage/feedback/';

      trackClick('link', 'Color Update from Welcome Page', 'Signup Funnel')
      mixpanel.track('Theme color updated / welcome');  
    }

    exports.skip = function(m1, m2) {
      if (m1 == '#_modal-Question')
        sendRequest("question", "We\'d love your feedback. Tell us what you want.");

      if (m1 == '#_modal-Profile')
        sendRequest("logo_url", "https://wantoo.io/static/dashboard/img/company_logos/sample-logo.jpg");

      var map = {
        "#_modal-Title" : "Title",
        "#_modal-Profile": "Logo",
        "#_modal-Question" : "Question",
        "#_modal-Theme" : "Theme color",
        "#_modal-Summary" : "Get started"
      };
      mixpanel.track(map[m1]+ " skipped / welcome" ); 

      if (m1 == '#_modal-Theme') {
        sendRequest("color", "3284FF" );
        window.location.href = '/' + companyName + '/manage/feedback/';
      } else 
        changeModal(m1, m2);

    } 

    startWelcome();

})(modalActions = {}, window.userInfo);
