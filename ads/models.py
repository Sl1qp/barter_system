from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name


class Condition(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Состояние товара")

    def __str__(self):
        return self.name


class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL изображения")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория"
    )
    condition = models.ForeignKey(
        Condition,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Состояние"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.title} (автор: {self.user.username})"


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("accepted", "Принята"),
        ("rejected", "Отклонена"),
    ]

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="sent_proposals")
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="received_proposals")

    comment = models.TextField(verbose_name="Комментарий")
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Предложение "
