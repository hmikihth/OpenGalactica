from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
    
class News(models.Model):
    class Meta:
        verbose_name_plural = "News"
    
    author = models.ForeignKey("Planet", on_delete=models.CASCADE)  # Link to the Planet model
    round = models.IntegerField()  # Game round when the news was created
    turn = models.IntegerField()   # Game turn when the news was created
    server_time = models.DateTimeField(default=timezone.now)  # Automatically set to current server time
    title = models.CharField(max_length=255)  # Title of the news article
    content = models.TextField()  # HTML-formatted content
    slug = models.SlugField(max_length=300, unique=True, blank=True)  # Human-readable URL slug

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.round}-{self.turn}-{self.title}")
            self.slug = base_slug
            counter = 1
            # Ensure slug is unique
            while News.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
        

    @property
    def description(self):
        return self.content if len(self.content) < 255 else self.content[:255] + "..."

    @property
    def timestamp(self):
        """Returns a string in the format round:turn:minutes (e.g., 5:120:42)"""
        return f"{self.round}:{self.turn}:{self.server_time.minute}"
        
