from process import process


def summary(records):
    totals = process(records)
    return f"{len(totals)} records, total {sum(totals):.2f}"
