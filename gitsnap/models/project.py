import uuid
from django.db import models, transaction
from django.conf import settings
from django.template.defaultfilters import slugify
from pygit2 import init_repository

from gitsnap.models.base import BaseTimestampModel


class Project(BaseTimestampModel):
    class Visibility(models.TextChoices):
        PUBLIC = ("public", "Public")
        PRIVATE = ("private", "Private")
        INTERNAL = ("internal", "Internal")

    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="projects")
    name = models.SlugField(max_length=255)
    description = models.TextField(blank=True, null=True)
    visibility = models.CharField(
        max_length=10, choices=Visibility.choices, default=Visibility.PUBLIC
    )
    default_branch = models.CharField(
        verbose_name="default branch", max_length=255, default="main"
    )
    resource = models.FileField(upload_to="projects/", blank=True)

    class Meta:
        db_table = "projects"
        unique_together = ["owner", "name"]

    def __str__(self) -> str:
        return f"{self.owner.username}/{self.name}"

    @classmethod
    @transaction.atomic
    def initiate(cls, owner, name, description=None, visibility=Visibility.PUBLIC):
        try:
            new_project = cls(
                owner=owner,
                name=slugify(name).lower(),
                description=description,
                visibility=visibility,
            )
            repository_path = f"projects/{uuid.uuid4().hex}.git"
            new_project.resource.name = repository_path
            new_project.save()

            git_path = f"{str(settings.MEDIA_ROOT)}/{repository_path}"
            init_repository(path=git_path, bare=True)
            return new_project
        except Exception as e:
            raise e