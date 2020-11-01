document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("#all-posts").addEventListener("click", () => load_view("posts"));
    if(document.querySelector("#following") != null){
        document.querySelector("#following").addEventListener("click", () => load_view("following"));
    }else{
        document.querySelector("#new-post").style.display = "none";
    }
    

    load_view("posts");

    document.querySelector("#new-post-form").addEventListener("submit", add_post);
});

function load_view(view){
    document.querySelector("#post-view").innerHTML = "";
    document.querySelector("#following-view").innerHTML = "";
    document.querySelector("#title").innerHTML = view.charAt(0).toUpperCase() + view.slice(1);

    switch(view){
        case "posts":
            document.querySelector("#post-view").style.display = "block";
            document.querySelector("#following-view").style.display = "none";
            load_posts();
            break;
        case "following":
            document.querySelector("#post-view").style.display = "none";
            document.querySelector("#following-view").style.display = "block";
            load_following();
            break;
    }

}

function load_posts(){
    fetch("/posts")
        .then((response) => response.json())
        .then((info) => {
            for(var i = 0; i < info.length; i++){
                var item = info[i];
                const element = document.createElement("div");
                const content = document.createElement("span");
                content.innerHTML = item["content"];
                element.append(content);
                element.classList += "list-item";

                const user = document.createElement("span");
                user.innerHTML = item["user"];
                element.append(user);
                
                if(item["liked"]){
                    const heart = document.createElement("span");
                    heart.classList += "iconify";
                    heart.dataset.icon = "ant-design:heart-filled";
                    heart.dataset.inline = "false";
                    heart.style.color = "red";
                    element.append(heart);
                }else{
                    const heart = document.createElement("span");
                    heart.classList += "iconify";
                    heart.dataset.icon = "ant-design:heart-outlined";
                    heart.dataset.inline = "false";
                    element.append(heart);
                }

                const likes = document.createElement("span")
                likes.innerHTML = item["likes"];
                element.append(likes);

                const time = document.createElement("span");
                time.innerHTML = item["time"];
                time.classList += "time";
                element.append(time);
                
                if(item["liked"] != "ano"){
                    element.dataset.id = item["id"];
                    element.dataset.like = item["liked"];
                    element.addEventListener("click", like);
                }

                const container = document.createElement("div");
                container.append(element);
                
                if(item["following"] != "ano"){
                    const follow = document.createElement("button");
                    follow.classList += "btn btn-sm btn-primary";
                    follow.dataset.userid = item["userid"];
                    follow.dataset.follow = item["following"];
                    follow.addEventListener("click", follow_user)
                    if(item["following"]){
                        follow.innerHTML = "Unfollow";
                    }else{
                        follow.innerHTML = "Follow";
                    }
                    container.append(follow);
                }
                

                document.querySelector("#post-view").append(container);
            }
        });
}

function load_following(){
    fetch("/following")
        .then((response) => response.json())
        .then((info) => {
            for(var i = 0; i < info.length; i++){
                var item = info[i];
                const element = document.createElement("div");
                const content = document.createElement("span");
                content.innerHTML = item["username"];
                element.append(content);
                element.classList += "list-item";

                document.querySelector("#following-view").append(element);
            }
        });
}

function add_post(){
    fetch("/newpost", {
        method: "POST",
        body: JSON.stringify({
          content: document.querySelector("#content").value,
        }),
      })
        .then(() => {
            document.querySelector("#content").value = "";
            load_view("posts");
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
      })
        .then(() => {
            load_view("posts");
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
      })
        .then(() => {
            load_view("posts");
    });
}