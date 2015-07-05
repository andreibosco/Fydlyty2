import csv, json, random, re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from Fydlyty2.accounts.models import UserProfile
from Fydlyty2.game.models import Character, Dialogue, Scenario, Script


@login_required
def index(request, template_name):
    return render_to_response(template_name, context_instance=RequestContext(request))

@login_required
def game(request, script_id, template_name):
    """

    """
    try:
        script = Script.objects.get(id = script_id)
    except Script.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))

    scenario = Scenario.objects.get(script = script)
    normal_character = Character.objects.get(scenario = scenario, mood = 'N')
    parent_dialogue = Dialogue.objects.get(script = script, parent = None, character = 'VC')
    if parent_dialogue:
        game_player = Dialogue.objects.filter(script = script, parent = parent_dialogue)
    else:
        game_player = Dialogue.objects.filter(script = script, parent = None, character = 'GP')

    data = {
        'scenario': scenario,
        'normal_character': normal_character,
        'script': script,
        'parent_dialogue': parent_dialogue,
        'game_player': game_player,
    }
    return render_to_response(template_name, context_instance=RequestContext(request, data))

@login_required
def create_basic_scenario(request, template_name):
    """
    Renders the create page for the basic scenario.
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
        return HttpResponseRedirect(reverse('confirm_basic_scenario', args=[scenario.id]))
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

            obj = Dialogue.objects.create(parent = parent, script = script, utterance = dialogue, mood = 'N')
            if character == gameplayer:
                obj.character = 'GP'
                mad, angry = change_dialogue(dialogue)
                if mad:
                    Dialogue.objects.create(parent = parent, script = script, utterance = mad, mood = 'M')
                if angry:
                    Dialogue.objects.create(parent = parent, script = script, utterance = angry, mood = 'A')
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
def confirm_basic_scenario(request, scenario_id, template_name):
    """
    Renders the confirmation page with the information uploaded,
    and handles form submission for proposed dialogues
    """
    if request.method == 'POST':
        for key, value in request.POST.iteritems():
            if key == 'csrfmiddlewaretoken':
                continue
            if not value:
                continue
            if len(key.split('_')) == 2:
                mood_type = key.split('_')[0]
                parent_id = key.split('_')[1]
            try:
                parent = Dialogue.objects.get(id = parent_id)
            except Dialogue.DoesNotExit:
                continue

            dialogue, created = Dialogue.objects.get_or_create(script = parent.script, mood = mood_type, parent = parent, character = 'GP')
            dialogue.utterance = value
            dialogue.save()

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

        try:
            parent_dialogue = Dialogue.objects.filter(script = script, parent = None)[0]
        except Dialogue.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))

        dialogues = [
            {'N': parent_dialogue}
        ]
        temp_dic = {}
        while True:
            next = Dialogue.objects.filter(script = script, parent = parent_dialogue)
            for obj in next:
                temp_dic[obj.mood] = obj
            if next:
                dialogues.append(temp_dic)
                temp_dic = {}
            try:
                parent_dialogue = next.get(mood = 'N')
            except Dialogue.DoesNotExist:
                parent_dialogue = None
            if parent_dialogue == None:
                break

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
    Show list of basic & complex scenarios
    """
    profile = UserProfile.objects.get(user = request.user)
    basic_scripts = Script.objects.filter(scenario__type = 'B').order_by('-id')
    complex_scripts = Script.objects.filter(scenario__type = 'C').order_by('-id')
    data = {
        'profile': profile,
        'basic_scenarios': basic_scripts,
        'complex_scripts': complex_scripts,
    }
    return render_to_response(template_name, context_instance=RequestContext(request, data))

def change_dialogue(dialogue):
    """
    The function takes a normal dialogue and changes it
    into forms of mad and angry
    """
    mad = None
    angry = None
    for key in settings.LANGUAGE:
        if key.lower() in dialogue.lower():
            values = settings.LANGUAGE.get(key)
            replace_with = random.choice(values)
            insensitive_key = re.compile(re.escape(key), re.IGNORECASE)
            if mad == None:
                mad = insensitive_key.sub(replace_with, dialogue)
                last_change = replace_with
                dialogue = mad
            elif replace_with != last_change:
                angry = insensitive_key.sub(replace_with, dialogue)
    return mad, angry

@login_required
def get_dialogues(request):
    """
    Get dialogue for Game player and Virtual Character
    """
    if request.is_ajax() and request.method == 'GET':
        try:
            dialogue = Dialogue.objects.get(id = request.GET.get('id'))
        except Dialogue.DoesNotExist:
            return HttpResponse(json.dumps({"status": False}))

        normal_parent = Dialogue.objects.filter(parent = dialogue.parent, mood = 'N')

        try:
            vc = Dialogue.objects.get(parent = normal_parent)
        except Dialogue.DoesNotExist:
            return HttpResponse(json.dumps({"status": False}))
        character = Character.objects.get(scenario = dialogue.script.scenario, mood = dialogue.mood)
        if vc:
            vc_dialogue = vc.utterance
        else:
            vc_dialogue = 'Nothing to say'

        gp_dialogues = Dialogue.objects.filter(parent = vc).order_by('?')

        gp_list = []
        for gp in gp_dialogues:
            gp_list.append({'id': gp.id, 'utterance': gp.utterance})

        values = settings.HELP.get(dialogue.mood)
        help_text = random.choice(values)
        return HttpResponse(json.dumps({"status": True, "image": character.image.url, "vc_dialogue": vc_dialogue,
                                        "help_text": help_text, "gp_dialogues": gp_list}))
    return HttpResponse(json.dumps({"status": False}))

@login_required
def debrief(request, script_id, template_name):
    """

    """
    return render_to_response(template_name, context_instance=RequestContext(request))

@login_required
def create_complex_scenario(request, scenario_id, template_name):
    """
    Renders the create page for the complex scenario.
    """
    return 0

@login_required
def confirm_complex_scenario(request, scenario_id, template_name):
    """
    Renders the confirmation page with the information uploaded,
    and handles form submission for proposed dialogues
    """
    return 0