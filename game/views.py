import csv, json, os, random, re, string

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from Fydlyty2.accounts.models import UserProfile
from Fydlyty2.game.models import Character, CTFile, Dialogue, Scenario, Script

from gtts import gTTS


@login_required
def index(request, template_name):
    """
    Render landing page for Fydlyty
    """
    return render_to_response(template_name, context_instance=RequestContext(request))

@login_required
def game(request, script_id, template_name):
    """
    Render both versions of the game (basic or complex)
    """
    try:
        script = Script.objects.get(id = script_id)
    except Script.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))

    scenario = Scenario.objects.get(script = script)

    parent_dialogue = Dialogue.objects.get(script = script, parent = None, character = 'VC')
    if parent_dialogue:
        game_player = Dialogue.objects.filter(script = script, parent = parent_dialogue)
    else:
        game_player = Dialogue.objects.filter(script = script, parent = None, character = 'GP')

    if scenario.type == 'B':
        normal_character = Character.objects.get(scenario = scenario, mood = 'N')

        data = {
            'scenario': scenario,
            'normal_character': normal_character,
            'script': script,
            'parent_dialogue': parent_dialogue,
            'game_player': game_player,
        }
    else:
        try:
            crazytalk = CTFile.objects.get(script = script, mood = 'N')
        except CTFile.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))

        project_path = "/" + crazytalk.script.scenario.title + "/" + crazytalk.mood + "/" + crazytalk.project.file.name.split("\\")[-1]
        idle_path = "/" + crazytalk.script.scenario.title + "/" + crazytalk.mood + "/" + crazytalk.idle.file.name.split("\\")[-1]
        vc_name = crazytalk.name
        vc_status = crazytalk.get_marital_status_display()
        vc_gender = crazytalk.get_gender_display()

        phrase = 'Hello game player! My name is ' + crazytalk.name + ' and I am the virtual character you will be playing fidelity with. You can read more about me in the right hand column. When ready press start game to proceed.'
        intro = gTTS(text=phrase, lang='en')
        intro_file = randomword(15)
        path_of_introfile = "Fydlyty2/media/audio/" + intro_file + ".mp3"
        intro.save(path_of_introfile)

        tts = gTTS(text=parent_dialogue.utterance, lang='en')
        filename = randomword(15)
        path_of_file = "Fydlyty2/media/audio/" + filename + ".mp3"
        tts.save(path_of_file)

        template_name = 'game/complex_game.html'

        data = {
            'scenario': scenario,
            'script': script,
            'parent_dialogue': parent_dialogue,
            'game_player': game_player,
            'project_path': project_path,
            'idle_path': idle_path,
            'filename': filename,
            'intro_file': intro_file,
            'name': vc_name,
            'gender': vc_gender,
            'marital_status': vc_status,
        }
    write_scenario(scenario = scenario, script = script, user = request.user,
                    parent_dialogue = parent_dialogue, game_player = game_player,
                    scenario_type = scenario.get_type_display(), type = 'N')
    return render_to_response(template_name, context_instance=RequestContext(request, data))

@login_required
def create_scenario(request, scenario_type, template_name):
    """
    Renders the create page for the scenario & handles
    POST requests.
    """
    if request.method == 'POST':
        title = request.POST.get('title', '')
        bgimage = request.FILES.get('bgimage', '')
        name = request.POST.get('name', '')
        role = request.POST.get('role', '')
        gender = request.POST.get('gender', '')
        status = request.POST.get('status', '')
        context = request.POST.get('context', '')
        scene = request.POST.get('scene', '')
        gameplayer = request.POST.get('gameplayer', '')
        virtualcharacter = request.POST.get('virtualcharacter', '')
        csvfile = handle_uploaded_file(request.FILES.get('script', ''))

        if scenario_type == '1':
            scenario = Scenario.objects.create(title = title, background = bgimage, role = role, type= 'B')
        else:
            scenario = Scenario.objects.create(title = title, background = bgimage, role = role, type= 'C')
        script = Script.objects.create(scenario = scenario, context = context, scene = scene)
        dialogue_script(csvfile, script, gameplayer, virtualcharacter)

        if scenario_type == '1':
            normalimage = request.FILES.get('normalimage', '')
            madimage = request.FILES.get('madimage', '')
            angryimage = request.FILES.get('angryimage', '')
            Character.objects.create(scenario = scenario, name = name, gender = gender, marital_status = status,
                                     image = normalimage, mood = 'N')
            Character.objects.create(scenario = scenario, name = name, gender = gender, marital_status = status,
                                     image = madimage, mood = 'M')
            Character.objects.create(scenario = scenario, name = name, gender = gender, marital_status = status,
                                     image = angryimage, mood = 'A')
            return HttpResponseRedirect(reverse('confirm_scenario', args=[scenario.id]))
        else:
            normalfile1 = request.FILES.get('normalfile1', '')
            normalfile2 = request.FILES.get('normalfile2', '')
            normalfile3 = request.FILES.get('normalfile3', '')
            normalfile4 = request.FILES.get('normalfile4', '')
            normalfile5 = request.FILES.get('normalfile5', '')
            ct_idle, ct_model, ct_motion, ct_project, ct_script = sort_files([normalfile1, normalfile2, normalfile3, normalfile4, normalfile5])
            CTFile.objects.create(script = script, name = name, gender = gender, marital_status = status, mood = 'N', idle = ct_idle, model = ct_model, motion = ct_motion, project = ct_project, ct_script = ct_script)

            madfile1 = request.FILES.get('madfile1', '')
            madfile2 = request.FILES.get('madfile2', '')
            madfile3 = request.FILES.get('madfile3', '')
            madfile4 = request.FILES.get('madfile4', '')
            madfile5 = request.FILES.get('madfile5', '')

            if madfile1 and madfile2 and madfile3 and madfile4 and madfile5:
                ct_idle, ct_model, ct_motion, ct_project, ct_script = sort_files([madfile1, madfile2, madfile3, madfile4, madfile5])
                CTFile.objects.create(script = script, name = name, gender = gender, marital_status = status,
                                        mood = 'M', idle = ct_idle, model = ct_model, motion = ct_motion,
                                        project = ct_project, ct_script = ct_script)

            angryfile1 = request.FILES.get('angryfile1', '')
            angryfile2 = request.FILES.get('angryfile2', '')
            angryfile3 = request.FILES.get('angryfile3', '')
            angryfile4 = request.FILES.get('angryfile4', '')
            angryfile5 = request.FILES.get('angryfile5', '')
            if angryfile1 and angryfile2 and angryfile3 and angryfile4 and angryfile5:
                ct_idle, ct_model, ct_motion, ct_project, ct_script = sort_files([angryfile1, angryfile2, angryfile3, angryfile4, angryfile5])
                CTFile.objects.create(script = script, name = name, gender = gender, marital_status = status,
                                        mood = 'A', idle = ct_idle, model = ct_model, motion = ct_motion,
                                        project = ct_project, ct_script = ct_script)
            return HttpResponseRedirect(reverse('confirm_scenario', args=[scenario.id]))
    else:
        return render_to_response(template_name, context_instance=RequestContext(request, {'scenario_type': scenario_type}))

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
def confirm_scenario(request, scenario_id, template_name):
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
            script = Script.objects.get(scenario = scenario)
        except Script.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))

        if scenario.type == 'B':
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

        else:
            try:
                crazytalk_normal = CTFile.objects.get(script = script, mood = 'N')
            except CTFile.DoesNotExist:
                return HttpResponseRedirect(reverse('index'))
            project_path_normal = "/" + crazytalk_normal.script.scenario.title + "/" + crazytalk_normal.mood + "/" + crazytalk_normal.project.file.name.split("\\")[-1]
            idle_path_normal = "/" + crazytalk_normal.script.scenario.title + "/" + crazytalk_normal.mood + "/" + crazytalk_normal.idle.file.name.split("\\")[-1]
            name = crazytalk_normal.name
            gender = crazytalk_normal.get_gender_display()
            marital_status = crazytalk_normal.get_marital_status_display()

            try:
                crazytalk_mad = CTFile.objects.get(script = script, mood = 'M')
            except CTFile.DoesNotExist:
                return HttpResponseRedirect(reverse('index'))
            project_path_mad = "/" + crazytalk_mad.script.scenario.title + "/" + crazytalk_mad.mood + "/" + crazytalk_mad.project.file.name.split("\\")[-1]
            idle_path_mad = "/" + crazytalk_mad.script.scenario.title + "/" + crazytalk_mad.mood + "/" + crazytalk_mad.idle.file.name.split("\\")[-1]

            try:
                crazytalk_angry = CTFile.objects.get(script = script, mood = 'A')
            except CTFile.DoesNotExist:
                return HttpResponseRedirect(reverse('index'))
            project_path_angry = "/" + crazytalk_angry.script.scenario.title + "/" + crazytalk_angry.mood + "/" + crazytalk_angry.project.file.name.split("\\")[-1]
            idle_path_angry = "/" + crazytalk_angry.script.scenario.title + "/" + crazytalk_angry.mood + "/" + crazytalk_angry.idle.file.name.split("\\")[-1]

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

        if scenario.type == 'B':
            data = {
                'character_normal': character_normal,
                'character_mad': character_mad,
                'character_angry': character_angry,
                'dialogues': dialogues,
                'scenario': scenario,
                'script': script,
            }
        else:
            data = {
                'name': name,
                'gender': gender,
                'marital_status': marital_status,
                'project_path_normal': project_path_normal,
                'idle_path_normal': idle_path_normal,
                'project_path_mad': project_path_mad,
                'idle_path_mad': idle_path_mad,
                'project_path_angry': project_path_angry,
                'idle_path_angry': idle_path_angry,
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
        'complex_scenarios': complex_scripts,
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
            write_scenario(user = request.user, scenario = dialogue.script.scenario, choice = dialogue, type = 'L', time_lapse = request.GET.get('time_lapse'))
            return HttpResponse(json.dumps({"status": False}))

        if vc:
            vc_dialogue = vc.utterance
        else:
            vc_dialogue = 'Nothing to say'

        if request.GET.get('type') == '1':
            character = Character.objects.get(scenario = dialogue.script.scenario, mood = dialogue.mood)
        else:
            crazytalk = CTFile.objects.get(script = dialogue.script, mood = dialogue.mood)
            project_path = "/" + crazytalk.script.scenario.title + "/" + crazytalk.mood + "/" + crazytalk.project.file.name.split("\\")[-1]
            idle_path = "/" + crazytalk.script.scenario.title + "/" + crazytalk.mood + "/" + crazytalk.idle.file.name.split("\\")[-1]
            background_path = crazytalk.script.scenario.background.url

            tts = gTTS(text=vc_dialogue, lang='en')
            filename = randomword(15)
            path_of_file = "Fydlyty2/media/audio/" + filename + ".mp3"
            tts.save(path_of_file)

        gp_dialogues = Dialogue.objects.filter(parent = vc).order_by('?')

        gp_list = []
        for gp in gp_dialogues:
            gp_list.append({'id': gp.id, 'utterance': gp.utterance})

        values = settings.HELP.get(dialogue.mood)
        help_text = random.choice(values)

        if request.GET.get('type') == '1':
            data = {"status": True, "vc_dialogue": vc_dialogue, "help_text": help_text,
                    "gp_dialogues": gp_list, "image": character.image.url}
        else:
            data = {"status": True, "vc_dialogue": vc_dialogue, "help_text": help_text,
                    "gp_dialogues": gp_list, "project_path": project_path,
                    "idle_path": idle_path, "filename": filename, "background_path": background_path,}
        write_scenario(user = request.user, scenario = dialogue.script.scenario,
                           parent_dialogue = vc, game_player = gp_dialogues, choice = dialogue, type = 'E', time_lapse = request.GET.get('time_lapse'))
        return HttpResponse(json.dumps(data))
    return HttpResponse(json.dumps({"status": False}))

@login_required
def debrief(request, script_id, template_name):
    """
    Read data from the debrif file and render on screen
    """
    try:
        script = Script.objects.get(id = script_id)
    except Script.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))

    scenario = Scenario.objects.get(script = script)
    scenario_type = scenario.type
    script_id = script.id
    attempt_number = 1
    while True:
        check_filename = "Fydlyty2/media/scenarios/" + str(request.user) + '_' + str(scenario) + '_' + str(attempt_number) + '.txt'
        if os.path.isfile(check_filename):
            filename = check_filename
            attempt_number += 1
        else:
            break
    with open(filename, 'r') as txtfile:
        attempt = txtfile.readlines()
    i = 0
    convo_list = []
    while True:
        if attempt[i].split(':')[0] == 'Scenario':
            scenario = attempt[i].split(':')[1]
            i+=1
        elif attempt[i].split(':')[0] == 'Script':
            script = attempt[i].split(':')[1]
            i+=1
        elif attempt[i].split(':')[0] == 'Game Type':
            game_type = attempt[i].split(':')[1]
            i+=1
        elif attempt[i].split(':')[0] == 'User':
            user = attempt[i].split(':')[1]
            i+=1
        elif attempt[i][0] == '-':
            try:
                attempt[i+1]
            except:
                break
            j = i + 1
            item = {}
            gp_list = []
            while True:
                if attempt[j][0] == '-':
                    item['GP'] = gp_list
                    convo_list.append(item)
                    i = j
                    break
                elif attempt[j].split(':')[0] == 'Time Lapse':
                    item['Time'] = attempt[j].split(':')[1]
                    j+=1
                elif attempt[j].split(':')[0] == 'VC':
                    item['VC'] = attempt[j].split(':')[1]
                    j+=1
                elif attempt[j].split(':')[0] == 'GP':
                    gp_list.append(attempt[j].split(':')[1])
                    j+=1
                elif attempt[j].split(':')[0] == 'Selection':
                    item['Selection'] = attempt[j].split(':')[1]
                    j+=1
                elif attempt[j].split(':')[0] == 'Character Mood':
                    item['CharacterMood'] = attempt[j].split(':')[1].strip()
                    j+=1
        else:
            i+=1
    data = {
        'script_id': script_id,
        'scenario': scenario,
        'script': script,
        'game_type': game_type,
        'user': user,
        'convo_list': convo_list,
        'scenario_type': scenario_type,
    }
    return render_to_response(template_name, context_instance=RequestContext(request, data))

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def sort_files(files):
    """
    Sort files into crazy talk categories;
    idle, model, motion, project, and script
    """
    ct_idle = ''
    ct_model = ''
    ct_motion = ''
    ct_project = ''
    ct_script = ''
    for file in files:
        file_type = file.name.split('.')[1]
        if file_type == 'uctidle':
            ct_idle = file
        elif file_type == 'uctmodel':
            ct_model = file
        elif file_type == 'uctmotion':
            ct_motion = file
        elif file_type == 'uctproject':
            ct_project = file
        elif file_type == 'uctscript':
            ct_script = file
    return ct_idle, ct_model, ct_motion, ct_project, ct_script

def write_scenario(scenario = None, script = None, user = None,
                    parent_dialogue = None, game_player = None,
                    choice = None, scenario_type = 'B', type = 'N', time_lapse = 0):

    attempt_number = 1
    while True:
        filename = "Fydlyty2/media/scenarios/" + str(user) + '_' + str(scenario) + '_' + str(attempt_number) + '.txt'
        if os.path.isfile(filename):
            with open(filename) as myfile:
                if 'THE END' in list(myfile)[-1]:
                    attempt_number += 1
                else:
                    break
        else:
            break
    with open(filename, 'a') as txtfile:
        if type == 'N':
            txtfile.write('Scenario: ')
            txtfile.write(str(scenario) + '     \n')
            txtfile.write('Script: ')
            txtfile.write(str(script) + '   \n')
            txtfile.write('Game Type: ')
            txtfile.write(str(scenario_type) + '    \n')
            txtfile.write('User: ')
            txtfile.write(str(user) + '     \n' + '------------------------------------------------------------------------------------------------------------------------------------------------------------------- \n')

            txtfile.write('Time Lapse: ')
            txtfile.write(str(time_lapse) + '    \n')
            txtfile.write(str(parent_dialogue) + '\n')
            for gp in game_player:
                txtfile.write(str(gp) + '\n')
        elif type == 'E':
            txtfile.write('Selection: ')
            txtfile.write(str(choice.utterance) + '\n')
            txtfile.write('Character Mood: ')
            txtfile.write(str(choice.get_mood_display()) + '\n' + '------------------------------------------------------------------------------------------------------------------------------------------------------------------- \n')

            txtfile.write('Time Lapse: ')
            txtfile.write(str(time_lapse) + '    \n')
            txtfile.write(str(parent_dialogue) + '\n')
            for gp in game_player:
                txtfile.write(str(gp) + '\n')
        elif type == 'L':
            txtfile.write('Selection: ')
            txtfile.write(str(choice.utterance) + '\n')
            txtfile.write('Character Mood: ')
            txtfile.write(str(choice.get_mood_display()) + '\n' + '---------------------------------------------------------------------------THE END---------------------------------------------------------------------------------- \n')
    return True