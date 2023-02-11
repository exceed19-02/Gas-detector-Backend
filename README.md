# Project-backend API Docs

here is a 2 domain for this project  
you can use any link between 2 of this domain
| Domain               | Link                                 |
| -------------------- | ------------------------------------ |
| exceed19.online      | http://group2.exceed19.online        |
| ecourse.cpe.ku.ac.th | http://ecourse.cpe.ku.ac.th/exceed02 |
1. get all record in the last hour : [get] `/last_hour`
    - return list of
        - x(time) : datetime.datetime
        - y(gas_quantity) : int
2. get all record in the last day : [get] `/record/last_day`
    - return list of
        - x(time) : datetime.datetime
        - y(avg of gas_quantity) : float
3. get last record : [get] `/record/last`
    - return JSON object
        - gas_quantity : int
        - status : enum["SAFE","WARNING","DANGER"]
4. get status of the window : [get] `/record/command`
    - return
        - isOpen : bool[True: เปิด, False: ปิด]
5. create new record : [post] `/add`
    - input JSON object as body
        - gas_quantity : int
        - status : enum["SAFE","WARNING","DANGER"]
    - return JSON object
        - message : "Record created"
6. update status of the window to bool by input : [put] `/update/{open}`
    - input as path
    - return JSON object
        - message : "already set command to {open}"
7. add mock data : [post] `/addmock`
    - return list of
        - gas_quantity : int
        - time : datetime.datetime
        - status : enum["SAFE","WARNING","DANGER"]
        - isCommand : False
