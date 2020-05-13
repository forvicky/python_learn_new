"""
if elif else示例
"""
ACCOUNT = 'zdd'
PASSWORD = '123456'

print("account")
user_account = input()

print("password")
user_password = input()

if user_account is None or ACCOUNT != user_account:
    print('账号错误')
elif PASSWORD != user_password:
    print('密码错误')
else:
    print('success')