from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import create_class_form,create_assignment_form,create_poll_form,add_answer_form,ParticipantsForm
from django.contrib.auth.models import User
from .models import ClassRoom,Assignment,Answer,Poll
from django.shortcuts import redirect
import datetime


@login_required(login_url='/accounts/login')
def home(request):
    classes = ClassRoom.objects.filter(host=request.user)
    all_classes = ClassRoom.objects.all()
    classes_you_are_in=[]
    for user_class in all_classes:
        if user_class.students.filter(username = request.user):
            classes_you_are_in.append(user_class)
    return render(request, 'lab/home.html',{'classes':classes,'classes_you_are_in':classes_you_are_in})

@login_required(login_url='/accounts/login')
def classroom(request,pk):
    classroom = ClassRoom.objects.get(id=pk)
    assignments = classroom.assignment_set.all()
    students = classroom.students.all()
    form = ParticipantsForm()

    for assignment in assignments:
        assignment.question = assignment.question[:400]
        date = str(assignment.due_date).split('-')
        time = str(assignment.due_time).split(':')
        date_time = date+time
        date_time = list(map(int,date_time))
        due_date =datetime.datetime(*date_time)
        current_date = datetime.datetime.now()
        if(due_date<current_date):
            assignment.status = "completed"
            assignment.save()
    ongoing_assignments=[]
    for assignment in assignments:
        if(assignment.status=='ongoing'):
            assignment.question = assignment.question[:50]
            ongoing_assignments.append(assignment)
    return render(request, 'lab/classroom.html',{'assignments':assignments,'classroom':classroom,'students':students,'form':form,'ongoing_assignments':ongoing_assignments})

@login_required(login_url='/accounts/login')
def create_class(request):
    form = create_class_form()
    if request.method == "POST":
        form = create_class_form(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            classname = form.cleaned_data['classname']
            class_room_details = ClassRoom(subject=subject,classname=classname)
            class_room_details.host = request.user
            class_room_details.save()
            class_room_details.students.add(request.user)
            return redirect('/lab')
    return render(request, 'lab/create_class.html',{"form":form})

@login_required(login_url='/accounts/login')
def create_assignment(request,pk):
    classroom = ClassRoom.objects.get(id=pk)
    form = create_assignment_form()
    if request.method == 'POST':
        form = create_assignment_form(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            type = form.cleaned_data['type']
            due_date = form.cleaned_data['due_date']
            due_time = form.cleaned_data['due_time']
            assignment_details = Assignment(question=question,type=type,due_date=due_date,due_time=due_time)
            assignment_details.class_in = classroom
            assignment_details.save()
            if(assignment_details.type=='poll'):
                return redirect('create_poll',pk=assignment_details.id)
            return redirect('classroom',pk=pk)
    return render(request, 'lab/create_assignment.html',{"form":form,"classroom":classroom})

@login_required(login_url='/accounts/login')
def question(request,pk):
    assignment = Assignment.objects.get(id=pk)
    answers = assignment.answer_set.all()
    if assignment.type == 'poll':
        poll = assignment.poll
    form = add_answer_form()
    return render(request, 'lab/question.html',{'assignment':assignment,'form':form,'answers':answers,'poll':poll})

@login_required(login_url='/accounts/login')
def vote(request, pk):
    poll = Poll.objects.get(id = pk)
    if request.method == 'POST':
        options = request.POST['poll']
        if options == 'option1':
            poll.option_one_count += 1
        elif options == 'option2':
            poll.option_two_count += 1
        elif options == 'option3':
            poll.option_three_count += 1
        elif options == 'option4':
            poll.option_four_count += 1
        elif options == 'option5':
            poll.option_five_count += 1
        else:
            HttpResponse(400, 'Invalid form')
        poll.save()
        return redirect('question',pk=poll.assignment_in.id)
    return render(request, "lab/question.html")

@login_required(login_url='/accounts/login')
def add_participants(request,pk):
    form = ParticipantsForm()
    classroom = ClassRoom.objects.get(id=pk)
    if request.method == 'POST':
        form = ParticipantsForm(request.POST)
        if form.is_valid():
            # answer = form.cleaned_data['answer']
            students = form.cleaned_data['students']
            for student in students:
                add_student = User.objects.get(username=student)
                classroom.students.add(add_student)
            return redirect('classroom',pk=pk)
    return render(request, 'lab/question.html')

@login_required(login_url='/accounts/login')
def add_answer(request,pk):
    assignment_in = Assignment.objects.get(id=pk)
    form = add_answer_form()
    if request.method == 'POST':
        form = add_answer_form(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            answer_details = Answer(answer=answer,assignment=assignment_in,student=request.user)
            answer_details.save()
            return redirect('question',pk=pk)
    return render(request, 'lab/question.html',{'form':form})


@login_required(login_url='/accounts/login')
def create_poll(request,pk):
    assignment_in = Assignment.objects.get(id=pk)
    form = create_poll_form()
    if request.method == 'POST':
        form = create_poll_form(request.POST)
        if form.is_valid():
            option_1 = form.cleaned_data['option_1']
            option_2 = form.cleaned_data['option_2']
            option_3 = form.cleaned_data['option_3']
            option_4 = form.cleaned_data['option_4']
            option_5 = form.cleaned_data['option_5']
            poll = Poll(assignment_in=assignment_in,question=assignment_in.question,option_one=option_1,option_two=option_2,option_three=option_3,option_four=option_4,option_five=option_5)
            poll.save()
            return redirect('question',pk=pk)
    return render(request, 'lab/create_poll.html',{'form':form,'assignment':assignment_in})