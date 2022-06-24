
## Installation 
사전에 Docker가 설치되어있어야 합니다.   

```shell
> git clone https://github.com/OnlineJudgePlatformDev/CodingPlatformDev.git
> cd CodingPlatformDev
> docker-compose up -d
```   

<br />   

이후 ```docker ps -a``` 를 실행하게 되면 다음과 깉이 4개의 컨테이너가 구동되고 있는 것을 확인 할 수 있음   

<p align="center"><img src="../img/dockerpsa.png" /></p>   


실행 후 [http://localhost](http://localhost) 접속하면 끝.   
   
<br />   

> #### :no_entry_sign: Issue   

Chrome 기준 특정 버전 이상부터는 크롬 정책으로 인해 ```http://localhost``` 접속시 강제로 ```https://localhost ```로 리다이렉트되는 경우가 있음. (이 외에 다른 브라우저에서도 안 될 수 있음.)
이를 해결하기 위해서는 원칙상 SSL 인증서를 갱신하는게 올바르나, 개발도중 로컬에서 매번 인증서를 갱신하기에는 무리가 있으므로, 임시로 리다이렉트를 하지 않도록 설정하는 방식으로 진행한다.   


<br />   

```chrome://flags/#allow-insecure-localhost``` 로 접속 후 ```Allow invalid certificates for resources loaded from localhost. ``` 항목을 <b>Enabled</b> 로 변경   

<br />   

<br />   
<br />   


## Project Hierarchy   
프로젝트 기본 계층    

```ruby   

 CodingPlatformDev
 │── back
 └── front
 ```  

<br />   

> <b>바로가기</b>   

[backend](/Wiki/back)    
[frontend](/Wiki/front)   
[docker](/Wiki/dockerwiki)   

<br />   
<br />   

### Development Guide

<br />   

front 모듈은 기본 언어가 영어로 설정되어있다. 만약 한국어로 바꾸고자 한다면 다음과 같이 변경하면 된다.   
```front/src/i18n/index.js 파일의 locale 값을 en-US -> ko 로 변경```   

<br />
<p align="center"><img src=../img/set_lang.png width="50%" height="50%"/></p> 
