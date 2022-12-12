from django.db import models

"""
Languages Model
"""
class Language(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50, null=False, blank=False)
  code = models.CharField(max_length=2, null=False, blank=False)

  def __str__(self) -> str:
    return self.name

"""
Channel Type Model
"""
class ChannelType(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50, null=False, blank=False)

  def __str__(self) -> str:
    return self.name

"""
Content Type Model
"""
class ContentType(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50, null=False, blank=False)

  def __str__(self) -> str:
    return self.name

"""
Genre Model
"""
class Genre(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=50, null=False, blank=False)

  def __str__(self) -> str:
    return self.name

"""
Author Model
"""
class Author(models.Model):
  id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=150, null=False, blank=False)
  picture = models.URLField(max_length=200, null=True)

  def __str__(self) -> str:
    return self.name

"""
Channels Model

A Channel stores the hierarchical structure and has a title, a language, a picture and might
contain other subchannels within itself. Channels might also have references to
Contents.
"""
class Channel(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=200, null=False, blank=False)
  language = models.ManyToManyField("Language")
  picture = models.URLField(max_length=200, null=True, blank=True)
  parent = models.ForeignKey("Channel", on_delete=models.CASCADE, null=True, blank=True)
  type = models.ForeignKey("ChannelType", on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self) -> str:
    return self.title
  
  def hasSubChannels(self):
    return Channel.objects.filter(parent=self).count() > 0

"""
Content Model

A Content can contain files (such as videos, pdfs, or text), a set of arbitrary metadata
associated with the content (content descriptions, authors, genre, etc.) and a rating
value which is a decimal number between 0 and 10.
"""
class Content(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=200, null=False, blank=False)
  description = models.TextField()
  authors = models.ManyToManyField("Author")
  genre = models.ManyToManyField("Genre")
  rating = models.DecimalField(max_digits=4, decimal_places=2)
  audio_languages = models.ManyToManyField("Language", related_name="audio")
  subtitle_languages = models.ManyToManyField("Language", related_name="subtitle")
  age_rating = models.CharField(max_length=50) # can be another model...
  type = models.ForeignKey("ContentType", on_delete=models.SET_NULL, null=True)
  channel = models.ForeignKey("Channel", on_delete=models.CASCADE)
  picture = models.URLField(max_length=200, null=True)

  def __str__(self) -> str:
    return self.title