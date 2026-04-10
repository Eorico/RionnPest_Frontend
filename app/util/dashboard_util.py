class DashboardFormatter:
    @staticmethod
    def format_time(hrs, min):
        return f"{int(hrs):02d}:{int(min):02d}"
    @staticmethod
    def format_date(date, month, year):
        return f"{month}/{date}/{year}"
    @staticmethod
    def format_time_range(start, end, meridiem):
        return f"[S]: {start} - [E]: {end} | {meridiem}"
    @staticmethod
    @staticmethod
    def format_chemicals(data_list, is_actual=False):
        if not isinstance(data_list, list):
            return "n/a"

        parts = []
        for item in data_list:
            name = (
                item.get('actual_chemicals_name')
                if is_actual else None
            )
            name = name or item.get('chemical_name') or item.get('chemicals_name') or "Unkown"
            qty = item.get('quantity', '0')
            parts.append(f"[C]: {name} - [Q]: {qty}")

        return "\n".join(parts)