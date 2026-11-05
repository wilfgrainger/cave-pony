from utils import page


def show(lines, n, size=5):
    # page() returns one too many, trim it here
    return "\n".join(page(lines, n, size)[:-1])
