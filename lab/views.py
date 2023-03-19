from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import create_class_form,create_assignment_form,create_poll_form,add_answer_form,ParticipantsForm
from django.contrib.auth.models import User
from .models import ClassRoom,Assignment,Answer,Poll,Voter
from django.shortcuts import redirect
import datetime
import subprocess, sys
import pyrebase, shutil

time = datetime.datetime.now(datetime.timezone.utc)

config = {
"apiKey": "AIzaSyBLRcq902ZtRsZWkcFq1nA83kSKOOjPfuk",
"authDomain": "project1-b6dce.firebaseapp.com",
"databaseURL": "https://project1-b6dce.firebaseio.com",
"projectId": "project1-b6dce",
"storageBucket": "project1-b6dce.appspot.com",
"serviceAccount": {
  "type": "service_account",
  "project_id": "project1-b6dce",
  "private_key_id": "3d4df670b6e9991e8463e53602e4197d3b686292",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCx2tqUE14DgiNR\nddz8cXZCozM9JkOUcUp5gZo8EE2rLPA4b5Am8Y652bcN/zF4MM00wC4daFpBWKd4\nHdYIFYSe9zZmWWIjD/ai84OaXQHCuKkR6bABzYy+Sp/8gEsfgCQtx5UdVNs/APJ6\nJBI0pYqqA/pryEAi0PzDX1R2tqPb0Cp5vECK7SNCydKGFMnQI6HIVyNXMGTlravQ\n8+837xhL2Gn+4gmfrdYiZIFIynm2az1wAwvg1Di2Yr1QQcbw+ooVlpxMMb9h7zky\nMcg+c6oobBLg/0Pv68VWP8SZrOBG6uEnBNDgaOCGtzxfOu1U3FzqWj9JaUbala8w\nSVkQHAFxAgMBAAECggEABNPCknnLF6/Iyx12k8B1m/3ndl2rQGRpx835dG9h2EdG\nNtXqVPBB9i/fTMk0G8XBUBD2P3SVXIguNW+j30DMQm9FwfXjmL2GbWpMFFy5X0JZ\nTmPoE8hzLTgDyxvlThPRh4+O78adk8JwEloXx2eF0bL9cT70ZK2E6r2T4ov2+xCJ\n+WjrZ+DMzM1LB00vS/UOtbmfdJKqPVK/BVJhHmpiVeoy4HGUCAh2j8QcHKDMDTUG\nVRL9Kt03R5zdt6Z+LogFM2ws970t6oOpSd6i+07DZ21ML8oeLbBTDkjjEVdpgEOr\nrhF7ORIMBLhxu0pupDc1DvVDsXeVl5cVpuFrtu0bcQKBgQDgsFyeXirjnwgKka1F\nnWjpJA/sz5xULqEdVkvseSKeOfQ1K45pa9y0gK4zHT+Jakpzn8neEIbmA8JQxHb5\ndzsEldkvxmU6lBdNSv7+5xs9JB51DMydowiNjBi6p3lL+3KvDBmXm+fxHLE8Dtn6\n5tp39AoJLafJZa8C7wcZ/Q3uiQKBgQDKo7eq+7Af9lq4yxqvLJkFBfPttpZb6mUg\nZ9ElEGbVDpy+UmExp6NsOM4IsZ5XmKWxqAXogDDOUJhjjHIQNzEBiAh+og7qh0+V\nnitJuhy0OwAQBJViXICrKbBAyIDQ0wTHY5yjAZ0F5jueaeayE1vXe1J00yTAUaah\nCLklzWMBqQKBgGd8s1v50VU/hSuhByZ+Jrji9DbFNKKNS4XAnn2PGYO4+6KVqiUi\nGehFMHa4bPA0tY/ls8uE3y0H5DLhGk8yPEuTXRIlFbDSTp06ApKTDTeu8BxHReMB\nGUpgkW8+/Z4idSLstsjedQjXh0Y7LOjj9RG0o/6wOYyIOgBm6WVt6UHJAoGAWi8Y\nu9j93ou2fo2t145in7Cxifb73fZogU6S7wroqSOysKVbKk0wVybE02uxS8zc2T8t\nOfdrQTbvS0ajMQJPJh5ToYAgYVJNIgpdu5c/1Rp5Aaf4j+kZPpP0JDDX25g+hTqY\n6Jb8OjboC62YBWLGOhVhcirSLWFpZjvKor9Qs9kCgYEAu9BUAWKMD01EgCzgx/IR\nc8B9Jv2NwdseKRotiuWuL1/TLU1yns0D9vIxXJG3Ya4tv1e/2Uoa4t1DH/eRqe+o\nHhmUQ2OiLXzRmZCZSEaGOLRg50gYEC2O5VoPSbXmaCYS4+8KU0yJ83vIDVEk0/Ji\nsvGGzo22/zx4EVAV5yUQhGo=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-dsoll@project1-b6dce.iam.gserviceaccount.com",
  "client_id": "100367057146429045553",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-dsoll%40project1-b6dce.iam.gserviceaccount.com"
}
}

firebase_storage = pyrebase.initialize_app(config)
storage = firebase_storage.storage()

def submit_code(request,pk,id):
    assignment = Assignment.objects.get(id = pk)
    answers = assignment.answer_set.all()
    answer_count = len(answers)
    current_user = request.user
    current_id = str(assignment.id)
    current_file = "submissions/" + current_id + "_" + str(answer_count + 1)
    file_name = ""
    final_output = ""
    already_answered = answers.filter(student=request.user)
    
    if(request.user==assignment.class_in.host):
        if(id == '0'):
            return redirect('classroom', pk=assignment.class_in.id)
        answer = Answer.objects.get(id=id)

        all_files = storage.list_files()
        for file in all_files:
            if file.name == answer.answer:
                print(file.name)
                file.download_to_filename(file.name)
                shutil.move(answer.answer,'submissions/'+answer.answer)

        submission = open("submissions/" + answer.answer, "r")
        code = ""
        for i in submission:
            code += i

        return render(request, 'lab/compiler.html',{"final_output":final_output,"pk":pk,"assignment":assignment, "code": code,"already_answered":already_answered}) 
        
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
        global time
        session_time = answer_details.created_on - time
        answer_details.session_time = session_time
        time_list = str(answer_details.session_time).split(":")
        answer_details.session_time = time_list[0] + " Hours " + time_list[1] + " Minutes " + time_list[2].split(".")[0] + " Seconds"
        answer_details.save()
        
        storage.child(file_name).put("submissions\\" + file_name)
        
        print(session_time)

    return redirect('question',pk=assignment.id)
            

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
                    "c_code", stderr=subprocess.STDOUT, shell=True, timeout=3,
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
                    "cpp_code", stderr=subprocess.STDOUT, shell=True, timeout=3,
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
    print(User.objects.all())
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
        global time
        time = datetime.datetime.now(datetime.timezone.utc)
        print(time)
        answer = answers.filter(student=request.user)
        
        if(request.user==assignment.class_in.host):
            return render(request,'lab/question.html',{'assignment':assignment,'answers':answers})
        if(assignment.status == "completed"):
            return redirect('classroom', pk=assignment.class_in.id)
        final_output=""
        code=""
        return render(request,'lab/compiler.html',{"final_output":final_output,"pk":assignment.id,"assignment":assignment, "code": code})
    form = add_answer_form()
    vote_list = []
    for voter in voters:
        vote_list.append(voter.voter)
    return render(request, 'lab/question.html',{'assignment':assignment,'form':form,'answers':answers,'poll':poll,"voters":vote_list,"voters_":voters})

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


def delete_assignment(request,pk):
    assignment = Assignment.objects.get(id=pk)
    pk = assignment.class_in.id
    assignment.delete()
    return redirect('classroom',pk=pk)

def delete_class(request,pk):
    classroom = ClassRoom.objects.get(id=pk)
    classroom.delete()
    return redirect('home')