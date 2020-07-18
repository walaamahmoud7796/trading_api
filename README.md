# Trading API

in repo directory run the following command
```
docker-compose up
```


# This app contains 6 routes 
* deposit
* withdraw
* buy
* sell
* stock
* user

### Deposit 
#### Definition
```
POST/deposit
```
### Arguments
* ```user_id:string``` unique identifier for the user
* ```amount:float```  deposit amount
#### Response
```json
    {
        "data": {
            "amount": "2000",
            "transaction_id": "fae8f7de-c912-11ea-8bd3-0242ac130002",
            "transaction_timestamp": "2020-07-18 16:23:14",
            "type": "deposit",
            "user_current_balance": 2000.0,
            "user_id": "e60a0530-c910-11ea-86cb-0242ac130002"
        },
        "message": "Success"
    }
```

### Withdraw
#### Definition
```
POST/withdraw
```
### Arguments
* ```user_id:string``` unique identifier for the user
* ```amount:float``` withdraws amount

#### Response on success
```json
{
    "data": {
        "amount": "50",
        "transaction_id": "fc9f81c4-c912-11ea-8bd3-0242ac130002",
        "transaction_timestamp": "2020-07-18 16:23:17",
        "type": "withdrawal",
        "user_current_balance": 1950.0,
        "user_id": "e60a0530-c910-11ea-86cb-0242ac130002"
    },
    "message": "Success"
}

```
#### Response on Failure
```json
{
    "data": {
        "user_current_balance": 1950
    },
    "message": "Insufficient request"
}
```

### Buy
### Definition
```
POST/buy
```
### Arguments
* ```user_id:string``` unique identifier for the user
* ```stock_id:string``` unique identifier for the required stock
* ```upper_bound:float```  upper bound for stock price
* ```lower_bound:float``` lower bound for stock price
* ```total:int``` total number of stocks to be bought 

### Response on succcess
```json
{
    "data": {
        "lower_bound": "150",
        "stock_id": "6c06600a-438d-46a0-9193-80d4a8d114db",
        "total": "10",
        "trade_id": "050a1392-c913-11ea-8bd3-0242ac130002",
        "trade_price": 1710.0,
        "upper_bound": "200",
        "user_id": "e60a0530-c910-11ea-86cb-0242ac130002"
    },
    "message": "successful trade"
}
```
### Response on failure 
#### case1
```json
{
    "message": "unsuccessful trade, stock price is out of bounds"
}
```
#### case2
```
{
    "data": {
        "trade_price": 8550.0,
        "user_balance": 1950
    },
    "message": "unsuccessful trade due to insufficient balance"
}
```
### Sell
### Definition
```
POST/sell
```
### Arguments
* ```user_id:string``` unique identifier for the user
* ```stock_id:string``` unique identifier for the required stock
* ```upper_bound:float```  upper bound for stock price
* ```lower_bound:float``` lower bound for stock price
* ```total:int``` total number of stocks to be bought 
### Response on success
```json
{
    "data": {
        "lower_bound": "150",
        "stock_id": "6c06600a-438d-46a0-9193-80d4a8d114db",
        "total": "10",
        "trade_id": "0f8a8cde-c913-11ea-8bd3-0242ac130002",
        "trade_price": 1710.0,
        "upper_bound": "200",
        "user_id": "e60a0530-c910-11ea-86cb-0242ac130002"
    },
    "message": "successful trade"
}
```
### Response on failure
```json
```json
{
    "message": "unsuccessful trade, stock price is out of bounds"
}
```
### Stock
### Definition
```
GET/stock
```
### Arguments
* ```stock_id:string``` unique identifier for the required stock
### Response
list of all trades done on that stock
```json
{
    "stock_id": "6c06600a-438d-46a0-9193-80d4a8d114db",
    "trades": [
        {
            "note": "stock price is out of bounds",
            "status": "unsuccessful",
            "stock_price": 171,
            "total_stocks": 10,
            "trade_id": "01d92334-c913-11ea-8bd3-0242ac130002",
            "trade_timestamp": "2020-07-18 16:23:26",
            "trade_type": "buy",
            "user_id": "e60a0530-c910-11ea-86cb-0242ac130002"
        },
        {
            "note": "user balance is sufficient",
            "status": "successful",
            "stock_price": 171,
            "total_stocks": 10,
            "trade_id": "050a1392-c913-11ea-8bd3-0242ac130002",
            "trade_timestamp": "2020-07-18 16:23:31",
            "trade_type": "buy",
            "user_id": "e60a0530-c910-11ea-86cb-0242ac130002"
        },
        {
            "note": "stock price is out of bounds",
            "status": "unsuccessful",
            "stock_price": 171,
            "total_stocks": 10,
            "trade_id": "089abab6-c913-11ea-8bd3-0242ac130002",
            "trade_timestamp": "2020-07-18 16:23:37",
            "trade_type": "sell",
            "user_id": "1"
        },
        {
            "note": "stock price matches bounds",
            "status": "successful",
            "stock_price": 171,
            "total_stocks": 10,
            "trade_id": "0b8cb08a-c913-11ea-8bd3-0242ac130002",
            "trade_timestamp": "2020-07-18 16:23:42",
            "trade_type": "sell",
            "user_id": "1"
        },
        {
            "note": "stock price matches bounds",
            "status": "successful",
            "stock_price": 171,
            "total_stocks": 10,
            "trade_id": "0f8a8cde-c913-11ea-8bd3-0242ac130002",
            "trade_timestamp": "2020-07-18 16:23:49",
            "trade_type": "sell",
            "user_id": "e60a0530-c910-11ea-86cb-0242ac130002"
        }
    ]
}

```

### User
### Definition 
```GET/user```
### Arguments
* ```user_id:string``` unique identifier for the user
### Response
```json
{
    "current_balance": 1950,
    "trades": [
        {
            "note": "stock price is out of bounds",
            "status": "unsuccessful",
            "stock_id": "6c06600a-438d-46a0-9193-80d4a8d114db",
            "stock_price": 171,
            "total_stocks": 10,
            "trade_id": "01d92334-c913-11ea-8bd3-0242ac130002",
            "trade_timestamp": "2020-07-18 16:23:26",
            "trade_type": "buy",
            "user_id": "e60a0530-c910-11ea-86cb-0242ac130002"
        },
        {
            "note": "user balance is sufficient",
            "status": "successful",
            "stock_id": "6c06600a-438d-46a0-9193-80d4a8d114db",
            "stock_price": 171,
            "total_stocks": 10,
            "trade_id": "050a1392-c913-11ea-8bd3-0242ac130002",
            "trade_timestamp": "2020-07-18 16:23:31",
            "trade_type": "buy",
            "user_id": "e60a0530-c910-11ea-86cb-0242ac130002"
        },
        {
            "note": "stock price matches bounds",
            "status": "successful",
            "stock_id": "6c06600a-438d-46a0-9193-80d4a8d114db",
            "stock_price": 171,
            "total_stocks": 10,
            "trade_id": "0f8a8cde-c913-11ea-8bd3-0242ac130002",
            "trade_timestamp": "2020-07-18 16:23:49",
            "trade_type": "sell",
            "user_id": "e60a0530-c910-11ea-86cb-0242ac130002"
        }
    ],
    "transactions": [
        {
            "amount": 2000,
            "transaction_id": "fae8f7de-c912-11ea-8bd3-0242ac130002",
            "transaction_timestamp": "2020-07-18 16:23:14",
            "type": "deposit"
        },
        {
            "amount": 50,
            "transaction_id": "fc9f81c4-c912-11ea-8bd3-0242ac130002",
            "transaction_timestamp": "2020-07-18 16:23:17",
            "type": "withdrawal"
        }
    ],
    "user_id": "e60a0530-c910-11ea-86cb-0242ac130002"
}
```


