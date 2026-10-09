from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'Жоспарланған'),
        ('in_progress', 'Орындалып жатыр'),
        ('done', 'Аяқталған'),
    ]

    title = models.CharField('Атауы', max_length=200)
    description = models.TextField('Сипаттамасы', blank=True)
    status = models.CharField('Күйі', max_length=20, choices=STATUS_CHOICES, default='todo')
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
