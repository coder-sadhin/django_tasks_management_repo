from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task,Project
from django.db.models import Q,Count, Max, Min, Avg

# Create your views here.


def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


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


def create_task(request):
    # employees = Employee.objects.all()
    form = TaskModelForm()  # For GET

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():

            """ For Model Form Data """
            form.save()

            return render(request, 'task_form.html', {"form": form, "message": "task added successfully"})

            ''' For Django Form Data'''
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

    context = {"form": form}
    return render(request, "task_form.html", context)

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