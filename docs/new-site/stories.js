function hideAllStories() {
  hideStory('story-1');
  hideStory('story-2');
  hideStory('story-3');
  hideStory('story-4');
  hideStory('story-5');
}
function removeCurrentStory() {
  var x = document.getElementById("stories");
  var li_elements = x.getElementsByTagName("li");
  for (var i = 0; i < li_elements.length; i++ ) {
      li_elements[i].classList.remove('current-story');
  }
}
function hideStory(id) {
  var x = document.getElementById(id);
  x.style.display = "none";
}
function showStory(source, id) {
  hideAllStories();
  var x = document.getElementById(id);
  if (x.style.display === "none") {
      x.style.display = "block";
  }
  if(source) {
      removeCurrentStory();
      source.classList.add('current-story');
  }
}
