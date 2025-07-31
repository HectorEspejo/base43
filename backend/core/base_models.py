"""
Base models for Base43 project.
Provides common fields and behaviors for all models.
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating
    created_at and updated_at fields.
    """
    created_at = models.DateTimeField(default=timezone.now, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class AuthorModel(TimeStampedModel):
    """
    Abstract base class that provides author tracking
    with created_by and updated_by fields.
    """
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        editable=False
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        editable=False
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract base class that provides soft delete functionality.
    Records are not actually deleted but marked as deleted.
    """
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    deleted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_deleted",
        editable=False
    )

    class Meta:
        abstract = True

    def delete(self, using=None, soft=True, deleted_by=None):
        """
        Soft delete by default, unless soft=False is passed.
        """
        if soft:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            self.deleted_by = deleted_by
            self.save(using=using)
        else:
            super().delete(using=using)

    def restore(self):
        """
        Restore a soft-deleted record.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save()


class PublishableModel(TimeStampedModel):
    """
    Abstract base class for models that can be published/unpublished.
    """
    is_published = models.BooleanField(default=False, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    
    class Meta:
        abstract = True

    def publish(self):
        """
        Mark the model as published.
        """
        if not self.is_published:
            self.is_published = True
            self.published_at = timezone.now()
            self.save()

    def unpublish(self):
        """
        Mark the model as unpublished.
        """
        self.is_published = False
        self.published_at = None
        self.save()


class OrderableModel(models.Model):
    """
    Abstract base class for models that need to be ordered.
    """
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        abstract = True
        ordering = ['order', '-created_at']


class SEOModel(models.Model):
    """
    Abstract base class for models that need SEO fields.
    """
    meta_title = models.CharField(
        max_length=60,
        blank=True,
        help_text="SEO title (max 60 characters)"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="SEO description (max 160 characters)"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated keywords"
    )
    og_image = models.ImageField(
        upload_to='seo/og/',
        blank=True,
        null=True,
        help_text="Open Graph image for social media"
    )

    class Meta:
        abstract = True


class SlugModel(models.Model):
    """
    Abstract base class for models that need a slug field.
    """
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="URL-friendly version of the name"
    )

    class Meta:
        abstract = True


# Managers for soft-deletable models
class SoftDeleteManager(models.Manager):
    """
    Manager that excludes soft-deleted records by default.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def all_with_deleted(self):
        """
        Return all records including soft-deleted ones.
        """
        return super().get_queryset()

    def deleted_only(self):
        """
        Return only soft-deleted records.
        """
        return super().get_queryset().filter(is_deleted=True)


class PublishedManager(models.Manager):
    """
    Manager that returns only published records.
    """
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
            published_at__lte=timezone.now()
        )