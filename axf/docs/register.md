####用户注册接口

######请求地址:/api/user/auth/register/
######请求方式:POST
######请求参数:
        u_username  用户名   str 必填
        u_password  密码     str 必填
        u_password2 确认密码 str 必填
        u_email     邮箱     str 必填
######响应结果:
      成功响应
      {
        "code": 200,
        "msg": "请求成功",
        "data": {
            "user_id": data.id,
        }
      }
      失败响应
      
######响应参数:
      user_id 登录用户的id值   int
      code 状态码  int
      msg  响应信息 str
      username 账号错误信息 str
      password 密码错误信息 str
      password2确认密码错误信息 str