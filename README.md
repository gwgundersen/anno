Anno is a thin client over Markdown files for easy, local editing and organization.


# Motivation

There are many note-taking apps. Why use Anno?

- **Own your data.** Anno works on Markdown files that live on your machine. That's it. Rather than have your notes siloed by a company in possibly proprietary text formats, your data lives in human-readable text files wherever you like.

- **Work locally, backup as you like.** Anno is entirely local. It's just a thin client on files in a given directory. Want awesome cloud storage backup? Push to a git server, encrypt the directory and email it to yourself, whatever you like.

## Anno is opinionated

Anno supports the most time-consuming text-editing operations such as:

- Previewing Markdown and MathJax updates as you write.
- Syncing Markdown header information (title and date) into a consistently formatted filename.
- Organizing your notes based on labels (specified in the Markdown header).
- Converting notes into PDFs for easy printing and sharing.
- "Uploading" images (copying them into a local directory).

Anno is designed for technical people. This means there is no support for things you might occasionally do that you can do from the command line or your OS's file manager such as:

- No search. Use `grep`, `ack`, or your favorite text search tool.
- No interface for archived or trashed files. The data lives in a directory on your machine. Use your favorite shell or your OS's file manager.

# Installation
