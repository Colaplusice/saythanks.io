# ☼  The 'Say Thanks' Project

forked

[![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)]()

## Spreading Thankfulness in Open Source™

[**saythanks.io**](https://saythanks.io/) will provide a button/link for use by open source projects, to
encourage users to send a simple *thank you* note to the creator (or creators)
of that project.

This simple button/link can be added to READMEs and project documentation.

The author can then enjoy a nice inbox (ideally) filled with very small,
thoughtful messages from the happy users of the software they enjoy to
toil over.

## Implementation Concepts

### ☤ The Basics

- Email when a new message of thankfulness is submitted (csrf enabled).
- Inbox page for each user/project with simple aggregation of messages (private).

### ☤ The Architecture

- Flask for API and Frontend, single application
- Auth0 for credential storage (in progress)
- Heroku for Hosting (done!)
- CloudFlare for SSL termination (done!)
- GitHub account creation, as well as passwordless email accounts

## Intended Collaborators

- Erin "The X" O'Connell (Python)
- Tom "The Pythonist" Baker (Javascript)
- Tom "Sea of Clouds" Matthews (Logo and Graphic Design)
- Kenneth "Your Name Here Instead, Idan?" Reitz (Frontend Design)

## Random Inspirational Links

- [Say Thanks for Package Control](https://packagecontrol.io/say_thanks)
- [Random 'Thanks' Issue on GH](https://github.com/foxmask/wallabag_api/issues/1)

## use babel

1. init_app and  make a babel.cfg
2. use babel syntax in jinjia template like `{{  _(' SayThanks.io') }}`
3. pybabel extract -F babel.cfg -k _l -o messages.pot.
collect translate item in workdir defined in babel.cfg
4. pybabel init -i messages.pot -d saythanks/translations -l zh
5. pybabel compile -d saythanks/translations

## if want to update

- pybabel extract -F babel.cfg -k _l -o messages.pot .
- pybabel update -i messages.pot -d saythanks/translations

## Oh, Thanks!

By the way... thank you! And if you'd like to [say thanks](https://saythanks.io/to/kennethreitz)... :)

✨🍰✨
