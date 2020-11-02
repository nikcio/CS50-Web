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
            
    });
}

function like(e){
    var post = e.currentTarget.dataset.id;
    var like = !(e.currentTarget.dataset.like == "true");
    fetch(`/like/${post}`, {
        method: "PUT",
        body: JSON.stringify({
          like: like,
        }),
      });

}

function follow_user(e){
    var user = e.currentTarget.dataset.userid;
    var follow = !(e.currentTarget.dataset.follow == "true");
    fetch(`/follow/${user}`, {
        method: "PUT",
        body: JSON.stringify({
          follow: follow,
        }),
      });
}