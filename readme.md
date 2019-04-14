# 测试edgexfoundry
通过模拟一个pymodbus server来测试edgexfoundry对数据的采集、
## 依赖
- Python，`pymodbus`
- `docker`, `docker-compose`
  
## 使用
- 1 安装python相关依赖，```pip install -r requirements.txt```
- 2 启动一个pymodbus TCP server；**修改script.py里```address=("192.168.0.110", 5020)```为你自己启动的地址**
- 3 ```docker-compose up -d```启动edgexfoundry相关服务；
- 4 ```curl http://localhost:48080/api/v1/event``` 查看取到的数据；**取到到的数据进行了`base64`加密**