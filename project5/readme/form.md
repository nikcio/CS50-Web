# Form validation

Because I use the generic views provied by django I achive form validaion. This validation is then shown in the template if any errors occur.

Example:

```
{% for error in form.genre.errors %}
    <p style="color: white">{{ error }}</p>
{% endfor %}
```

Here the errors from the genre field will be shown in the template.