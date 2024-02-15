
    var adfly_id = 27181549;
    var adfly_advert = 'int';
    var frequency_cap = 5;
    var frequency_delay = 5;
    var init_delay = 3;
    var popunder = true;

            document.addEventListener("DOMContentLoaded", function(event) { 
            var scrollpos = localStorage.getItem('scrollpos');
            if (scrollpos) window.scrollTo(0, scrollpos);
        });

        window.onbeforeunload = function(e) {
            localStorage.setItem('scrollpos', window.scrollY);
        };


        
        
        window.onscroll = function() {scrollFunction()};

  function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
      document.getElementById("topbutton").style.display = "block";
    } else {
      document.getElementById("topbutton").style.display = "none"; 
    }
  }

  // Scroll to the top of the document when the button is clicked
  function topFunction() {
    const duration = 500; // duration of the animation in milliseconds
    const target = document.documentElement; // element to scroll to

    const targetPos = 0; // target position to scroll to
    const startPos = window.pageYOffset; // current position of the scroll

    const distance = targetPos - startPos; // distance to scroll
    let startTime = null;

    function animation(currentTime) {
      if (startTime === null) {
        startTime = currentTime;
      }

      const timeElapsed = currentTime - startTime;
      const run = ease(timeElapsed, startPos, distance, duration);
      window.scrollTo(0, run);

      if (timeElapsed < duration) {
        requestAnimationFrame(animation);
      }
    }
    function ease(t, b, c, d) {
      t /= d / 2;
      if (t < 1) return c / 2 * t * t + b;
      t--;
      return -c / 2 * (t * (t - 2) - 1) + b;
    }

    requestAnimationFrame(animation);
  }
