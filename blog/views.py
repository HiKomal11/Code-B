from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import BlogPost
from .serializers import BlogPostSerializer
@api_view(['GET'])
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-date')
    data = [
        {
            "id": post.id,
            "title": post.title,
            "date": post.date,
            "excerpt": post.excerpt,
            "image": post.image.url if post.image else None,
            "category": post.category.name if post.category else None,
        }
        for post in posts
    ]
    return Response(data)

@api_view(['GET'])
def blog_detail(request, pk):
    try:
        post = BlogPost.objects.get(pk=pk)
        data = {
            "id": post.id,
            "title": post.title,
            "date": post.date,
            "content": post.content,  # ✅ rich text HTML
            "image": post.image.url if post.image else None,
            "category": post.category.name if post.category else None,
        }
        return Response(data)
    except BlogPost.DoesNotExist:
        return Response({"error": "Not found"}, status=404)



class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.all().order_by("-created_at")
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]