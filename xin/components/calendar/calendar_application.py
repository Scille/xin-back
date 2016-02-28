#! /usr/bin/env python3

from autobahn_sync.core import AutobahnSync

from view import (create_calendar, list_calendar, get_calendar, modify_calendar, event_calendar_creation,
                  create_meeting, list_meetings, get_meeting, modify_meeting, event_meeting_creation, delete_meeting)

from mongoengine import connect
from mongoengine.connection import _get_db


class CalendarApplication():

    def __init__(self, config=None):
        if config:
            import json
            try:
                json_file = open(config)
                self.config = json.load(json_file)
                json_file.close()
            except IOError as e:
                e.strerror = 'Unable to load configuration file (%s)' % e.strerror
                raise
        else:
            self.config = {'CROSSBAR': 'ws://127.0.0.1:8080/ws',
                           'DATABASE':  {'URL': 'mongodb://localhost:27017/calendar', 'NAME': 'calendar'}}

    def start(self):
        self.wamp = AutobahnSync()
        wamp = self.wamp
        connect(self.config['DATABASE']['NAME'], host=self.config['DATABASE']['URL'])
        self.db = _get_db()

        @wamp.register('calendar.create')
        def calendar_create(name, users):
            calendar = create_calendar(name, users)
            return calendar

        @wamp.register('calendar.list')
        def calendar_list():
            return list_calendar()

        @wamp.register('calendar.retrieve')
        def calendar_get(calendar_id):
            return get_calendar(calendar_id)

        @wamp.register('calendar.modify')
        def calendar_modify(calendar_id, name=None, users=None, append=False):
            return modify_calendar(calendar_id, name, users, append)

        @wamp.register('meeting.create')
        def meeting_create(calendar_id, name, users, date_begin, duration=None, place=None, comment=None, tags=None):
            return create_meeting(calendar_id,
                                  name, users, date_begin, duration, place, comment, tags)

        @wamp.register('meeting.list')
        def meeting_list(calendar_id):
            return list_meetings(calendar_id)

        @wamp.register('meeting.retrieve')
        def meeting_get(meeting_id):
            return get_meeting(meeting_id)

        @wamp.register('meeting.modify')
        def meeting_modify(meeting_id, name=None, users=None, append=False, date_begin=None, duration=None, place=None, comment=None, tags=None):
            return modify_meeting(meeting_id, name, users, append, date_begin, duration, place, comment, tags)

        @wamp.register('meeting.delete')
        def meeting_delete(meeting_id):
            return delete_meeting(meeting_id)

        self.wamp = wamp
        self.wamp.run(url=self.config['CROSSBAR'], blocking=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Component calendar of Scille')
    parser.add_argument('--config', action='store_true', dest="config",
                        help='give a config file to the application ie do not use the default one')
    args = parser.parse_args()
    app = CalendarApplication(args.config)
    app.start()
