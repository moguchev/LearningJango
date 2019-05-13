from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from asker.models import Answer, Tag, Question, Profile, Like
from faker import Faker
from random import choice


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')

    if iteration == total:
        print()


pass


class Command(BaseCommand):
    fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument('--questions', type=int)
        parser.add_argument('--users', type=int)
        parser.add_argument('--tags', type=int)
        parser.add_argument('--answers', type=int)

    @transaction.atomic()
    def handle(self, *args, **options):
        users_cnt = options['users']
        questions_cnt = options['questions']
        tags_cnt = options['tags']
        answers_cnt = options['answers']

        if tags_cnt is not None:
            self.generate_tags(tags_cnt)

        if users_cnt is not None:
            self.generate_users(users_cnt)

        if questions_cnt is not None:
            self.generate_questions(questions_cnt)

        if answers_cnt is not None:
            self.generate_answers(answers_cnt)

    @classmethod
    def generate_tags(cls, tags_cnt):
        tags = []
        print_progress_bar(0, tags_cnt, prefix='Generate tags:', suffix='Complete', length=50)

        for i in range(tags_cnt):
            tag = Tag.objects.create(title=cls.fake.word())
            tag.save()
            tags.append(tag)
            print_progress_bar(i, tags_cnt, prefix='Generate tags:', suffix='Complete', length=50)

        print_progress_bar(tags_cnt, tags_cnt, prefix='Generate tags:', suffix='Complete', length=50)
        return tags

    @classmethod
    def generate_users(cls, users_cnt):
        users = []
        print_progress_bar(0, users_cnt, prefix='Generate users:', suffix='Complete', length=50)

        for i in range(users_cnt):
            u = User.objects.create_user(
                cls.fake.user_name(),
                email=cls.fake.email(),
                password='admin')
            Profile.objects.create(user=u)
            users.append(u)
            print_progress_bar(i, users_cnt, prefix='Generate users:', suffix='Complete', length=50)

        print_progress_bar(users_cnt, users_cnt, prefix='Generate users:', suffix='Complete', length=50)
        return users

    @classmethod
    def generate_questions(cls, questions_cnt):
        questions = []
        print_progress_bar(0, questions_cnt, prefix='Generate questions:', suffix='Complete', length=50)

        user_ids = list(
            Profile.objects.values_list('id', flat=True)
        )

        tags = list(
            Tag.objects.values_list('id', flat=True)
        )

        for i in range(questions_cnt):
            question = Question(
                author_id=choice(user_ids),
                title=cls.fake.sentence(),
                text='\n'.join(cls.fake.sentences(cls.fake.random_int(3, 6))),
                rating=cls.fake.random_int(0, 50),
            )
            question.save()
            for _ in range(cls.fake.random_int(2, 6)):
                Tag.objects.get(id=choice(tags)).question_set.add(question)
            question.save()
            questions.append(question)
            print_progress_bar(i, questions_cnt, prefix='Generate questions:', suffix='Complete', length=50)

        print_progress_bar(questions_cnt, questions_cnt, prefix='Generate questions:', suffix='Complete', length=50)
        return questions

    @classmethod
    def generate_answers(cls, answers_cnt):
        answers = []

        user_ids = list(
            Profile.objects.values_list('id', flat=True)
        )

        question_ids = list(
            Question.objects.values_list('id', flat=True)
        )

        print_progress_bar(0, len(question_ids), prefix='Generate answers:', suffix='Complete', length=50)
        for j in range(len(question_ids)):
            q_id = choice(question_ids)

            amount = cls.fake.random_int(0, answers_cnt)
            for i in range(amount):
                answer = Answer.objects.create(
                    question_id=q_id,
                    author_id=choice(user_ids),
                    text='\n'.join(cls.fake.sentences(cls.fake.random_int(2, 5))),
                    rating=cls.fake.random_int(0, 12),
                )
                answer.save()
                answers.append(answer)
            print_progress_bar(j, len(question_ids), prefix='Generate answers:', suffix='Complete', length=50)

        print_progress_bar(len(question_ids), len(question_ids), prefix='Generate answers:', suffix='Complete', length=50)
        return answers
