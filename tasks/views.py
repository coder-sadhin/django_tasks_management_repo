from django.contrib import messages
from django.shortcuts import render,redirect
from tasks.forms import TaskDetailModelForm, TaskModelForm
from tasks.models import Employee, Task,Project
from django.db.models import Q,Count, Max, Min, Avg

# Create your views here.


def manager_dashboard(request):
    # tasks= Task.objects.all()
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status="COMPLETED").count()
    # in_progress_task = Task.objects.filter(status='IN_PROGRESS').count()
    # pending_task = Task.objects.filter(status="PENDING").count()

    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING')),
    )

    # tasks= Task.objects.select_related('details').prefetch_related('assigned_to').all()
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status="COMPLETED").count()
    # in_progress_task = Task.objects.filter(status='IN_PROGRESS').count()
    # pending_task = Task.objects.filter(status="PENDING").count()

    # Retriving task data
    type=request.GET.get('type','all')

    base_query = Task.objects.select_related(
        'details').prefetch_related('assigned_to')

    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()

    context={
        'tasks':tasks,
        'counts':counts
        # 'total_task':total_task,
        # 'completed_task':completed_task,
        # 'in_progress_task':in_progress_task,
        # 'pending_task':pending_task
    }


    return render(request, "dashboard/manager-dashboard.html",context)


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def test(request):
    names = ["Mahmud", "Ahamed", "John", "Mr. X"]
    count = 0
    for name in names:
        count += 1
    context = {
        "names": names,
        "age": 23,
        "count": count
    }
    return render(request, 'test.html', context)


# def create_task(request):
    # employees = Employee.objects.all()
    # form = TaskModelForm()  # For GET

    # if request.method == "POST":
    #     form = TaskModelForm(request.POST)
    #     if form.is_valid():

            # """ For Model Form Data """
            # form.save()

            # return render(request, 'task_form.html', {"form": form, "message": "task added successfully"})

            # ''' For Django Form Data'''
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')  # list [1,3]

            # task = Task.objects.create(
            #     title=title, description=description, due_date=due_date)

            # # Assign employee to tasks
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)

            # return HttpResponse("Task Added successfully")

    # context = {"form": form}
    # return render(request, "task_form.html", context)

def create_task(request):
    # employees = Employee.objects.all()
    task_form = TaskModelForm()  # For GET
    task_detail_form = TaskDetailModelForm()

    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Created Successfully")
            return redirect('create-task')

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)


# update tasks
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task)  # For GET

    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)

    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(
            request.POST, instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():

            """ For Model Form Data """
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update-task', id)

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)

# delete tasks
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager_dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('manager_dashboard')

def view_task(request):
    # tasks= Task.objects.all()
    # padding_task=Task.objects.filter(status="PENDING")
    # single_task=Task.objects.frist()
    # task3=Task.objects.get(id=3)

    # using exclude
    # tasks= TaskDetail.objects.exclude(priority="L")

    # for using or condition
    # tasks=Task.objects.filter(Q(status="PENDING") | Q(status="IN-PROGRESS"))
    
    # USING SELECT RELETED TO JOIN DATA
    # tasks= Task.objects.select_related('details').all()
    # tasks=Task.objects.select_related('task').all() from details to task

    # using foregnkey
    # tasks=Task.objects.select_related("project").all()

    """ prefetch_releted (reverse Foreignkey, manytomany)"""
    # this is for foreignkey
    # tasks = Project.objects.prefetch_related('task_set').all()

    # for manytomany
    # tasks = Task.objects.prefetch_related('assigned_to').all()


    # use aggregate
    # task_count= Task.objects.aggregate(num_task=Count('id'))

    # using annotate
    projects = Project.objects.annotate(
        num_task=Count('task')).order_by('num_task')
    return render(request, "show_task.html", {"projects": projects})