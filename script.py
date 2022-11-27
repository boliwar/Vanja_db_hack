import random
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation


def get_child(fio):
    try:
        child = Schoolkid.objects.filter(full_name__contains=fio).get()
        if child:
            print(f'Найден: {child.full_name}, {child.birthday} дата рождения')
            return child
    except Schoolkid.MultipleObjectsReturned:
        print(f'{fio} много значений,уточните запрос.')
    except Schoolkid.DoesNotExist:
        print(f'Не найден {fio}' )
    finally:
        return None


def fix_marks(schoolkid):
    marks = Mark.objects.filter(schoolkid=schoolkid, points__lte=3)
    for mark in marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in chastisements:
        chastisement.delete()


def create_commendation(schoolkid, title):
    praise = random.choice(('Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Великолепно!',
                            'Прекрасно!', 'Талантливо!', 'Я поражен!'))

    lessons = Lesson.objects.filter(year_of_study=schoolkid.year_of_study, group_letter=schoolkid.group_letter,
                                    subject__title=title)

    for lesson in lessons:
        commendation = Commendation.objects.filter(created=lesson.date, schoolkid=schoolkid, teacher=lesson.teacher)
        if commendation:
            continue

        Commendation.objects.create(text=praise,
                                    created=lesson.date,
                                    schoolkid=schoolkid,
                                    subject=lesson.subject,
                                    teacher=lesson.teacher,
                                    )
        break