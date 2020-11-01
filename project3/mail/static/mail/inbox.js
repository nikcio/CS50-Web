document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");

  // Assignment listeners
  document
    .querySelector("#compose-form")
    .addEventListener("submit", send_email);
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";

  // Assignment code
  document.querySelector("#email-detail").style.display = "none";
  document.querySelector("#message").innerHTML = "";
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  // Assignment code
  document.querySelector("#email-detail").style.display = "block";

  document.querySelector("#emails-view").innerHTML = '';
  document.querySelector("#email-detail").innerHTML = '';

  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      for(var i = 0; i < emails.length; i++) {
        var email = emails[i];
        const element = document.createElement("div");
        const from = document.createElement("span");
        from.innerHTML = `From: ${email["sender"]}`;
        element.append(from);
        const subject = document.createElement("span");
        subject.innerHTML = `Subject: ${email["subject"]}`;
        element.append(subject);
        const date = document.createElement("span");
        date.innerHTML = `Date: ${email["timestamp"]}`;
        element.append(date);
        element.classList += "email-item";

        if(email["read"] === true){
          element.classList += " read"
        }

        if(mailbox === "inbox"){
          const archive = document.createElement("button");
          archive.innerHTML = "Archive";
          archive.dataset.id = email["id"];
          archive.dataset.archive = true;
          archive.classList += "btn  btn-sm btn-primary";
          archive.addEventListener("click", archive_email);
          element.append(archive);
        }else if(mailbox === "archive"){
          const archive = document.createElement("button");
          archive.innerHTML = "Unarchive";
          archive.dataset.id = email["id"];
          archive.dataset.archive = false;
          archive.classList += "btn  btn-sm btn-primary";
          archive.addEventListener("click", archive_email);
          element.append(archive);
        }

        element.dataset.id = email["id"];
        element.addEventListener("click", email_clicked);
        document.querySelector("#emails-view").append(element);
      }
    }).then(() => document.querySelector("#message").innerHTML = "");
}

// Assignment functions
function send_email() {
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: document.querySelector("#compose-recipients").value,
      subject: document.querySelector("#compose-subject").value,
      body: document.querySelector("#compose-body").value,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      if (result["error"] != undefined) {
        document.querySelector("#message").innerHTML = result["error"];
      } else {
        document.querySelector("#message").innerHTML = result["message"];
        load_mailbox("sent");
      }
    });
}

function email_clicked(e) {
  var email = e.currentTarget.dataset.id
  if(e.target.nodeName != "BUTTON"){
    fetch(`/emails/${email}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
    fetch(`/emails/${email}`)
    .then(response => response.json())
    .then(email => {
        load_email(email);
    });
  }
}

function load_email(email){
  document.querySelector("#emails-view").innerHTML = '';
  document.querySelector("#email-detail").innerHTML = '';
  
  const element = document.querySelector("#email-detail")
  const from = document.createElement("span");
  from.innerHTML = `<strong>From:</strong> ${email["sender"]}`;
  element.append(from);
  const to = document.createElement("span");
  to.innerHTML = `<strong>To:</strong> ${email["recipients"]}`;
  element.append(to);
  const subject = document.createElement("span");
  subject.innerHTML = `<strong>Subject:</strong> ${email["subject"]}`;
  element.append(subject);
  const date = document.createElement("span");
  date.innerHTML = `<strong>Timestamp:</strong> ${email["timestamp"]}`;
  element.append(date);
  const body = document.createElement("span");
  body.innerHTML = `${email["body"]}`;
  const reply = document.createElement("button");
  reply.innerHTML = 'Reply';
  reply.classList += "btn  btn-sm btn-outline-primary";
  reply.dataset.from = email["sender"];
  reply.dataset.subject = email["subject"];
  reply.dataset.body = email["body"];
  reply.dataset.date = email["timestamp"];
  reply.addEventListener('click', reply_mail);
  element.append(reply);
  element.append(body);
}

function archive_email(e){
  var email = e.currentTarget.dataset.id;
  var archive = (e.currentTarget.dataset.archive == 'true');

  fetch(`/emails/${email}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: archive
        
    })
  }).then(() => {
      if(archive){
        load_mailbox("inbox");
      }else{
        load_mailbox("archive")
      }
    });
}

function reply_mail(e){
  var from = e.currentTarget.dataset.from;
  var subject = e.currentTarget.dataset.subject;
  var body = e.currentTarget.dataset.body;
  var date = e.currentTarget.dataset.date;
  compose_email();

  document.querySelector("#compose-recipients").value = from;

  var prefix;

  if(subject.substring(0, 4) === "Re: "){
    prefix = "";
  }else{
    prefix = "Re: "
  }

  document.querySelector("#compose-subject").value = `${prefix}${subject}`;
  document.querySelector("#compose-body").value = `\r\n\r\n On ${date} ${from} wrote: ${body}`;

}