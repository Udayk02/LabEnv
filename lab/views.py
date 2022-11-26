from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import create_class_form,create_assignment_form,create_poll_form,add_answer_form,ParticipantsForm
from django.contrib.auth.models import User
from .models import ClassRoom,Assignment,Answer,Poll,Voter
from django.shortcuts import redirect
import datetime
import subprocess, sys

def submit_code(request,pk,id):
    assignment = Assignment.objects.get(id = pk)
    answers = assignment.answer_set.all()
    answer_count = len(answers)
    current_user = request.user
    current_id = str(assignment.id)
    current_file = "submissions/" + current_id + "_" + str(answer_count + 1)
    file_name = ""
    final_output = ""
    if(request.user==assignment.class_in.host):
        answer = Answer.objects.get(id=id)
        submission = open("submissions/" + answer.answer, "r")
        code = ""
        for i in submission:
            code += i
        return render(request, 'lab/compiler.html',{"final_output":final_output,"pk":pk,"assignment":assignment, "code": code}) 
        
    for answer in answers:
        if(request.user==answer.student):
            return render(request, 'lab/compiler.html',{"final_output":final_output,"pk":pk,"assignment":assignment}) 
    
    if request.method == "POST":
        print(current_file)
        code = ""
        input_text = ""
        print(request.POST)
        if len(request.POST["code1"]) > 0:
            code = str(request.POST["code1"])
            code = "\n".join(code.split("~"))
        if len(request.POST["code_input1"]) > 0:
            input_text = request.POST["code_input1"]
            input_text = "\n".join(input_text.split("~"))
        language = request.POST["language1"]
        with open("input.txt", "w") as input_file:
            input_file.write(input_text)
        sys.stdin = open("input.txt", "r")
        
        if (language == '50'):
            with open(current_file + ".c", "w") as code_file:
                code_file.write(code)
            file_name = str(assignment.id) + "_" + str(answer_count + 1) + ".c"
            try:
                output = subprocess.check_output(
                "gcc " + current_file + ".c -o c_code", stderr=subprocess.STDOUT, shell=True, timeout=3,
                universal_newlines=True, stdin=sys.stdin)
            except subprocess.CalledProcessError as exc:
                final_output = str(exc.returncode) + " " + exc.output
            else:
                try:
                    output = subprocess.check_output(
                    current_file, stderr=subprocess.STDOUT, shell=True, timeout=3,
                    universal_newlines=True, stdin=sys.stdin)
                except subprocess.CalledProcessError as exc:
                    final_output = str(exc.returncode) + " " + exc.output
                else:
                    final_output = output
        elif (language == '54'):
            with open(current_file + ".cpp", "w") as code_file:
                code_file.write(code)
            file_name = str(assignment.id) + "_" + str(answer_count + 1) + ".cpp"
                
            try:
                output = subprocess.check_output(
                "g++ " + current_file + ".cpp -o cpp_code", stderr=subprocess.STDOUT, shell=True, timeout=3,
                universal_newlines=True, stdin=sys.stdin)
            except subprocess.CalledProcessError as exc:
                final_output = str(exc.returncode) + " " + exc.output
            else:
                try:
                    output = subprocess.check_output(
                    current_file, stderr=subprocess.STDOUT, shell=True, timeout=3,
                    universal_newlines=True, stdin=sys.stdin)
                except subprocess.CalledProcessError as exc:
                    final_output = str(exc.returncode) + " " + exc.output
                else:
                    final_output = output
        elif (language == '62'):
            code = code.replace("Main", "J" + current_id + "_" + str(answer_count + 1))
            with open("J" + current_file + ".java", "w") as code_file:
                code_file.write(code)
            file_name = "J" + str(assignment.id) + "_" + str(answer_count + 1) + ".java"
            
            try:
                output = subprocess.check_output(
                "javac " + current_file + ".java", stderr=subprocess.STDOUT, shell=True, timeout=3,
                universal_newlines=True, stdin=sys.stdin)
            except subprocess.CalledProcessError as exc:
                final_output = str(exc.returncode) + " " + exc.output
            else:
                try:
                    output = subprocess.check_output(
                    "java " + current_file, stderr=subprocess.STDOUT, shell=True, timeout=3,
                    universal_newlines=True, stdin=sys.stdin)
                except subprocess.CalledProcessError as exc:
                    final_output = str(exc.returncode) + " " + exc.output
                else:
                    final_output = output
        elif (language == '71'):
            with open(current_file + ".py", "w") as code_file:
                code_file.write(code)
            file_name = str(assignment.id) + "_" + str(answer_count + 1) + ".py"
                
            try:
                output = subprocess.check_output(
                "python " + current_file + ".py", stderr=subprocess.STDOUT, shell=True, timeout=3,
                universal_newlines=True, stdin=sys.stdin)
            except subprocess.CalledProcessError as exc:
                final_output = str(exc.returncode) + " " + exc.output
            else:
                final_output = output
                
        answer_details = Answer(assignment = assignment, student = current_user, answer = file_name)
        answer_details.save()
            
    return render(request, 'lab/compiler.html',{"final_output":final_output,"pk":pk,"assignment":assignment})

def run_code(request,pk):
    assignment = Assignment.objects.get(id=pk)
    final_output = ""
    code = ""
    input_text = ""
    if request.method == "POST":
        print(request.POST)
        if len(request.POST["code"]) > 0:
            code = str(request.POST["code"])
            code = "\n".join(code.split("~"))
        if len(request.POST["code_input"]) > 0:
            input_text = request.POST["code_input"]
            input_text = "\n".join(input_text.split("~"))
        language = request.POST["language"]
        with open("input.txt", "w") as input_file:
            input_file.write(input_text)
        sys.stdin = open("input.txt", "r")
        
        if (language == '50'):
            with open("code.c", "w") as code_file:
                code_file.write(code)
            try:
                output = subprocess.check_output(
                "gcc " + "code" + ".c -o c_code", stderr=subprocess.STDOUT, shell=True, timeout=3,
                universal_newlines=True, stdin=sys.stdin)
            except subprocess.CalledProcessError as exc:
                final_output = str(exc.returncode) + " " + exc.output
            else:
                try:
                    output = subprocess.check_output(
                    "code", stderr=subprocess.STDOUT, shell=True, timeout=3,
                    universal_newlines=True, stdin=sys.stdin)
                except subprocess.CalledProcessError as exc:
                    final_output = str(exc.returncode) + " " + exc.output
                else:
                    final_output = output
        elif (language == '54'):
            with open("code.cpp", "w") as code_file:
                code_file.write(code)
            try:
                output = subprocess.check_output(
                "g++ " + "code" + ".cpp -o cpp_code", stderr=subprocess.STDOUT, shell=True, timeout=3,
                universal_newlines=True, stdin=sys.stdin)
            except subprocess.CalledProcessError as exc:
                final_output = str(exc.returncode) + " " + exc.output
            else:
                try:
                    output = subprocess.check_output(
                    "code", stderr=subprocess.STDOUT, shell=True, timeout=3,
                    universal_newlines=True, stdin=sys.stdin)
                except subprocess.CalledProcessError as exc:
                    final_output = str(exc.returncode) + " " + exc.output
                else:
                    final_output = output
        elif (language == '62'):
            with open("Main.java", "w") as code_file:
                code_file.write(code)
            try:
                output = subprocess.check_output(
                "javac " + "Main" + ".java", stderr=subprocess.STDOUT, shell=True, timeout=3,
                universal_newlines=True, stdin=sys.stdin)
            except subprocess.CalledProcessError as exc:
                final_output = str(exc.returncode) + " " + exc.output
            else:
                try:
                    output = subprocess.check_output(
                    "java Main", stderr=subprocess.STDOUT, shell=True, timeout=3,
                    universal_newlines=True, stdin=sys.stdin)
                except subprocess.CalledProcessError as exc:
                    final_output = str(exc.returncode) + " " + exc.output
                else:
                    final_output = output
        elif (language == '71'):
            with open("code.py", "w") as code_file:
                code_file.write(code)
            try:
                output = subprocess.check_output(
                "python " + "code" + ".py", stderr=subprocess.STDOUT, shell=True, timeout=3,
                universal_newlines=True, stdin=sys.stdin)
            except subprocess.CalledProcessError as exc:
                final_output = str(exc.returncode) + " " + exc.output
            else:
                final_output = output
        print(final_output)        
    return render(request, 'lab/compiler.html', {"final_output":final_output,"pk":pk,"assignment":assignment, "code": code})

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
    poll=None
    voters=[]
    if assignment.type == 'poll':
        poll = assignment.poll
        voters = poll.voter_set.all()
    if assignment.type == 'assignment':
        if(request.user==assignment.class_in.host):
            return render(request,'lab/question.html',{'assignment':assignment,'answers':answers})
        return redirect('compiler_run',pk=pk)
    form = add_answer_form()
    vote_list = []
    for voter in voters:
        vote_list.append(voter.voter)
    return render(request, 'lab/question.html',{'assignment':assignment,'form':form,'answers':answers,'poll':poll,"voters":vote_list})

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
        v = Voter(voter=request.user,poll=poll)
        v.save()
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
            if(option_1):
                poll.option_one_count=0
            if(option_2):
                poll.option_two_count=0
            if(option_3):
                poll.option_three_count=0
            if(option_4):
                poll.option_four_count=0
            if(option_5):
                poll.option_five_count=0
            poll.save()
            return redirect('question',pk=pk)
    return render(request, 'lab/create_poll.html',{'form':form,'assignment':assignment_in})