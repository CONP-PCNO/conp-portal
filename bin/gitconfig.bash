#!/usr/bin/env bash

# Safer pushes. Other values: nothing, matching, upstream, simple
git config --global push.default current

# colorize output (Git 1.5.5 or later)
git config --global color.ui auto

# and from 1.5.4 onwards, this will works:
git config --global color.interactive auto

# better colors for spotting whitespace
git config --global color.whitespace "red reverse"
git config --global color.diff.whitespace "red reverse"

# make meta info blue so it makes a nice visual separation in diffs
git config --global color.diff.meta "blue black bold"

# user-friendly paging of some commands which don't use the pager by default
# (other commands like "git log" already do)
# to override pass --no-pager or GIT_PAGER=cat
git config --global pager.status true
git config --global pager.show-branch true

# shortcut aliases
git config --global alias.st status
git config --global alias.ci commit
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.di diff

# View the current working tree status using the short format
git config --global alias.s "status -s"

# show last commit
git config --global alias.last "log -1 HEAD"

# unstage
git config --global alias.unstage "reset HEAD --"

# show difference between the HEAD and the index
git config --global alias.staged "diff --cached"

# Show verbose output about tags, branches or remotes
git config --global alias.tags "tag -l"
git config --global alias.branches "branch -a"
git config --global alias.remotes "remote -v"

# A better looking log
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

# List contributors with number of commits
git config --global alias.contributors "shortlog --summary --numbered"

# whitespace
git config --global merge.renormalize true
git config --global core.autocrlf input
git config --global core.pager 'less -x4' # Tab indent size 4 instead of 8

# Enable rerere functionality. http://git-scm.com/blog/2010/03/08/rerere.html
git config --global rerere.enabled true
