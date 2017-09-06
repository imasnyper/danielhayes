from .models import Post
from autofixture import generators, register, AutoFixture

class PostAutoFixture(AutoFixture):
    field_values = {
        'pub_date': generators.DateTimeGenerator(),
    }

register(Post, PostAutoFixture)