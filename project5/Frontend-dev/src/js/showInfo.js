$(() => {
    $(".mediaItem, #heroInfo").on("click", (e) => {
        var id = e.currentTarget.dataset.id;

        fetch(`/get/${id}`, {
            method: "GET"
        })
        .then(response => response.json())
        .then(media => {
            var modal = $("#exampleModal");

            modal.find(".header-image").css("background-image", `linear-gradient(180deg, rgba(20, 20, 20, 0) 68%, #141414 100%), url("${media.image}")`);
            modal.find(".title").text(media.title);
            modal.find(".modal-body .row div p").text(media.description);
            modal.find(".modal-body .row div span")[0].innerHTML = `<strong>Genre:</strong> ${media.genre}`;
            modal.find(".modal-body .row div span")[1].innerHTML = `<strong>Date:</strong> ${media.date}`;
            modal.find(".view-trailer").attr("href", `/trailer/${media.id}`);
            if(media.isSeries == true){
                modal.find(".edit").attr("href", `/editor/edit/series/${media.id}`);
            }else{
                modal.find(".edit").attr("href", `/editor/edit/movie/${media.id}`);
            }

            var saveButton = modal.find(".modal-header .save-modal");
            console.log(media.saved);
            if(media.saved){
                var oldItem = saveButton.find("svg");
                var newItem = document.createElement("span");
                newItem.classList = "iconify";
                newItem.dataset.icon = "ant-design:heart-filled";
                newItem.style = "color:red; font-size:25px;";
                oldItem.replaceWith(newItem);
            }else{
                var oldItem = saveButton.find("svg");
                var newItem = document.createElement("span");
                newItem.classList = "iconify";
                newItem.dataset.icon = "ant-design:heart-outlined";
                newItem.style = "color:#fff; font-size:25px;";
                oldItem.replaceWith(newItem);
            }
            saveButton.attr("data-id", media.id);

            saveButton.off("click", "**");

            saveButton.on("click", (e) => {
                if(e.currentTarget.dataset.id == id){
                    var save = !media.saved;
                    console.log(id);
                    console.log(e.currentTarget.dataset.id);
                    fetch(`/get/${id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            saved: save
                        })
                      })
                      .then(() => {
                        var oldItem = saveButton.find("svg");
                        var newItem = document.createElement("span");
                        if(save){
                            newItem.classList = "iconify";
                            newItem.dataset.icon = "ant-design:heart-filled";
                            newItem.style = "color:red; font-size:25px;";
                        
                        }else{
                            newItem.classList = "iconify";
                            newItem.dataset.icon = "ant-design:heart-outlined";
                            newItem.style = "color:#fff; font-size:25px;";
                        }
                        media.saved = save;
                        oldItem.replaceWith(newItem);
                        
                      });
                }
                
            });
            
        });
    })
})