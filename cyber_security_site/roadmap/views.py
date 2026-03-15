from django.shortcuts import get_object_or_404, render

from .models import Roadmap, RoadmapStep


# список roadmap
def roadmap_view(request):

    roadmaps = Roadmap.objects.all()

    return render(request, "roadmap/roadmap.html", {"roadmaps": roadmaps})


# страница roadmap со всеми шагами
def roadmap_step_view(request, roadmap_slug):

    roadmap = get_object_or_404(Roadmap, slug=roadmap_slug)

    roadmap_steps = roadmap.steps.all()

    return render(
        request,
        "roadmap/roadmap_steps.html",
        {"roadmap": roadmap, "roadmap_steps": roadmap_steps},
    )


def roadmap_step_detail(request, roadmap_slug, step_slug):

    roadmap = get_object_or_404(Roadmap, slug=roadmap_slug)

    step = get_object_or_404(RoadmapStep, roadmap=roadmap, slug=step_slug)

    return render(
        request, "roadmap/roadmap_step_detail.html", {"roadmap": roadmap, "step": step}
    )
