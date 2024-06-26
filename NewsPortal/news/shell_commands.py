from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment

# Создание пользователей
user1 = User.objects.create_user('user1', password='password123')
user2 = User.objects.create_user('user2', password='password123')

# Создание авторов
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Создание категорий
category1 = Category.objects.create(name='Sports')
category2 = Category.objects.create(name='Politics')
category3 = Category.objects.create(name='Education')
category4 = Category.objects.create(name='Technology')

# Создание статей и новостей
post1 = Post.objects.create(author=author1, type=Post.ARTICLE, title='Article 1', text='Content of article 1')
post2 = Post.objects.create(author=author2, type=Post.ARTICLE, title='Article 2', text='Content of article 2')
news1 = Post.objects.create(author=author1, type=Post.NEWS, title='News 1', text='Content of news 1')

# Присвоение категорий статьям и новостям
post1.categories.add(category1, category2)
post2.categories.add(category2, category3)
news1.categories.add(category3, category4)

# Создание комментариев
comment1 = Comment.objects.create(post=post1, user=user2, text='Comment to post 1 by user2')
comment2 = Comment.objects.create(post=post1, user=user1, text='Comment to post 1 by user1')
comment3 = Comment.objects.create(post=post2, user=user1, text='Comment to post 2 by user1')
comment4 = Comment.objects.create(post=news1, user=user2, text='Comment to news 1 by user2')

# Применение лайков и дизлайков к статьям/новостям и комментариям
post1.like()
post1.like()
post2.like()
news1.dislike()

comment1.like()
comment2.dislike()
comment3.like()
comment4.like()

# Обновление рейтингов авторов
author1.update_rating()
author2.update_rating()

# Вывод username и рейтинга лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
best_author.user.username, best_author.rating

# Вывод даты добавления, username автора, рейтинга, заголовка и превью лучшей статьи
best_post = Post.objects.order_by('-rating').first()
best_post.created_at, best_post.author.user.username, best_post.rating, best_post.title, best_post.preview()

# Вывод всех комментариев к лучшей статье
comments = Comment.objects.filter(post=best_post)
for comment in comments:

from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment

# Создание пользователей
user1 = User.objects.create_user('user1', password='password123')
user2 = User.objects.create_user('user2', password='password123')

# Создание авторов
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Создание категорий
category1 = Category.objects.create(name='Sports')
category2 = Category.objects.create(name='Politics')
category3 = Category.objects.create(name='Education')
category4 = Category.objects.create(name='Technology')

# Создание статей и новостей
post1 = Post.objects.create(author=author1, type=Post.ARTICLE, title='Article 1', text='Content of article 1')
post2 = Post.objects.create(author=author2, type=Post.ARTICLE, title='Article 2', text='Content of article 2')
news1 = Post.objects.create(author=author1, type=Post.NEWS, title='News 1', text='Content of news 1')

# Присвоение категорий статьям и новостям
post1.categories.add(category1, category2)
post2.categories.add(category2, category3)
news1.categories.add(category3, category4)

# Создание комментариев
comment1 = Comment.objects.create(post=post1, user=user2, text='Comment to post 1 by user2')
comment2 = Comment.objects.create(post=post1, user=user1, text='Comment to post 1 by user1')
comment3 = Comment.objects.create(post=post2, user=user1, text='Comment to post 2 by user1')
comment4 = Comment.objects.create(post=news1, user=user2, text='Comment to news 1 by user2')

# Применение лайков и дизлайков к статьям/новостям и комментариям
post1.like()
post1.like()
post2.like()
news1.dislike()

comment1.like()
comment2.dislike()
comment3.like()
comment4.like()

# Обновление рейтингов авторов
author1.update_rating()
author2.update_rating()

# Вывод username и рейтинга лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
best_author.user.username, best_author.rating

# Вывод даты добавления, username автора, рейтинга, заголовка и превью лучшей статьи
best_post = Post.objects.order_by('-rating').first()
best_post.created_at, best_post.author.user.username, best_post.rating, best_post.title, best_post.preview()

# Вывод всех комментариев к лучшей статье
comments = Comment.objects.filter(post=best_post)
for comment in comments:
    comment.created_at, comment.user.username, comment.rating, comment.text