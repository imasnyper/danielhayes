class FourDigitYearConverter:
    regex = '\d{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % int(value)


class TwoDigitMonthConverter:
    regex = '\d{2}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%02d' % int(value)
