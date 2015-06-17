import csv

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
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
        bgimage = request.FILES.get('bgimage', '')
        name = request.POST.get('name', '')
        role = request.POST.get('role', '')
        gender = request.POST.get('gender', '')
        status = request.POST.get('status', '')
        normalimage = request.FILES.get('normalimage', '')
        madimage = request.FILES.get('madimage', '')
        angryimage = request.FILES.get('angryimage', '')
        context = request.POST.get('context', '')
        scene = request.POST.get('scene', '')
        gameplayer = request.POST.get('gameplayer', '')
        virtualcharacter = request.POST.get('virtualcharacter', '')
        csvfile = handle_uploaded_file(request.FILES.get('script', ''))

        scenario = Scenario.objects.create(title = title, background = bgimage, role = role)
        Character.objects.create(scenario = scenario, name = name, gender = gender, marital_status = status,
                                 image = normalimage, mood = 'N')
        Character.objects.create(scenario = scenario, name = name, gender = gender, marital_status = status,
                                 image = madimage, mood = 'M')
        Character.objects.create(scenario = scenario, name = name, gender = gender, marital_status = status,
                                 image = angryimage, mood = 'A')
        script = Script.objects.create(scenario = scenario, context = context, scene = scene)

        dialogue_script(csvfile, script, gameplayer, virtualcharacter)
        return HttpResponseRedirect(reverse('confirm_scenario', args=[scenario.id]))
    else:
        return render_to_response(template_name, context_instance=RequestContext(request))

def dialogue_script(file, script, gameplayer, virtualcharacter):
    """
    Read data from a temporary static location
    and save in database
    """
    with open(settings.TEMP_SCRIPT, 'rb') as csvfile:
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

def handle_uploaded_file(file):
    """
    Save data from the dialogue script to
    a temporary file in staticfiles
    """
    destination = open(settings.TEMP_SCRIPT, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    return True

@login_required
def confirm_scenario(request, scenario_id, template_name):
    """
    Renders the confirmation page with the information uploaded,
    and handles form submission for proposed dialogues
    """
    if request.method == 'POST':
        for key, value in request.POST.iteritems():
            print key, value
        return HttpResponseRedirect(reverse('scenarios_list'))

    else:
        try:
            scenario = Scenario.objects.get(id = scenario_id)
        except Scenario.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))

        try:
            character_normal = Character.objects.get(scenario = scenario, mood = 'N')
        except Character.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))

        try:
            character_mad = Character.objects.get(scenario = scenario, mood = 'M')
        except Character.DoesNotExist:
            character_mad = None

        try:
            character_angry = Character.objects.get(scenario = scenario, mood = 'A')
        except Character.DoesNotExist:
            character_angry = None

        try:
            script = Script.objects.get(scenario = scenario)
        except Script.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))

        dialogues = Dialogue.objects.filter(script = script)

        data = {
            'character_normal': character_normal,
            'character_mad': character_mad,
            'character_angry': character_angry,
            'dialogues': dialogues,
            'scenario': scenario,
            'script': script,
        }
        return render_to_response(template_name, context_instance=RequestContext(request, data))

@login_required
def scenarios_list(request, template_name):
    """

    """
    scenarios = Scenario.objects.all()
    data = {
        'basic_scenarios': scenarios,
    }
    return render_to_response(template_name, context_instance=RequestContext(request, data))