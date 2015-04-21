# import logging
# log = logging.getLogger(__name__)

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from django_object_actions import (
    DjangoObjectActions,
    takes_instance_or_queryset,
)

from easy_select2 import select2_modelform

from .models import (
    Convention,
    Contest,
    District,
    Quartet,
    Chorus,
    Award,
    Performance,
    Singer,
    GroupMember,
    GroupAward,
    GroupFinish,
)


class GroupMemberInline(admin.TabularInline):
    form = select2_modelform(
        GroupMember,
        attrs={'width': '250px'},
    )
    model = GroupMember
    extra = 0


class GroupAwardInline(admin.TabularInline):
    form = select2_modelform(
        GroupAward,
        attrs={'width': '250px'},
    )
    model = GroupAward
    extra = 0


class GroupFinishInline(admin.TabularInline):
    form = select2_modelform(
        GroupFinish,
        attrs={'width': '250px'},
    )
    model = GroupFinish
    extra = 0


@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Convention,
        attrs={'width': '250px'},
    )
    save_on_top = True


@admin.register(Contest)
class ContestAdmin(DjangoObjectActions, admin.ModelAdmin):
    @takes_instance_or_queryset
    def import_scores(self, request, queryset):
        for obj in queryset:
            obj.import_scores()
    import_scores.label = 'Import Scores'
    form = select2_modelform(
        Contest,
        attrs={'width': '250px'},
    )
    save_on_top = True
    objectactions = [
        'import_scores',
    ]

    inlines = [
        GroupFinishInline,
    ]

    list_filter = (
        'kind',
        'year',
        'district',
    )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    form = select2_modelform(
        District,
        attrs={'width': '250px'},
    )
    save_on_top = True


QuartetForm = select2_modelform(
    Quartet,
    attrs={'width': '250px'},
)


@admin.register(Quartet)
class QuartetAdmin(admin.ModelAdmin):
    form = QuartetForm
    inlines = (
        GroupMemberInline,
        GroupFinishInline,
        # GroupAwardInline,
    )
    save_on_top = True


@admin.register(Chorus)
class ChorusAdmin(admin.ModelAdmin):
    def is_picture(self, obj):
        return bool(obj.picture)

    form = select2_modelform(
        Chorus,
        attrs={'width': '250px'},
    )

    list_display = (
        'name',
        'location',
        'website',
        'facebook',
        'twitter',
        'email',
        'phone',
        'director',
        'chapter_name',
        'chapter_code',
        'is_picture',
    )

    readonly_fields = (
        'is_picture',
    )

    # inlines = (
    #     GroupMemberInline,
    #     GroupAwardInline,
    # )
    save_on_top = True


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Chorus,
        attrs={'width': '250px'},
    )

    save_on_top = True


@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    form = select2_modelform(
        Performance,
        attrs={'width': '250px'},
    )
    list_display = (
        'group',
        'contest',
        'round',
        'place',
        'song1',
        'mus1',
        'prs1',
        'sng1',
        'song2',
        'mus2',
        'prs2',
        'sng2',
        'men',
    )

    list_filter = (
        'contest',
    )

    ordering = (
        'place',
    )

    save_on_top = True


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    fields = (
        'name',
    )

    form = select2_modelform(
        Singer,
        attrs={'width': '250px'},
    )
    save_on_top = True


# class CommonAdmin(admin.ModelAdmin):
#     list_display = [
#         'name',
#         'location',
#         'phone',
#         'twitter',
#         'picture',
#     ]

#     search_fields = ['name']
#     save_on_top = True
