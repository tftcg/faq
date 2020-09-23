<html>
    <head>
      <link rel="stylesheet" type="text/css" href="style.css"/>
      <script>
          // THIS IS ONLY USED ON NEWS
          function hideAllNews() {
              hideNews('news-1');
              hideNews('news-2');
              hideNews('news-3');
              hideNews('news-4');
              hideNews('news-5');
          }
          function removeCurrentStory() {
              var x = document.getElementById("news-stories");
              var li_elements = x.getElementsByTagName("li");
              for (var i = 0; i < li_elements.length; i++ ) {
                  li_elements[i].classList.remove('current-story');
              }
          }
          function hideNews(id) {
              var x = document.getElementById(id);
              x.style.display = "none";
          }
          function showNews(source, id) {
              hideAllNews();
              var x = document.getElementById(id);
              if (x.style.display === "none") {
                  x.style.display = "block";
              }
              if(source) {
                  removeCurrentStory();
                  source.classList.add('current-story');
              }
          }
      </script>
    </head>
    <body>
        <div id="topbar">
            <img id="logo" src="images/tcg-logo-CON.png" alt="Transformers - Trading Card Game"/>
            <ul id="menu">
                <li class="selected"><a href="">Home</a></li>
                <!-- Home has a message about the state of the game; along with a Recent News sidebar that can be clicked on.
                     The message about state is basically the default news. -->
                <li><a href="">Cards</a></li>
                <!-- Cards has both links to FortMax/Teletraan, and it has links to any custom cards. It also has the history of the game. Perhaps it has resources for making custom cards? -->
                <li><a href="">How &amp; Where to Play</a></li>
                <!-- How to Play links to Videos, and has instructions on how to play -->
                <!-- Also Talks about LGS and online play -->
                <li><a href="">Rules</a></li>
                <!-- Rules links to Aequitas, and to the Aequitas FAQ directly -->
                <li class="standout"><a href="">Links</a></li>
                <!-- Links has a lot of community links. -->
            </ul>
        </div>
