# Anno - simple, fast, local note-taking software

## Why use Anno?

There are many note-taking apps. How is Anno different? Anno is a local, web server-based user interface on top of [Markdown](https://daringfireball.net/projects/markdown/) files in a given directory. See a screenshot below. It makes writing, organizing, and searching through those files easy. That's it. There are many benefits to this approach:

- **Own your data.** Writing things down is an investment in your future. Rather than have your notes siloed by a company in a possibly proprietary text format, your data lives in plaintext files on your machine. If you use Anno for a while and then stop, no worries. Your data, Markdown files, is human-readable, easily portable to other tools, and convertable to other formats (see [Pandoc](https://pandoc.org/)).

- **Organize notes naturally.** Most note-taking apps create a new organizational system for your notes that is distinct from your filesystem. This forces you to store your notes separately from related files. Anno only works with `.anno.md` files in the current working directory, allowing you to organize your notes using your filesystem. Furthermore, all files with `labels` in the [YAML](https://yaml.org/)-style front matter can be viewed in their respective collections, making intra-directory organization easy without touching your underlying directory structure.

- **Use other software.** Anno adheres to the [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) of modular software that is simple, short, clear, and extensible. For example, data redundancy for text files is a solved problem, and Anno does not control users through product integration. Want cloud backups? Push to a git server or work out of a directory with file syncing. Want security? Encrypt the directory. Anno focuses on easy Markdown editing and organization.

- **Stay local, work fast.** Do you want to work on a plane or a train? Do you want a fast, simple user interface that isn't pinging a remote server or downloading large front-end interfaces? Anno is fast—it uses a small Flask server and one ~100 line JavaScript file—and can be used anywhere.


## What Anno supports

Anno provides a user interface for the most common and/or time-consuming text-editing operations. 

<img src='https://raw.githubusercontent.com/gwgundersen/anno/master/screenshots/editing.png?token=AAVQBIFJQMFJMLK4RFCCZ72576O7I'/>

Some basic functionality Anno support is:

- Previewing changes as you write.
- Writing equations using MathJax.
- Searching through files.
- Organizing notes in a directory with labels.
- Adding images to notes.
- Syncing Markdown front matter (title and date) into consistently formatted filenames.
- Converting notes into [LaTeX](https://www.latex-project.org/) PDFs for easy printing and sharing.
    
## Installation
