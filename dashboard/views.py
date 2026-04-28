
from django.shortcuts import render, redirect, get_object_or_404
from .models import GamingSession
from .forms import GamingSessionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import openpyxl
from django.http import HttpResponse

@login_required
def dashboard_view(request):
    sessions = GamingSession.objects.filter(user=request.user).order_by('-date')

    total_sessions = sessions.count()
    total_profit = sum(s.profit or 0 for s in sessions)
    biggest_win = max([s.best_win for s in sessions], default=0)

    wins = sum(1 for s in sessions if s.profit > 0)
    losses = sum(1 for s in sessions if s.profit <= 0)
    win_rate = (wins / total_sessions * 100) if total_sessions else 0

    dates = [s.date.strftime("%Y-%m-%d") for s in sessions]
    profits = [s.profit for s in sessions]
    games = [s.game_name for s in sessions]

    if request.method == "POST":
        form = GamingSessionForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('dashboard')
        else:
            print("FORM ERRORS:", form.errors)  # DEBUG

    else:
        form = GamingSessionForm()

    return render(request, 'dashboard/dashboard.html', {
        'sessions': sessions,
        'form': form,
        'total_sessions': total_sessions,
        'total_profit': total_profit,
        'biggest_win': biggest_win,
        'win_rate': round(win_rate),
        'dates': dates,
        'profits': profits,
        'games': games,
        'wins': wins,
        'losses': losses,
    })

@login_required
def overview(request):
    sessions = GamingSession.objects.filter(user=request.user)

    total_sessions = sessions.count()
    total_profit = sum(s.profit or 0 for s in sessions)
    biggest_win = max([s.best_win for s in sessions], default=0)

    wins = sum(1 for s in sessions if (s.profit or 0) > 0)
    losses = sum(1 for s in sessions if (s.profit or 0) <= 0)
    win_rate = (wins / total_sessions * 100) if total_sessions > 0 else 0

    dates = [s.date.strftime("%Y-%m-%d") for s in sessions]
    profits = [s.profit or 0 for s in sessions]

    return render(request, 'dashboard/overview.html', {
        'total_sessions': total_sessions,
        'total_profit': total_profit,
        'biggest_win': biggest_win,
        'win_rate': round(win_rate),
        'dates': dates,
        'profits': profits,
        'wins': wins,
        'losses': losses,
    })

def delete_session(request, id):
    session = get_object_or_404(GamingSession, id=id, user=request.user)
    session.delete()
    return redirect('dashboard')


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "dashboard/login.html", {"error": "Invalid credentials"})

    return render(request, "dashboard/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def edit_session(request, id):
    session = get_object_or_404(GamingSession, id=id, user=request.user)

    form = GamingSessionForm(request.POST or None, instance=session)

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('dashboard')

    return render(request, 'dashboard/editSession.html', {'form': form})

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "dashboard/register.html", {"form": form})

@login_required
def add_session(request):
    if request.method == "POST":
        form = GamingSessionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('dashboard')
    else:
        form = GamingSessionForm()

    return render(request, 'dashboard/add_session.html', {'form': form})

@login_required
def export_excel(request):
    sessions = GamingSession.objects.filter(user=request.user)
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sessions"

    # Headers
    headers = ["Date", "Game", "Start", "End", "Profit", "Spins", "Bet"]
    ws.append(headers)

    # Data rows
    for s in sessions:
        ws.append([
            str(s.date),
            s.game_name,
            s.start_balance,
            s.end_balance,
            s.profit,
            s.spins,
            s.bet
        ])

    # Response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=gaming_sessions.xlsx'

    wb.save(response)
    return response












