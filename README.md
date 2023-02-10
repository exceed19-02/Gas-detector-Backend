# Project-backend API Docs
http://group2.exceed19.online
1. get all record in the last hour : [get] http://group2.exceed19.online/record/lasthour
    - return list of
        - gas_quantity : int
        - time : datetime.datetime
2. get last record : [get] http://group2.exceed19.online/record/last
    - return JSON object
        - gas_quantity : int
        - status : enum["SAFE","WARNING","DANGER"]
3. get status of the window : [get] http://group2.exceed19.online/record/command
    - return
        - isOpen : bool[True: เปิด, False: ปิด]
4. create new record : [post] http://group2.exceed19.online/add
    - input JSON object as body
        - gas_quantity : int
        - status : enum["SAFE","WARNING","DANGER"]
    - return JSON object
        - message : "Record created"
5. update status of the window to bool by input : [put] http://group2.exceed19.online/update/{open}
    - input as path
    - return JSON object
        - message : "already set command to {open}"