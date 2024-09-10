from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from dotenv import load_dotenv
import os


# 加载 .env 文件
load_dotenv()

# 获取环境变量
WP_URL = os.getenv('WP_URL')
WP_USERNAME = os.getenv('WP_USERNAME')
WP_PASSWORD = os.getenv('WP_PASSWORD')


message = """"""


client = Client(WP_URL, WP_USERNAME, WP_PASSWORD)

user_info = client.call(GetUserInfo())
print('用户名:', user_info.username)
print('昵称:', user_info.nickname)

# 创建一个新的 WordPressPost 对象
post = WordPressPost()
post.title = '我的第一篇文章'
post.content = message
post.terms_names = {
    'post_tag': ['Python', 'WordPress'],  # 文章标签
    'category': ['Technology']            # 文章分类
}
post.post_status = 'publish'  # 'draft' 表示草稿, 'publish' 表示发布

# 发布文章
post_id = client.call(NewPost(post))
print(f'文章发布成功，ID: {post_id}')


# from wordpress_xmlrpc.methods.posts import EditPost
#
# post_id_to_edit = post_id  # 假设你刚刚发布的文章
# post.title = '更新后的文章标题'
# client.call(EditPost(post_id_to_edit, post))
# print('文章更新成功')

