import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from Fydlyty2.game.models import Character, Dialogue, Scenario, Script


@login_required
def index(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))

@login_required
def game(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))

@login_required
def create_scenario(request, template_name):
    """

    """
    if request.method == 'POST':
        title = request.POST.get('title', '')
        bgimage = request.POST.get('bgimage', '')
        name = request.POST.get('name', '')
        gender = request.POST.get('gender', '')
        status = request.POST.get('status', '')
        normalimage = request.POST.get('normalimage', '')
        madimage = request.POST.get('madimage', '')
        angryimage = request.POST.get('angryimage', '')
        role = request.POST.get('role', '')
        context = request.POST.get('context', '')
        scene = request.POST.get('scene', '')
        gameplayer = request.POST.get('gameplayer', '')
        virtualcharacter = request.POST.get('virtualcharacter', '')
        csvfile = request.POST.get('script', '')

        scenario = Scenario.objects.create(title = title, background = bgimage, role = role)
        Character.objects.create(scenario = scenario, name = name, gender = gender, marital_status = status,
                                 image = normalimage, mood = 'N')
        Character.objects.create(scenario = scenario, name = name, gender = gender, marital_status = status,
                                 image = madimage, mood = 'M')
        Character.objects.create(scenario = scenario, name = name, gender = gender, marital_status = status,
                                 image = angryimage, mood = 'A')
        script = Script.objects.create(context = context, scene = scene)
        dialogue_script(csvfile, script, gameplayer, virtualcharacter)
        return render_to_response(template_name, context_instance=RequestContext(request))
    else:
        return render_to_response(template_name, context_instance=RequestContext(request))

def dialogue_script(file, script, gameplayer, virtualcharacter):
    """

    """
    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        parent = None
        for row in spamreader:
            string = ' '.join(row)
            character = string.split(',')[0]
            dialogue = string.split(',')[1]

            obj = Dialogue.objects.create(parent = parent, script = script, utterance = dialogue)
            if character == gameplayer:
                obj.character = 'GP'
            else:
                obj.character = 'VC'
            obj.save()
            parent = obj
    return 0