# Password reset

In the project you have the possibility to change your password if you forgot it. This is done by using the functionallity given by django. Here I created the needed pages in the `accounts\templates\registration` folder and added the needed settings to the settings file:

```python
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = str(BASE_DIR.joinpath('sent_emails'))
```

This gives us the possibillity to "send" emails to a folder. In this case I've picked the folder sent_emails. Here emails sent by the password reset function be sent.

We can use the link given in the email to complete the password reset process and thereby change the users password.

**All the pages used with password recovery doesn't have any crasy styling because I felt that the default styling was sufficient.**