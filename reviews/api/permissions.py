from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsReviewerOrReadOnly(BasePermission):
    message = "Only reviewer can delete the review"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.reviewer == request.user
        