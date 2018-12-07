from django.contrib import admin

from Fydlyty2.game.models import Character, CTFile, Dialogue, Scenario, Script


class CharacterAdmin(admin.ModelAdmin):
    pass


class CTFileAdmin(admin.ModelAdmin):
    pass


class DialogueAdmin(admin.ModelAdmin):
    pass


class ScenarioAdmin(admin.ModelAdmin):
    pass


class ScriptAdmin(admin.ModelAdmin):
    pass

admin.site.register(Character, CharacterAdmin)
admin.site.register(CTFile, CTFileAdmin)
admin.site.register(Dialogue, DialogueAdmin)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(Script, ScriptAdmin)