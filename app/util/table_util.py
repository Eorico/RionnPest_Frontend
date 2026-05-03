class TableDataHelper:

    @staticmethod
    def fmt_chemicals(data_list, is_actual=False):
        if not isinstance(data_list, list):
            return "n/a"
        parts = []
        for item in data_list:
            name   = item.get('actual_chemicals_name') if is_actual else None
            name   = name or item.get('chemical_name') or "Unknown"
            qty    = item.get('quantity') or '0'
            prefix = "[A.C.U]" if is_actual else "[C]"
            remarks = (item.get('remarks') or '').strip()
            line   = f"{prefix}: {name} - [Q]: {qty}"
            if remarks:
                line += f" | [R]: {remarks}"
            parts.append(line)
        return "\n".join(parts) if parts else "n/a"

    @staticmethod
    def fmt_remarks(record: dict) -> str:
        chem_remarks   = [f"[C.U]: {c.get('remarks')}"   for c in (record.get('chemicals_use') or [])         if (c.get('remarks') or '').strip()]
        actual_remarks = [f"[A.C.U]: {c.get('remarks')}" for c in (record.get('actual_chemicals_used') or [])  if (c.get('remarks') or '').strip()]
        all_remarks    = chem_remarks + actual_remarks
        return "\n".join(all_remarks) if all_remarks else "n/a"

    @staticmethod
    def fmt_time_range(record: dict) -> str:
        return (
            f"[S]: {record.get('start_time','n/a')} {record.get('start_meridiem','')}"
            f" - [E]: {record.get('end_time','n/a')} {record.get('end_meridiem','')}"
        )

    @staticmethod
    def fmt_date(record: dict) -> str:
        return f"{record.get('month')}/{record.get('date')}/{record.get('year')}"

    @staticmethod
    def get_chemicals(record: dict) -> list:
        return record.get('chemicals_use') or record.get('chemical_use') or []

    @staticmethod
    def get_actual_chemicals(record: dict) -> list:
        return record.get('actual_chemicals_used') or record.get('actual_chemical_used') or []