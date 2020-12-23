# Class based views

I've been using the class based views that django provieds in most of the functionallity of this program. 

The class based views I've used include:

* ListView
* DetailView
* CreateView
* UpdateView

These views has been used along with mixins which made it possible to make login required for views and make the editor views only accessable to editors:

* LoginRequiredMixin
* UserPassesTestMixin

To make sure the editors views was only accessable to editors this function was used in the views with the `UserPassesTestMixin`:

```python
def test_func(self):
    return self.request.user.isEditor
```