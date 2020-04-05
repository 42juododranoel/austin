Этот репозиторий — тестовое задание, которое я писал для одной компании, не буду говорить какой. Не хочу, чтобы моя работа зря пропадала, тут хороший код, может пригодиться когда-нибудь. Задача: написать скрипт, который анализирует гитхабовский репозиторий, выводит тридцать лучших участников, статистику по задачам и пул-реквестам, всё это за указанный промежуток времени и на указанной ветке. Было разрешено использовать только стандартную питонскую библиотеку, поэтому пришлось без pytest, requests, click и PyGithub. Я пытался договориться, чтобы сняли ограничение на библиотеку, но не вышло. Как и устроиться в эту компанию, лол.

# Austin

A simple script to analyze Github repository:

```bash
python3 manage.py \
  https://github.com/django/django \
  --branch master \
  --start-date 2020-01-01 \
  --end-date 2020-03-01
```

```
Top contributors:
+----+-----------------+---------+
| #  | login           | commits |
+----+-----------------+---------+
| 1  | felixxm         | 40      |
| 2  | claudep         | 21      |
| 3  | hramezani       | 17      |
| 4  | carltongibson   | 14      |
| 5  | adamchainz      | 13      |
| 6  | jdufresne       | 11      |
| 7  | charettes       | 10      |
| 8  | sir-sigurd      | 7       |
| 9  | Taoup           | 4       |
| 10 | matheuscmotta   | 3       |
| 11 | matthijskooijman | 3       |
| 12 | abhijeetviswa   | 3       |
| 13 | apollo13        | 3       |
| 14 | hannseman       | 3       |
| 15 | pope1ni         | 3       |
| 16 | blueyed         | 3       |
| 17 | jcushman        | 3       |
| 18 | 007gzs          | 2       |
| 19 | cool-RR         | 2       |
| 20 | vdboor          | 2       |
| 21 | sanjioh         | 2       |
| 22 | Vibhu-Agarwal   | 2       |
| 23 | Hansikk         | 1       |
| 24 | kimbo           | 1       |
| 25 | cmackenziek     | 1       |
| 26 | rohitjha941     | 1       |
| 27 | Valze           | 1       |
| 28 | dorosch         | 1       |
| 29 | coltonbh        | 1       |
| 30 | andrewgodwin    | 1       |
+----+-----------------+---------+

Open pull requests count: 43
Closed pull requests count: 201
Stale pull requests count: 30

Open issues count: 0
Closed issues count: 0
Stale issues count: 0
```

How to use:

1. Generate personal access token for your Github account. No permissions are required, just make a bare token: https://github.com/settings/tokens

2. Write that token to `.token` file in this folder

3. That's it, you can now run `python3 manage.py <REPO_URL>`
