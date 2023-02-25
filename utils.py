import frontmatter
from rich.console import Console
from rich.markdown import Markdown


def read_note(note_path: str) -> frontmatter.Post:
  with open(note_path, 'r') as f:
    return frontmatter.loads(f.read())


def render_note(console: Console, markdown: str, note_name: str) -> None:
  console.clear()
  console.print(f'[bold red]{note_name}[/bold red]')
  console.print()
  console.print(Markdown(markdown))
  console.print('')