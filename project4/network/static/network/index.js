document.addEventListener("DOMContentLoaded", function() {
    if (document.querySelector("#following") == null){
        document.querySelector("#new-post").style.display = "none";
    }
    if(document.querySelector("#new-post-form") != null){
        document.querySelector("#new-post-form").addEventListener("submit", add_post);
    }
    if(document.querySelector("#follow") != null){
        document.querySelector("#follow").addEventListener("click", follow_user);
    }
    if(document.getElementsByClassName("like") != null){
        var likeButtons = document.getElementsByClassName("like");
        Array.from(likeButtons).forEach(function(element) {
            element.addEventListener('click', like);
          });
    }
    if(document.getElementsByClassName("edit") != null){
      var likeButtons = document.getElementsByClassName("edit");
      Array.from(likeButtons).forEach(function(element) {
          element.addEventListener('click', edit);
        });
  }
});

function add_post(){
    fetch("/newpost", {
        method: "POST",
        body: JSON.stringify({
          content: document.querySelector("#content").value,
        }),
      })
        .then(() => {
            document.querySelector("#content").value = "";
            location.reload();
    });
}

function like(e){
    var post = e.currentTarget.dataset.id;
    var like = !(e.currentTarget.dataset.like == "true");
    var target = e.currentTarget;
    fetch(`/like/${post}`, {
        method: "PUT",
        body: JSON.stringify({
          like: like,
        }),
      }).then(() => {
        var parrent = document.querySelector(`#post-${post}`);
        if(like){
          parrent.querySelector("#likes").innerHTML = parseInt(target.dataset.cur_likes) + 1;
          target.dataset.cur_likes = parseInt(target.dataset.cur_likes) + 1;
          target.dataset.like = like;
          target.innerHTML = "Unlike";

          var oldItem = parrent.querySelector("svg");
          var newItem = document.createElement("span");
          newItem.classList += "iconify";
          newItem.dataset.icon = "ant-design:heart-filled";
          newItem.dataset.inline = "false";
          newItem.style = "color:red;";

          parrent.replaceChild(newItem, oldItem);

        }else{
          parrent.querySelector("#likes").innerHTML = parseInt(target.dataset.cur_likes) - 1;
          target.dataset.cur_likes = parseInt(target.dataset.cur_likes) - 1;
          target.dataset.like = like;
          target.innerHTML = "Like";

          var oldItem = parrent.querySelector("svg");
          var newItem = document.createElement("span");
          newItem.classList += "iconify";
          newItem.dataset.icon = "ant-design:heart-outlined";
          newItem.dataset.inline = "false";

          parrent.replaceChild(newItem, oldItem);
        }
        
      });

}

function follow_user(e){
    var user = e.currentTarget.dataset.userid;
    var follow = !(e.currentTarget.dataset.follow == "true");
    var target = e.currentTarget;
    fetch(`/follow/${user}`, {
        method: "PUT",
        body: JSON.stringify({
          follow: follow,
        }),
      }).then(() => {
        var followerCount = document.querySelector("#followers");
        if(follow){
          target.innerHTML = "Unfollow";
          target.dataset.follow = follow;
          followerCount.innerHTML = "Followers: " + (parseInt(followerCount.dataset.count) + 1);
          followerCount.dataset.count = parseInt(followerCount.dataset.count) + 1;
        }else{
          target.innerHTML = "Follow";
          target.dataset.follow = follow;
          followerCount.innerHTML = "Followers: " + (parseInt(followerCount.dataset.count) - 1);
          followerCount.dataset.count = parseInt(followerCount.dataset.count) - 1;
        }
      });
}

function edit(e){
    var target = e.currentTarget;

    var parrent = document.querySelector(`#post-${target.dataset.id}`);

    if(target.dataset.edit == "true"){
      var oldText = parrent.querySelector("#content");
      var newText = document.createElement("textarea");
      newText.value = oldText.innerHTML;
  
      parrent.replaceChild(newText, oldText);

      target.dataset.edit = "false";
      target.innerHTML = "Save";
    }else{
      var oldText = parrent.querySelector("textarea");
      var newText = document.createElement("span");
      newText.innerHTML = oldText.value;
      newText.id = "content";

      parrent.replaceChild(newText, oldText);

      target.dataset.edit = "true";
      target.innerHTML = "Edit";

      fetch(`/update/${target.dataset.id}`, {
        method: "PUT",
        body: JSON.stringify({
          content: oldText.value,
        }),
      });
    }
    
    
}