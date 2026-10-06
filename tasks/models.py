from django.db import models

class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'todo', 'Жоспарланған'
        IN_PROGRESS = 'in_progress', 'Орындалып жатыр'
        DONE = 'done', 'Аяқталған'

    title = models.CharField('Атауы', max_length=200)
    description = models.TextField('Сипаттамасы', blank=True)
    status = models.CharField('Күйі', max_length=20, choices=Status.choices, default=Status.TODO)
    created_at = models.DateTimeField('Құрылған уақыты', auto_now_add=True)

    class Meta:
        ordering = ['-created_at', '-id']
        verbose_name = 'Тапсырма'
        verbose_name_plural = 'Тапсырмалар'
        constraints = [models.CheckConstraint(
            condition=models.Q(status__in=['todo', 'in_progress', 'done']),
            name='task_status_valid',
        )]

    def __str__(self):
        return self.title
