# from fastapi import FastAPI, Depends, Body, HTTPException, status
# from jose import JWTError, jwt
#
# SECRET_KEY = "ed970259a19edfedf1010199c7002d183bd15bcaec612481b29bac1cb83d8137"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
#
# @app.get('/')
# async def test(token: str = Depends(oauth2_scheme)):
#     # 定义一个验证异常的返回
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="认证失败",
#         # 根据OAuth2规范, 认证失败需要在响应头中添加如下键值对
#         headers={'WWW-Authenticate': "Bearer"}
#     )
#     # 验证token
#     try:
#         # 解密token, 返回被加密的字典
#         payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
#         print(f'payload: {payload}')
#         # 从字典中获取user_id数据
#         user_id = payload.get('user_id')
#         print(f'user_id: {user_id}')
#         # 若没有user_id, 则返回认证异常
#         if not user_id:
#             raise credentials_exception
#     except JWTError as e:
#         print(f'认证异常: {e}')
#         # 如果解密过程出现异常, 则返回认证异常
#         raise credentials_exception
#     # 解密成功, 返回token中包含的user_id
#     return {'hello': user_id}
