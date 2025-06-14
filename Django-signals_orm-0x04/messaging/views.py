from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Your account and data were deleted successfully.")
        return redirect("home")  # or your login/home URL
    return redirect("profile")  # fallback if not POST
