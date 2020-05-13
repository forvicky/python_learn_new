# sub 正则替换
import re

lanuage = 'Python Java\/:*?"<>|    C#JavaPHPC# '

# sub 正则替换
r = re.sub('[\s\\\/:*?"<>|]','', lanuage)
print(r)