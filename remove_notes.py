import glob
import os

import fire
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Confirm


def read_file(note_path: str) -> str:
  with open(note_path, 'r') as f:
    return f.read()


def render_note(console: Console, markdown: str, note_name: str) -> None:
  console.clear()
  console.print(f'[bold red]{note_name}[/bold red]')
  console.print()
  console.print(Markdown(markdown))
  console.print('')  
  

def maybe_remove_note(
    console: Console,
    note_path: str,
    search_string: str,
) -> bool:
  markdown = read_file(note_path)
  if search_string not in markdown:
    return False
  note_name = os.path.basename(note_path)
  render_note(console, markdown, note_name)  
  really_delete = Confirm.ask(
      f'Really delete [bold red]{note_name}[/bold red]?')
  if really_delete:
    os.remove(note_path)
    return True


def remove_notes(search_string: str, directory: str = '~/Obsidian/Vault/Box'):
  directory = os.path.abspath(directory.replace('~', os.environ['HOME']))
  console = Console()
  deleted = {True: 0, False: 0}
  for note_path in glob.glob(f'{directory}/**.md'):
    deleted[maybe_remove_note(console, note_path, search_string)] += 1
  console.print(f'Deleted {deleted[True]} notes. Kept {deleted[False]} notes.')


if __name__ == '__main__':
  fire.Fire(remove_notes)