from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets
# Create your models here.


class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    poll_text = models.TextField()
    poll_date = models.DateTimeField(default=timezone.now)
    poll_status = models.BooleanField(default=True)

    def user_can_vote(self, user):
        users_vote = user.vote_set.all()
        uv = users_vote.filter(poll=self)

        if uv.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            dict = {}
            alert_class = ['primary', 'secondary', 'success',
                           'danger', 'dark', 'warning', 'info']
            dict['alert_class'] = secrets.choice(alert_class)
            dict['text'] = choice.choice_text
            dict['num_votes'] = choice.get_vote_count

            if not self.get_vote_count:
                dict['percentage'] = 0
            else:
                dict['percentage'] = (
                    choice.get_vote_count/self.get_vote_count)*100
            res.append(dict)
        return res

    def __str__(self):
        return f"{self.poll_text}"


class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def __str__(self):
        return f"{self.poll.poll_text[:25]}-{self.choice_text[:25]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.poll.poll_text[:25]}-{self.choice.choice_text[:25]}-{self.user.username}"


class Result(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    result = models.ImageField(upload_to="images/", default=None)

    def __str__(self):
        return f"{self.poll.poll_text[:25]}-RESULT"


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self) -> str:
        return f"{self.name}-{self.email}-{self.subject}"
