from django.shortcuts import render, redirect
from .models import User, Activity, UserManager
from django.contrib import messages

# Login, register, and logout commands...

def index(request):
    return render(request, 'index.html')

def login(request):
    print(request.POST)
    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if logged_user.password == request.POST['password']:
            request.session['user'] = logged_user.name
            request.session['id'] = logged_user.id
            return redirect('/admin_edits')
    return redirect('/')

def register_user(request):
    return render(request, 'register_user.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register_user')
    if request.POST['password'] != request.POST['confpw']:
        return redirect('/register_user')
    else:
        new_user = User.objects.create(name=request.POST['name'], email=request.POST['email'], password=request.POST['password'])
        request.session['user'] = new_user.name
        request.session['id'] = new_user.id
        return redirect('/admin_edits')

def logout(request):
    request.session.flush()
    return redirect('/')

# Commands made by the admin (the parents)...

def choiceBoard(request):
    user = User.objects.get(id=request.session['id'])
    activities = Activity.objects.filter(user=user)
    request.session['sum'] = 0
    if 'points_earned' not in request.session:
        request.session['points_earned'] = 0
    for activity in activities:
        request.session['sum'] = request.session['sum'] + activity.points
    my_reward = user.reward
    context = {
        'my_reward': my_reward,
        'activities': activities,
    }
    return render(request, 'choiceBoard.html', context)

def admin_edits(request):
    user = User.objects.get(id=request.session['id'])
    my_activities = Activity.objects.filter(user=user)
    my_reward = user.reward
    context = {
        'my_activities': my_activities,
        'my_reward': my_reward,
        'user': user
    }
    return render(request, 'admin_edits.html', context)

def createActivity(request, id):
    new_item = Activity.objects.create(item=request.POST['item'], points=request.POST['points'], user=User.objects.get(id=id))
    return redirect('/admin_edits')

def createReward(request, id):
    print(id)
    new_reward = User.objects.get(id=id)
    new_reward.reward = request.POST['reward']
    new_reward.save()
    return redirect('/admin_edits')

def delete(request, id):
    activity = Activity.objects.get(id=id)
    activity.delete()
    return redirect('/admin_edits')

def completed_activity(request, id):
    activity = Activity.objects.get(id=id)
    add_points = activity.points
    request.session['points_earned'] = request.session['points_earned'] + activity.points
    return redirect('/choiceBoard')