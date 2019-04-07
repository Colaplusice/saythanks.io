# ☼  The ‘Say Thanks’ Project（感谢有你）

## intro:

[origin readme](/readme_base.md)
forked [saythanks.io](https://github.com/kennethreitz/saythanks.io),在此基础上，修改了一些feature:

## feature:

- [x] flask & peewee & postgresql &docker-compose
- [x] flask-babel 支持中文和英文
- [x] 简单的用户注册和登录
- [x] 通过qq邮箱发送邮件

## use babel

1. init_app and  make a babel.cfg
2. use babel syntax in jinjia template like `{{  _(' SayThanks.io') }}`
3. pybabel extract -F babel.cfg -k _l -o messages.pot.
collect translate item in workdir defined in babel.cfg
4. pybabel init -i messages.pot -d saythanks/translations -l zh
5. pybabel compile -d saythanks/translations

### update

- pybabel extract -F babel.cfg -k _l -o messages.pot .
- pybabel update -i messages.pot -d saythanks/translations

