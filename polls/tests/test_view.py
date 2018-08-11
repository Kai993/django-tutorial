import datetime

import os
import sys

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

# 上位の階層にあるモジュールをインポートできるように設定
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from polls.models import Question


def create_question(question_text, days):
    """
    与えられた`question_text`で質問を作成し、
    与えられた数の`days`オフセットを公開。
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(
               question_text=question_text,
               pub_date=time
           )


class QuestionIndexViewTest(TestCase):
    def test_質問が無い(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')

        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )

    def test_過去の質問(self):
        create_question(question_text='Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_将来の質問(self):
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )

    def test_将来と過去の質問(self):
        create_question(question_text='Past question.', days=-30)
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_2つの過去の質問(self):
        create_question(question_text='Past question 1.', days=-30)
        create_question(question_text='Past question 2.', days=-5)
        respons = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            respons.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTest(TestCase):
    def test_将来の質問(self):
        """
        将来の質問は404を返す
        """
        future_question = create_question('Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        print(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_過去の質問(self):
        """
        過去の質問はテキストが表示される
        """
        past_question = create_question(
            question_text='Past Question.',
            days=-5
        )
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
