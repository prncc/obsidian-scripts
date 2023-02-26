import glob
import os

import fire
import frontmatter
from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import IntPrompt

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
  choices = {
      'd': 'every (d)ay',
      'w': 'every (w)eek',
      'm': 'every (m)onth',
      'y': 'every (y)ear',
      's': '(s)paced...',
      'n': '(n)one',
  }
  displayed_choices = '/'.join(choices.values())
  choice = Prompt.ask(
      ('Add repeat field to metadata? '
       f'[bold purple]{displayed_choices}[/bold purple]'),
      default='n',
      choices=choices.keys(),
      show_choices=False,
  )
  if choice == 'n':
    return False
  if choice == 's':
    frequency = IntPrompt.ask('How many months between spaced intervals')
    repeat = f'spaced every {frequency} months'
  else:
    repeat = choices[choice].replace('(', '').replace(')', '')
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
    modified[maybe_add_repeat_to_note(console, note_path)] += 1
  console.print(f'Added repeat to {modified[True]} notes. '
                f'Kept {modified[False]} notes.')


if __name__ == '__main__':
  fire.Fire(add_repeat)