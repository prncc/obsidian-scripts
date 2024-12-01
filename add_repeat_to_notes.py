import glob
import os

import fire
import frontmatter
from rich.console import Console
from rich.prompt import Prompt

from utils import read_note
from utils import render_note


def maybe_add_repeat_to_note(
    console: Console,
    note_path: str,
) -> bool:
  note = read_note(note_path)
  if 'repeat' in note.metadata:
    return False
  note_name = os.path.basename(note_path)
  render_note(console, note.content, note_name)
  choice = Prompt.ask(
      'Repeat frequency in weeks?',
      default='never',
  )
  if choice in ['never', 'n', '0']:
    repeat = 'never'
  else:
    repeat = f'spaced every {choice} weeks'
  note.metadata['repeat'] = repeat
  with open(note_path, 'wt') as f:
    f.write(frontmatter.dumps(note))
  return True


def add_repeat(directory: str = '~/Obsidian/Vault/Box'):
  """Add the repeat field to notes."""
  directory = os.path.abspath(directory.replace('~', os.environ['HOME']))
  console = Console()
  modified = {True: 0, False: 0}
  for note_path in glob.glob(f'{directory}/**.md'):
    try:
      modified[maybe_add_repeat_to_note(console, note_path)] += 1
    except KeyboardInterrupt:
      print()
      break
  console.print(f'Added the repeat field to {modified[True]} notes. '
                f'Skipped {modified[False]} already repeating notes.')


if __name__ == '__main__':
  fire.Fire(add_repeat)