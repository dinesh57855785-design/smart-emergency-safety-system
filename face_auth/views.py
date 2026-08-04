import json
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from accounts.models import User
from .models import FaceProfile


def _parse_descriptor(data):
    if isinstance(data, str):
        data = json.loads(data)
    return [float(x) for x in data]


@csrf_exempt
@require_POST
def face_register_api(request):
    """Store a face descriptor for the currently signed-in user.

    This endpoint is called after the user has registered normally and is
    authenticated. It stores the 128-dimension face descriptor captured by
    face-api.js so it can later be used for face login.
    """
    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "error": "Authentication required."}, status=403)
    try:
        body = json.loads(request.body)
    except (ValueError, TypeError):
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)
    descriptor = body.get("descriptor")
    if not descriptor or not isinstance(descriptor, list):
        return JsonResponse({"ok": False, "error": "No face descriptor provided."}, status=400)
    cleaned = _parse_descriptor(descriptor)
    profile, created = FaceProfile.objects.update_or_create(
        user=request.user,
        defaults={"descriptor": json.dumps(cleaned)},
    )
    return JsonResponse({"ok": True, "created": created, "updated": not created})


@csrf_exempt
@require_POST
def face_login_api(request):
    """Authenticate a user by comparing a captured face descriptor to all
    stored FaceProfile descriptors using Euclidean distance.

    The browser sends the descriptor captured from the webcam; the server
    compares it against every stored profile and logs in the closest match
    if the distance is below the threshold (0.6 = same person by default).
    """
    try:
        body = json.loads(request.body)
    except (ValueError, TypeError):
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)
    descriptor = body.get("descriptor")
    if not descriptor or not isinstance(descriptor, list):
        return JsonResponse({"ok": False, "error": "No face descriptor provided."}, status=400)
    captured = _parse_descriptor(descriptor)
    best_user = None
    best_dist = float("inf")
    threshold = 0.6
    for profile in FaceProfile.objects.select_related("user").all():
        stored = profile.get_descriptor()
        if len(stored) != len(captured):
            continue
        dist = sum((a - b) ** 2 for a, b in zip(stored, captured)) ** 0.5
        if dist < best_dist:
            best_dist = dist
            best_user = profile.user
    if best_user is None or best_dist >= threshold:
        return JsonResponse({"ok": False, "error": "Face not recognized. Please try again or use password login."}, status=401)
    if not best_user.is_active:
        return JsonResponse({"ok": False, "error": "Account is not active."}, status=403)
    login(request, best_user, backend="django.contrib.auth.backends.ModelBackend")
    return JsonResponse({"ok": True, "redirect": "/dashboard/"})


@login_required
def face_status_api(request):
    has_face = FaceProfile.objects.filter(user=request.user).exists()
    return JsonResponse({"ok": True, "has_face": has_face})
