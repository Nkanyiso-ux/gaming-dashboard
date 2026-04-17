
from django.shortcuts import render, redirect
from .models import GamingSession
from .forms import GamingSessionForm
from django.shortcuts import get_object_or_404

def dashboard_view(request):
    sessions = GamingSession.objects.all().order_by('-date')

    # ✅ FILTER LOGIC
    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    if start_date and end_date:
        sessions = sessions.filter(date__range=[start_date, end_date])

    total_sessions = sessions.count()
    total_profit = sum(s.profit or 0 for s in sessions)
    biggest_win = max([s.best_win for s in sessions], default=0)

    wins = sum(1 for s in sessions if (s.profit or 0) > 0)
    losses = sum(1 for s in sessions if (s.profit or 0) <= 0)
    win_rate = (wins / total_sessions * 100) if total_sessions > 0 else 0

    dates = [s.date.strftime("%Y-%m-%d") for s in sessions]
    profits = [s.profit or 0 for s in sessions]
    games = [s.game_name for s in sessions]

    if request.method == "POST":
        form = GamingSessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
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
        'losses': losses,
        'wins': wins,
    })
 


def delete_session(request, id):
    if request.method == 'POST':
        session = get_object_or_404(GamingSession, id=id)
        session.delete()
 
    return redirect('dashboard')

def overview(request):
    sessions = GamingSession.objects.all()

    total_sessions = sessions.count()
    total_profit = sum(s.profit or 0 for s in sessions)
    biggest_win = max([s.best_win for s in sessions], default=0)

    wins = sum(1 for s in sessions if (s.profit or 0) > 0)
    win_rate = (wins / total_sessions * 100) if total_sessions > 0 else 0

    dates = [s.date.strftime("%Y-%m-%d") for s in sessions]
    profits = [s.profit or 0 for s in sessions]

    return render(request, 'dashboard/overview.html', {
        'total_sessions': total_sessions,
        'total_profit': total_profit,
        'biggest_win': biggest_win,
        'win_rate': round(win_rate, 2),
        'dates': dates,
        'profits': profits,
    })