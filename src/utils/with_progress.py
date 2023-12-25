from rich.progress import Progress, SpinnerColumn, TextColumn


def with_progress(func, description="loading..."):
    def wrapper(*args, **kwargs):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description, total=None)
            result = func(*args, **kwargs)
            progress.stop()
            return result

    return wrapper
