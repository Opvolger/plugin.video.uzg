from datetime import datetime, tzinfo, timedelta
import time


class AmsterdamZone(tzinfo):
    def __init__(self, date):
        self.offset = +1
        self.isdst = False
        # omdat ik niet gebruik wil maken van externe lib's, zomer/wintertijd uitgeprogrammeerd.
        if self.dateitem('2007-03-25 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2007-10-28 02:00:00'):
            self.isdst = True
        if self.dateitem('2008-03-30 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2008-10-26 02:00:00'):
            self.isdst = True
        if self.dateitem('2009-03-29 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2009-10-25 02:00:00'):
            self.isdst = True
        if self.dateitem('2010-03-28 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2010-10-31 02:00:00'):
            self.isdst = True
        if self.dateitem('2011-03-27 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2011-10-30 02:00:00'):
            self.isdst = True
        if self.dateitem('2012-03-25 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2012-10-28 02:00:00'):
            self.isdst = True
        if self.dateitem('2013-03-31 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2013-10-27 02:00:00'):
            self.isdst = True
        if self.dateitem('2014-03-30 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2014-10-26 02:00:00'):
            self.isdst = True
        if self.dateitem('2015-03-29 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2015-10-25 02:00:00'):
            self.isdst = True
        if self.dateitem('2016-03-27 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2016-10-30 02:00:00'):
            self.isdst = True
        if self.dateitem('2017-03-26 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2017-10-29 02:00:00'):
            self.isdst = True
        if self.dateitem('2018-03-25 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2018-10-28 02:00:00'):
            self.isdst = True
        if self.dateitem('2019-03-31 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2019-10-27 02:00:00'):
            self.isdst = True
        if self.dateitem('2020-03-29 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2020-10-25 02:00:00'):
            self.isdst = True
        if self.dateitem('2021-03-28 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2021-10-31 02:00:00'):
            self.isdst = True
        if self.dateitem('2022-03-27 02:00:00') < date.replace(tzinfo=None) < self.dateitem('2022-10-30 02:00:00'):
            self.isdst = True
        # Hier zal de zomer en wintertijd wel zijn afgeschaft :)
        self.name = 'Europe/Amsterdam'

    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)

    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)

    def tzname(self, dt):
        return self.name

    def dateitem(self, datumstring):
        try:
            datetimevalue = datetime.strptime(datumstring, "%Y-%m-%d %H:%M:%S")
        except TypeError:
            datetimevalue = datetime(
                *(time.strptime(datumstring, "%Y-%m-%d %H:%M:%S")[0:6]))
        return datetimevalue
