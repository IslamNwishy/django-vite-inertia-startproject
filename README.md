# Django + Vite + Inertia Initialize project tool

## Steps

- Clone the project into a directory on your system
- Rename the repo to your project name
- Create a virtual environment and activate it `python -m venv venv` then `venv/Scripts/activate`
- Install requirements `pip install -r requirements_dev.txt`
- Run `python .\startproject <project name>` with the name of the project you want to initialize
- run `docker compose up`
- in a different terminal tab run `npm run dev`
- navigate to `localhost:8000` to see the welcome page
- Delete the startproject directory after the project is initialized

## Get Started

### Mixins

The project comes with some mixins found at [./utils/inertia_utils/](./utils/inertia_utils/) to ease the creation of inertia compatible django views

#### InertiaViewMixin

Adapts any django view (like `ListView`, `CreateView`, `UpdateView`, `DeleteView`, `LoginView`, `LogoutView`, etc.) to render inertia templates instead of html templates

- Usage

```python
from django.views.generic.edit import CreateView

class MyView(InertiaViewMixin, CreateView):
    form_class = MyForm # this is required if you have an output that you want to serialize
    template_name = 'MyComponent' # the path to the component in the src/pages directory (don't include the extension).
    permission_check=[login_required] # list of decorator functions checking if the user has access (made for ease of use but you can still use the offical way of checking permissions with `method_decorator` if you want)
    ... # normal attributes for the View
```

#### InertiaFormMixin

Serializes a django Form to JSON, and allows for manual serialization for the viewing of objects with `readonly_<attribute_name>` functions.

- Hint: the mixin is automatically appended to any `form_class` used under [InertiaViewMixin](#inertiaviewmixin) if not already inherited.

- Usage

```python
from django import forms
from app_name.models import MyModel

class MyForm(InertiaFormMixin, forms.ModelForm):
    class Meta:
        model=MyModel
        # can use normal fields syntax with __all__ and everything
        # will be used to determine which fields to return for ListView and RetrieveView
        fields=["is_active", "created_by", "text_list"]

    # will be called when the form `serialize_form` or `serialize_fields` methods are sent read_only=true
    # hint: this is done automatically when using ListView/RetrieveView
    def readonly_text_list(self, value):
        return value.replace('\n',' ,')
```

### Frontend

Some premade components to ease the process of creating typical forms made using django

They have tailwind classes already to give a default look, but you are encourged to change them for a new project once you get things going

- Usage:

#### vue3

```javascript
<Form :form='form'/>
```

#### react

```javascript
<Form {...form} />
```
