import datetime
import os

from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse

from schedule.forms import GlobalSplitDateTimeWidget
from schedule.models import Event, Rule, Occurrence
from schedule.periods import Period, Month, Day
from schedule.utils import EventListManager

class TestEventListManager(TestCase):
    def setUp(self):
        weekly = Rule(frequency = "WEEKLY")
        weekly.save()
        daily = Rule(frequency = "DAILY")
        daily.save()
        
        self.event1 = Event(**{
                'title': 'Weekly Event',
                'start': datetime.datetime(2009, 4, 1, 8, 0),
                'end': datetime.datetime(2009, 4, 1, 9, 0),
                'end_recurring_period' : datetime.datetime(2009, 10, 5, 0, 0),
                'rule': weekly,
               })
        self.event1.save()
        self.event2 = Event(**{
                'title': 'Recent Event',
                'start': datetime.datetime(2008, 1, 5, 9, 0),
                'end': datetime.datetime(2008, 1, 5, 10, 0),
                'end_recurring_period' : datetime.datetime(2008, 5, 5, 0, 0),
                'rule': daily
               })
        self.event2.save()
    
    def test_occurrences_after(self):
        eml = EventListManager([self.event1, self.event2])
        occurrences = eml.occurrences_after(datetime.datetime(2009,4,1,0,0))
        self.assertEqual(occurrences.next().event, self.event1)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event2)
        self.assertEqual(occurrences.next().event, self.event1)
