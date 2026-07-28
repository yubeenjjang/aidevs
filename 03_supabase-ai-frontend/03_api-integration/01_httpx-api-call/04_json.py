# https://jsonplaceholder.typicode.com/
# posts 정보를 가져와서 출력한다.
#userId, title, body 출력

import httpx

API_URL = "https://jsonplaceholder.typicode.com/posts"
response = httpx.get(API_URL, timeout=5.0)

print("status code:", response.status_code)  # HTTP 요청이 성공했는지 확인할 수 있는 상태 코드를 출력합니다.
print("json:", response.json())  # 백엔드가 반환한 JSON 응답을 딕셔너리 형태로 출력합니다.

result = response.json()
for data in result :
    print(f"{data["userId"]} {data["title"]}")
    
    