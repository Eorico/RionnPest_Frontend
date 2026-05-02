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

            prefix = "[A.C.U]" if is_actual else "[C]"
            
            line = f"{prefix}: {name} - [Q]: {qty}"
            parts.append(line)

        return "\n".join(parts) if parts else "n/a"