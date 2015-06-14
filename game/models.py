import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _


class Scenario( models.Model ):
    """
    The scenario is one instant of the game. It will consist of
    a background, character, script, and role of player in the game
    """
    title = models.CharField(max_length = 100)
    background = models.ImageField(_('background image'), upload_to = "Fydlyty2/media/BackgroundImages/")
    role = models.CharField(max_length = 50, blank = True, null = True)

    def __unicode__(self):
        return _("%s") % (self.title)

    class Meta:
        app_label = "game"
        verbose_name = "scenario"
        verbose_name_plural = "scenarios"


class Character( models.Model ):
    """
    The character will be an image which with a mood described with it
    It is related to a scenario
    """
    CHARACTER_MOOD_CHOICES = (
	    ('N', 'Normal'),
        ('M', 'Mad'),
        ('A', 'Angry'),
    )
    CHARACTER_GENDER_CHOICES = (
	    ('', ''),
        ('M', 'Male'),
        ('F', 'Female'),
    )
    CHARACTER_STATUS_CHOICES = (
	    ('N', 'I don\'t want to say'),
        ('S', 'Single'),
        ('R', 'In a relationship'),
        ('E', 'Engaged'),
        ('M', 'Married'),
        ('W', 'Widowed'),
        ('SP', 'Seperated'),
        ('D', 'Divorced'),
    )
    scenario = models.ForeignKey(Scenario)

    name = models.CharField(max_length = 50)
    gender = models.CharField(max_length = 2,
                                 choices = CHARACTER_GENDER_CHOICES,
                                 default = '')
    marital_status = models.CharField(max_length = 2,
                                 choices = CHARACTER_STATUS_CHOICES,
                                 default = '')
    image = models.ImageField(_('character image'), upload_to = "images/")
    mood = models.CharField(max_length = 2,
                                 choices = CHARACTER_MOOD_CHOICES,
                                 default = 'N')

    def __unicode__(self):
        return _("Character for %s with mood %s") % (self.scenario.title, self.mood)

    class Meta:
        app_label = "game"
        verbose_name = "character"
        verbose_name_plural = "characters"


class Script( models.Model ):
    """
    The script is related to a scenario, and will have brief description
    of the context and scene
    """
    scenario = models.ForeignKey(Scenario)

    context = models.TextField(_('context'), null = True, blank = True)
    scene = models.TextField(_('scene'), null = True, blank = True)

    def __unicode__(self):
        return _("Script for scenario %s") % (self.scenario.title)

    class Meta:
        app_label = "game"
        verbose_name = "script"
        verbose_name_plural = "scripts"


class Dialogue( models.Model ):
    """
    The dialogue which will have a recursive relationship with itself
    Parent with null is dialogue initiator
    Mood states how the patient feels with the utterance
    Mood is insignificant in doctor's dialogue
    """
    CHARACTER_MOOD_CHOICES = (
	    ('N', 'Normal'),
        ('M', 'Mad'),
        ('A', 'Angry'),
    )
    CHARACTER_CHOICES = (
        ('GP', 'Game Player'),
        ('VC', 'Virtual Character'),
    )
    parent = models.ForeignKey('self', blank = True, null = True)
    script = models.ForeignKey(Script)

    utterance = models.TextField()
    character = models.CharField(max_length = 2,
                                 choices = CHARACTER_CHOICES,
                                 default = 'GP')
    mood = models.CharField(max_length = 2,
                                 choices = CHARACTER_MOOD_CHOICES,
                                 blank = True, null = True,
                                 default = 'N')

    def __unicode__(self):
        return _("%s: %s") % (self.character, self.utterance)

    class Meta:
        app_label = "game"
        verbose_name = "dialogue"
        verbose_name_plural = "dialogues"

def get_upload_path(instance, filename):
    return os.path.join(settings.BASE_DIR, 'Fydlyty2/media/CrazyTalkFiles', instance.scenario.title, instance.dialogue.mood, filename)


class CTFile( models.Model ):
    """
    The CTFile is related to all the files from crazy talk. These files are
    represent the animated character on the screen
    """
    dialogue = models.ForeignKey(Dialogue)
    scenario = models.ForeignKey(Scenario)

    file1 = models.FileField(blank = True, upload_to = get_upload_path)
    file2 = models.FileField(blank = True, upload_to = get_upload_path)
    file3 = models.FileField(blank = True, upload_to = get_upload_path)
    file4 = models.FileField(blank = True, upload_to = get_upload_path)
    file5 = models.FileField(blank = True, upload_to = get_upload_path)

    def __unicode__(self):
        return _("Crazy Talk files for scenario %s") % (self.scenario.title)

    class Meta:
        app_label = "game"
        verbose_name = "crazy talk file"
        verbose_name_plural = "crazy talk files"