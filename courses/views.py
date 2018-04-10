from courses.models import Course, Section, Question, UserAnswer
from courses.forms import CourseForm
from django.db import transaction
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied, SuspiciousOperation

def course_detail(request, course_id):
    course = Course.objects.get(pk=course_id)
    # course = get_object_or_404(Course, pk=course_id)
    return render(request, 'courses/course_detail.html', {
        'course': course,
    })


def course_list(request):
    courses = Course.objects.prefetch_related('students')
    return render(request, 'courses/course_list.html', {
        'courses': courses,
    })


def course_add(request):
    if request.POST:
        form = CourseForm(request.POST)
        if form.is_valid():
            new_course = form.save()
            return HttpResponseRedirect(new_course.get_absolute_url())
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {
        'form': form,
    })

def do_section(request, section_id):
        section = Section.objects.get(id=section_id)
        return render(request, 'courses/do_section.html', {
            'section': section,
        })

    # pretty much a default-ish way to post data.
    # packing up all the database access stuff into perform_test() keeps this
    # function cleaner by only handling authentication logic, while
    # the other function accesses database logic
def do_test(request, section_id):
    # check if the user is logged in, reject, which will result in a http error 403
    if not request.user.is_authenticated:
        raise PermissionDenied

    section = Section.objects.get(id=section_id)
    if request.method == 'POST':
        data = {}
        for key, value in request.POST.items():
            if key == 'csrfmiddlewaretoken':
                continue

            # prepare db logic inputs
            question_id = key.split('-')[1]
            answer_id = request.POST.get(key)
            data[question_id] = answer_id
        # pass inputs into db logic
        perform_test(request.user, data, section)

        return redirect(reverse('show_results', args=(section_id,)))
    return render(request, 'courses/do_test.html', {
        'section': section
    })
def perform_test(user, data, section):
    # DB LOGIC ONLY
    # performs queries from the database as needed and stores query results in the database
    with transaction.atomic():
        UserAnswer.objects.filter(user=user,
                                  question__section=section).delete()
        for question_id, answer_id in data.items():
            question = Question.objects.get(id=question_id)
            answer_id = int(answer_id)
            if answer_id not in question.answer_set.values_list('id', flat=True):
                raise SuspiciousOperation('Answer is not valid for this question')
            user_answer = UserAnswer.objects.create(
                user=user,
                question=question,
                answer_id=answer_id
            )
def calculate_score(user, section):
    questions = Question.objects.filter(section=section)
    correct_answers = UserAnswer.objects.filter(
        user=user,
        question__section=section,
        answer__correct=True
    )
    try:
        return (correct_answers.count() / questions.count()) * 100
    except:
        return 'not taken'

def show_results(request, section_id):
    if not request.user.is_authenticated:
        raise PermissionDenied
    section = Section.objects.get(id=section_id)
    return render(request, 'courses/show_results.html', {
        'section': section,
        'score': calculate_score(request.user, section)
    })
