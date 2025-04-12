from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Ad, ExchangeProposal, Category, Condition
from .forms import AdForm, ExchangeProposalForm, SignUpForm


class AdListView(ListView):
    model = Ad
    template_name = "ads/list_ads.html"
    context_object_name = "ads"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")
        category_id = self.request.GET.get("category")
        condition_id = self.request.GET.get("condition")

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query))
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if condition_id:
            queryset = queryset.filter(condition__id=condition_id)
        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["conditions"] = Condition.objects.all()
        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = "ads/detail_ad.html"
    context_object_name = "ad"


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = "ads/create_ad.html"
    success_url = reverse_lazy("ads:ad-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = "ads/edit_ad.html"
    success_url = reverse_lazy("ads:ad-list")

    def dispatch(self, request, *args, **kwargs):
        ad = self.get_object()
        if ad.user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AdDeleteView(LoginRequiredMixin, DeleteView):
    model = Ad
    template_name = "ads/delete_ad.html"
    success_url = reverse_lazy("ads:ad-list")

    def dispatch(self, request, *args, **kwargs):
        ad = self.get_object()
        if ad.user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = "ads/list_proposals.html"
    context_object_name = "proposals"
    paginate_by = 10

    def get_queryset(self):
        return ExchangeProposal.objects.filter(
            Q(ad_sender__user=self.request.user) | Q(ad_receiver__user=self.request.user)
        ).order_by("-created_at")


class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ExchangeProposalForm
    template_name = "ads/create_proposal.html"
    success_url = reverse_lazy("ads:proposal-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.status = "pending"
        return super().form_valid(form)


class ProposalUpdateView(LoginRequiredMixin, UpdateView):
    model = ExchangeProposal
    fields = ["status"]
    template_name = "ads/update_proposal.html"
    success_url = reverse_lazy("ads:proposal-list")

    def dispatch(self, request, *args, **kwargs):
        proposal = self.get_object()
        if proposal.ad_receiver.user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ProposalDeleteView(LoginRequiredMixin, DeleteView):
    model = ExchangeProposal
    template_name = "ads/delete_proposal.html"
    success_url = reverse_lazy("ads:proposal-list")

    def dispatch(self, request, *args, **kwargs):
        proposal = self.get_object()
        if proposal.ad_sender.user != request.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, "register/signup.html", {"form": form})
