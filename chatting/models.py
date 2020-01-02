from .search import BlogPostIndex

def indexing(self):
   obj = BlogPostIndex(
      meta={'id': self.id},
      author=self.author.username,
      posted_date=self.posted_date,
      title=self.title,
      text=self.text
   )
   obj.save()
   return obj.to_dict(include_meta=True)