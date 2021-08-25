from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


class Group(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.CharField(max_length=50, unique=True)
    google_calendar_email = fields.CharField(max_length=100, default='')


class Event(Model):
    id = fields.IntField(pk=True)
    group = fields.ForeignKeyField('models.Group', related_name='events', on_delete=fields.CASCADE)
    text = fields.CharField(max_length=100)
    date = fields.DatetimeField()

    class Meta:
        unique_together = (('group', 'text', 'date'))

    @property
    def as_dict(self):
        return {'text': self.text, 'date': self.date}


# class Chat(Model):
#     id = fields.BigIntField(pk=True)
#     title = fields.TextField(null=True)
#     invite_link = fields.CharField(max_length=100)
#     type = fields.CharField(max_length=100)

#     class Meta:
#         table = "chat"

#     def __str__(self):
#         return self.name


# class MessageQueue(Model):
#     id = fields.IntField(pk=True)
#     chat = fields.ForeignKeyField('models.Chat', related_name='messages', on_delete=fields.CASCADE)
#     text = fields.TextField()


# class FrequencyPosting(Model):
#     id = fields.IntField(pk=True)
#     chat = fields.ForeignKeyField('models.Chat', related_name='frequency')
#     type = fields.CharField(max_length=20)
#     count_time = fields.IntField(null=True)
#     type_time = fields.CharField(max_length=20, null=True)
#     day_of_week = fields.CharField(max_length=15, null=True)
#     day_of_month = fields.IntField(null=True)

