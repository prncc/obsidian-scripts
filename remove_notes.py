import glob
import os

import fire
from rich.console import Console
from rich.prompt import Confirm

from utils import read_note
from utils import render_note


def maybe_remove_note(
    console: Console,
    note_path: str,
    search_string: str,
) -> bool:
  markdown = read_note(note_path).content
  if search_string not in markdown:
    return False
  note_name = os.path.basename(note_path)
  render_note(console, markdown, note_name)
  really_delete = Confirm.ask(
      f'Really delete [bold red]{note_name}[/bold red]?')
  if really_delete:
    os.remove(note_path)
    return True
  return False


def remove_notes(search_string: str, directory: str = '~/Obsidian/Vault/Box'):
  """Remove notes that contain search_string.

  You'll be asked whether to remove each note containing the string you
  specified.
  """
  directory = os.path.abspath(directory.replace('~', os.environ['HOME']))
  console = Console()
  deleted = {True: 0, False: 0}
  for note_path in glob.glob(f'{directory}/**.md'):
    deleted[maybe_remove_note(console, note_path, search_string)] += 1
  console.print(f'Deleted {deleted[True]} notes. Kept {deleted[False]} notes.')


if __name__ == '__main__':
  fire.Fire(remove_notes)