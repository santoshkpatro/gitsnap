from django.http import Http404

from gitsnap.models import User, Project


class ProjectPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        user: User = User.objects.filter(username=kwargs.get("username")).first()
        if not user:
            raise Http404

        project: Project = Project.objects.filter(
            owner=user, name=kwargs.get("name")
        ).first()
        if not project:
            raise Http404

        if project.visibility == Project.Visibility.PRIVATE:
            # Check for owner permissions for private projects
            if not request.user.is_authenticated:
                raise Http404

            if not request.user == project.owner:
                raise Http404

        request.project = project
        return super().dispatch(request, *args, **kwargs)
