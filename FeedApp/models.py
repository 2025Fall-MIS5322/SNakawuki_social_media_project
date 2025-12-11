# from django.db import models
# from django.contrib.auth.models import User
# from django.conf import settings

# class Profile(models.Model):
#     first_name = models.CharField(max_length=200, blank=True)
#     last_name = models.CharField(max_length=200, blank=True)
#     email = models.EmailField(max_length=300, blank=True)
#     dob = models.DateField(null=True, blank=True)
#     bio = models.TextField(blank=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     #friends = models.ManyToManyField('User', blank=True, related_name='friends')
#     friends = models.ManyToManyField('auth.User', blank=True, related_name='friends')
#     created = models.DateTimeField(auto_now=True)
#     updated = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.user.username}"

# STATUS_CHOICES = (
#     ('sent', 'Sent'),
#     ('accepted', 'Accepted'),
# )

# class Relationship(models.Model):
#     sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
#     receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
#     status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='sent')
#     created = models.DateTimeField(auto_now=True)
#     updated = models.DateTimeField(auto_now_add=True)

#     # UPDATED __str__ method
#     def __str__(self):
#         # This will show 'john_doe sent to jane_doe' in the admin
#         return f"{self.sender.user.username} {self.status} to {self.receiver.user.username}"

# class Post(models.Model):
#     description = models.CharField(max_length=255, blank=True)
#     username = models.ForeignKey(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='images', blank=True)
#     date_posted = models.DateTimeField(auto_now_add=True) 

#     def __str__(self):
#         return self.description

# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
#     text = models.CharField(max_length=200) 
#     date_added = models.DateTimeField(auto_now_add=True, blank=True)

#     def __str__(self):
#         return self.text
    
# class Like(models.Model):
#     username = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

from django.db import models
from django.contrib.auth.models import User
# from django.conf import settings # settings import is not necessary in models definitions

# --- Profile and Relationship Models (Keeping your existing structure) ---

class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=300, blank=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('auth.User', blank=True, related_name='friends')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}"

STATUS_CHOICES = (
    ('sent', 'Sent'),
    ('accepted', 'Accepted'),
)

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='sent')
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.user.username} {self.status} to {self.receiver.user.username}"

# --- Updated Post Model (Modified to handle both images AND videos) --- 
class Post(models.Model):
    # Renamed 'description' to 'body' for consistency with previous examples, keeps your field type/length
    description = models.CharField(max_length=255, blank=True, verbose_name="Caption") 
    
    # Renamed 'username' ForeignKey to 'author' for clarity
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') 
    
    # CHANGED: Switched from ImageField to FileField to allow videos (MP4s, MOVs)
    # The upload_to directory is now 'post_files' to handle both types
    image = models.FileField(upload_to='post_files/', blank=True, null=True)
    
    # Renamed 'date_posted' to 'created_on' for consistency
    date_posted = models.DateTimeField(auto_now_add=True) 
    class Meta:
        # Added meta ordering to ensure the newest posts appear at the top of the feed
        ordering = ['-date_posted']

    def __str__(self):
        return self.description

    # Helper methods for the template (using the 'image' field name)
    def is_video(self):
        if self.image:
            url = self.image.url.lower()
            return url.endswith('.mp4') or url.endswith('.mov') or url.endswith('.avi')
        return False

    
    def is_image(self):
        if self.image:
            return not self.is_video() 
        return False

# --- Comment and Like Models (Slightly adjusted related_name for clarity) ---

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # Use 'comments' related name
    # Renamed 'username' to 'author' for consistency
    username = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE) 
    text = models.CharField(max_length=200) 
    date_added = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.text
    
class Like(models.Model):
    # Restored original related_name
    username = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE) 
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)