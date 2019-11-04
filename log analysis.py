import psycopg2
import numpy as np
import re
from datetime import datetime

# this part shows the most errors occured in a day
print('most errors were occured on')
db = psycopg2.connect('dbname=news')
c = db.cursor()
c.execute(""" select to_char(errors.day, 'Mon DD, YYYY'),
    ROUND(((errors.errors/total.total) * 100)::DECIMAL, 2)::TEXT as percentage
    FROM errors, total
    WHERE total.day = errors.day
    AND (((errors.errors/total.total) * 100) > 1.0)
    ORDER BY errors.day;""")
f = c.fetchall()
sol = datetime.strftime(f[0][0], '%b %d, %Y')
print(sol)
db.close()
print('')
print('These are the most viewed articles')

# this part shows the top three most viewed articles
db = psycopg2.connect('dbname=news')
c = db.cursor()
c.execute(""" select *
                from top_three_articles
                order by views desc
                limit 3;""")
sol = c.fetchall()
for x in range(len(sol)):
    print(str(sol[x][0])+'-'+str(sol[x][1]) + ' Views')
db.close()

print('')
print('most popular Authors are the following')

# this part is to show the most popular author
db = psycopg2.connect('dbname=news')
c = db.cursor()
c.execute("""select name as top_three_authors,
    sum(top_three_articles.views) as views
    from authord, top_three_articles
    where authord.title = top_three_articles.title
    group by top_three_authors
    order by views desc
    limit 3;""")
sol = c.fetchall()
for x in range(len(sol)):
    print(str(sol[x][0])+'-'+str(sol[x][1]) + ' Views')
db.close()