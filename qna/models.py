from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reputation = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def calculate_reputation(self):
        question_upvotes = self.user.questions.aggregate(Sum('votes__value'))['value__sum'] or 0
        answer_upvotes = self.user.answers.aggregate(Sum('votes__value'))['value__sum'] or 0
        self.reputation = (question_upvotes * 5) + (answer_upvotes * 10)
        self.save()

class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True)
    is_solved = models.BooleanField(default=False)
    accepted_answer = models.ForeignKey('Answer', null=True, blank=True, on_delete=models.SET_NULL, related_name='accepted_for')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def increment_view_count(self):
        self.views += 1
        self.save()

class Answer(models.Model):
    content = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer to {self.question.title}"

    def accept(self):
        # Remove any previously accepted answer
        self.question.answers.filter(is_accepted=True).update(is_accepted=False)
        self.is_accepted = True
        self.save()
        # Update the question
        self.question.is_solved = True
        self.question.accepted_answer = self
        self.question.save()
        # Award reputation to the answer author
        profile = self.author.userprofile
        profile.reputation += 15
        profile.save()

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE, related_name='comments')
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.author.username}"

class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE, related_name='votes')
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE, related_name='votes')

    class Meta:
        unique_together = [
            ('user', 'question'),
            ('user', 'answer'),
        ]

    def __str__(self):
        target = self.question or self.answer
        return f"{self.get_value_display()} by {self.user.username} on {target}"