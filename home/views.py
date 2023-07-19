from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import ListView
from api_backend.models import CryptoCurrency


# Create your views here.
class IndexListView(ListView):
    paginate_by = 10
    model = CryptoCurrency
    template_name = "home/index.html"

    def get_queryset(self):
        queryset = CryptoCurrency.objects.filter(
            price_change_percentage_24h__isnull=False).order_by('-market_cap')[0:4]
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        if queryset is not None:
            context['top_gainers'] = queryset
        return context
    
def test_view(request):
    file_path = "/coinluxe/loaderio-f7cb4845fcb26f88ba745418682e372e.txt"
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
        return HttpResponse(file_content, content_type="text/plain")
    except FileNotFoundError:
        return HttpResponseNotFound("File not found.")
