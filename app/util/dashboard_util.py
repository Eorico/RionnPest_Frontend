from util.table_util import TableDataHelper

class DashboardFormatter:

    @staticmethod
    def format_time(hrs, min):
        return f"{int(hrs):02d}:{int(min):02d}"

    @staticmethod
    def format_date(date, month, year):
        return f"{month}/{date}/{year}"

    @staticmethod
    def format_time_range(start, end, start_meridiem, end_meridiem):
        return f"[S]: {start} | {start_meridiem} - [E]: {end} | {end_meridiem}"

    @staticmethod
    def format_chemicals(data_list, is_actual=False):
        return TableDataHelper.fmt_chemicals(data_list, is_actual)  # delegate

    @staticmethod
    def format_remarks(record: dict) -> str:
        return TableDataHelper.fmt_remarks(record)  # delegate

    @staticmethod
    def format_record_time_range(record: dict) -> str:
        return TableDataHelper.fmt_time_range(record)  # delegate

    @staticmethod
    def format_record_date(record: dict) -> str:
        return TableDataHelper.fmt_date(record)  # delegate