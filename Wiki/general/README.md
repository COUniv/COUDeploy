### 일반적인 배포 방법

------

- 프론트엔드

먼저 완성된 frontend파일을 빌드 합니다.

```shell
cd COUDeploy/frontend
npm run build 
>>>dist
```



그리고 빌드 이후 결과물로 나온 `dist` 폴더를 압축합니다.

`dist.zip`을 `backend`폴더에 복사 붙여넣기를 합니다.

<br>
<br>

- 백엔드

적용된 `dist` 폴더를 확인한 후 도커 이미지로 빌드 합니다.

```shell
cd COUDeploy/backend
docker build --tag [name]:[version] .
>>>backend 폴더를 도커 이미지로 빌드...
```



빌드를 진행하면 도커 이미지 파일이 생성 됩니다. 그리고 이 이미지를 배포하면 됩니다.

```shell
#먼저 도커에 로그인하는 과정이 필요합니다.
docker push [repositories_name]:[version]
```



이제 내 도커 허브에 가서 확인해서 정상적으로 배포가 되었는지 확인합니다!

