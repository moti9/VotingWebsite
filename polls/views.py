from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from polls.forms import EditPollForm, ChoiceForm
from .models import Poll, Choice, Vote, Contact
from django.contrib.auth.models import User
from django.db.models import Count
# from django.core.exceptions import MultiValueDictKeyError
# from django.core.exceptions import FieldError
from django.utils.datastructures import MultiValueDictKeyError
# from django.core.exceptions import ValidationError
# Create your views here.


@login_required
def home(request):
    all_polls = Poll.objects.all()
    # print(all_polls)
    search_term = ''
    try:
        if 'name' in request.GET:
            all_polls = all_polls.order_by('poll_text')

        if 'date' in request.GET:
            all_polls = all_polls.order_by('poll_date')

        if 'vote' in request.GET:
            all_polls = all_polls.annotate(
                Count('vote')).order_by('vote__count')

        if 'search' in request.GET:
            search_term = request.GET['search']
            all_polls = all_polls.filter(text__icontains=search_term)
    except:
        pass
    paginator = Paginator(all_polls, 6)
    # print(paginator.count)
    page = request.GET.get('page')
    # print(page)
    polls = paginator.get_page(page)
    # print(polls)

    dict_copy = request.GET.copy()
    params = dict_copy.pop('page', True) and dict_copy.urlencode()
    context = {
        'polls': polls,
        'params': params,
        'search_term': search_term,
    }
    # print(polls)
    # print(params)
    return render(request, 'polls/index.html', context)


@login_required()
def createpoll(request):
    if request.method == "POST":
        try:
            flag = False
            msg = ""
            poll_text = request.POST['poll-text']
            if not poll_text:
                flag = True
                msg += "Please check your poll."
            num_choices = int(request.POST['choices'])
            if num_choices < 2 or num_choices > 10:
                msg += "Please enter number of choice in range(2-10)."
                flag = True
            for i in range(num_choices):
                choice_text = request.POST['choice'+str(i+1)]
                if not choice_text:
                    msg += "Please enter choice."
                    flag = True
                    break
            if flag:
                messages.error(
                    request, "Hhdgfdgfdgg", extra_tags='alert alert-warning alert-dismissible fade')
                return render(request, 'polls/create.html')
                return
            # Get User
            owner = User(request.user)
            # print(owner)

            # save poll
            poll = Poll(owner=owner.id, poll_text=poll_text)
            poll.save()
            poll_id = Poll(poll).id

            # save choices
            for i in range(num_choices):
                choice_text = request.POST['choice'+str(i+1)]
                choice = Choice(poll=poll_id, choice_text=choice_text)
                choice.save()

            # user = User(id=request.user.id)
            # print(user)
            messages.success(
                request, "Poll created successfully", extra_tags='alert alert-success alert-dismissible fade')
            return render(request, 'polls/create.html')
        # except MultiValueDictKeyError:
        except:
            pass
            return render(request, 'polls/create.html')
            pass
    return render(request, 'polls/create.html')


@login_required()
def list_by_user(request):
    all_polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(all_polls, 6)
    # print("Start")
    # print(paginator.count)
    # print("End")

    page = request.GET.get('page')
    polls = paginator.get_page(page)
    # print("Start")
    # print(polls.count)
    # print("End")

    context = {
        'polls': polls,
    }
    return render(request, 'polls/index.html', context)


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=int(poll_id))

    if not poll.poll_status:
        return render(request, 'polls/result.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'polls/detail.html', context)


@login_required
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            messages.success(request, "Poll Updated successfully.",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("polls:list_by_user")

    else:
        form = EditPollForm(instance=poll)

    return render(request, "polls/edit.html", {'form': form, 'poll': poll})


@login_required
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')
    poll.delete()
    messages.success(request, "Poll Deleted successfully.",
                     extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("polls:list_by_user")


@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    # form = ChoiceForm(instance=poll)
    if request.user != poll.owner:
        return redirect('polls:home')

    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice added successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:edit', poll.id)
    else:
        form = ChoiceForm(instance=poll)
    context = {
        'form': form,
    }
    return render(request, 'polls/add_choice.html', context)


@login_required
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice Updated successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:edit', poll.id)
    else:
        form = ChoiceForm(instance=choice)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': choice,
    }
    return render(request, 'polls/add_choice.html', context)


@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('home')
    choice.delete()
    messages.success(
        request, "Choice Deleted successfully.", extra_tags='alert alert-success alert-dismissible fade')
    return redirect('polls:edit', poll.id)


@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    if not poll.user_can_vote(request.user):
        messages.error(
            request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade')
        return redirect("polls:home")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        # print(vote)
        return render(request, 'polls/result.html', {'poll': poll})
    else:
        messages.error(
            request, "No choice selected!", extra_tags='alert alert-warning alert-dismissible fade')
        return redirect("polls:detail", poll_id)
    return render(request, 'polls/result.html', {'poll': poll})


@login_required
def endpoll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('mypolls')

    if poll.poll_status is True:
        poll.poll_status = False
        poll.save()
        return render(request, 'polls/result.html', {'poll': poll})
    else:
        return render(request, 'polls/result.html', {'poll': poll})


# @login_required
# def contact(request):
#     if not request.user.is_authenticated:
#         return render(request, 'accounts/login')
#     if request.method == "POST":
#         name = request.POST['name']
#         email = request.POST['email']
#         subject = request.POST['subject']
#         message = request.POST['message']
#         try:
#             user = User(request.user)
#             contact = Contact(user=user.id, name=name,
#                               email=email, subject=subject, message=message)
#             contact.save()
#         except:
#             return render(request,'home')
#             return render(request, '/')


# from django.core.mail import send_mail
