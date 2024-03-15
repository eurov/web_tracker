## За нами следят (Python)


Чтобы запустить проект:

```bash
docker compose up --detach --build  
```

Затем в бразуере перейти по адресу ```http://localhost:8000/```, и воспользоваться клиентом DRF для отправки запросов.


Отправить запрос также можно из консоли, с помощью инструмента командной строки ```curl```

```bash
 curl http://127.0.0.1:8000/visited_domains/              
  
```

Пример ответа:
```
> {"domains":["ya.ru","sber.ru","stackoverflow.com"],"status":"ok"}
```



