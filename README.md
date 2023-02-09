# Project-backend API Docs
http://group2.exceed19.online
1. get all data : [get] http://group2.exceed19.online/
    - return list of
        - sensor_id : int(1-3)
        - status : bool[True: มีแก๊สรั่ว, False: ไม่มีแก๊สรั่ว]
        - gas_quantity : int()
        - delay : int(0-500) #เป็นตัว delay ไฟ ถ้าไม่ใช่ 0 จะลดลงเรื่อยๆ (default = 500)
2. get data from sensor_id : [get] http://group2.exceed19.online/{id}
    - return
        - sensor_id : int(1-3)
        - status : bool[True: มีแก๊สรั่ว, False: ไม่มีแก๊สรั่ว]
        - gas_quantity : int()
        - delay : int(0-500) #เป็นตัว delay ไฟ ถ้าไม่ใช่ 0 จะลดลงเรื่อยๆ (default = 500)