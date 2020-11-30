import huawei_b890_api
import time

x = huawei_b890_api.HuaweiB890API('user', 'password')

with open('log.csv', 'w') as file:
    data = x.diagnosis()
    file.write(','.join(str(e) for e in list(data.keys())))
    file.write('\n')
    t = 60
    while t > 0:
        data = x.diagnosis()
        file.write(','.join(str(e) for e in list(data.values())))
        file.write('\n')
        time.sleep(1)
        t -= 1

x.logout()
