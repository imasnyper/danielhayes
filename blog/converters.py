class FourDigitYearConverter:
    regex = '\d{4}'

    @staticmethod
    def to_python(value):
        return int(value)

    @staticmethod
    def to_url(value):
        return '%04d' % int(value)


class TwoDigitMonthConverter:
    regex = '\d{2}'

    @staticmethod
    def to_python(value):
        return int(value)

    @staticmethod
    def to_url(value):
        return '%02d' % int(value)
