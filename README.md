#### 趣维审核

> 


#### 视频审核

```cython

from review_saas.video_review import Video

video_review = Video(client_id, toke)
flag,msg = video_review.review(视频编号,视频播放地址,业务码, 视频时长, 用户id)
if not flag:
    print(msg)

```

#### 图片审核

```cython

from review_saas.img_review import ImgReview

img_review = ImgReview(client_id,token)
flag,msg = img_review.review(video_id: int, secret_id: str, user_id: str, img_list: List, video_url: str = '')
if not flag:
    print(msg)

```



#### 文本审核

```cython

from review_saas.text_review import TextReview

img_review = TextReview(client_id,token)
flag,msg = img_review.review(text_id: int, secret_id: str, user_id: str, text:str)
if not flag:
    print(msg)

```