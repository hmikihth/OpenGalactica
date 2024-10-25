from django.db import models

from django.template.defaultfilters import slugify

class Encyclopedia(models.Model):
    title = models.CharField(max_length=255)  # Title of the encyclopedia entry
    content = models.TextField()  # HTML-formatted content
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # Human-readable URL slug

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            # Ensure slug is unique
            while Encyclopedia.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
