# Logins

The project has two login pages. These pages can be found in this folder: `accounts\templates\registration`

By using two different login pages we can navigate the user differetly by knowing if it's an editor or a standard user which is loggin on.

By default all users will be created as a standard user. To become an editor you need to change the value in the django admin under users.

When a user is editor can the user access pages which is used by an editor and they can create, update and delete content.

We use two views to make sure you don't think that you can create an edior user yourself and to make the editor login page a little more special.

The normal login page can be found at: `http://127.0.0.1:8000/accounts/login` this is also the page you're sent to if you try to access the website without logging in first.

To see the editor page go to `http://127.0.0.1:8000/accounts/editorlogin`

**Both logins have djangos standard form validation and shows errors on if you enter wrong credentials.**