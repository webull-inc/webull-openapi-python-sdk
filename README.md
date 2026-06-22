# Webull OpenAPI Python SDK

Note: This is the new version of the Webull SDK, currently applicable only to Webull Hong Kong, Webull US, Webull JP, Webull SG, Webull TH, Webull AU, Webull MY, Webull UK, Webull BR, Webull MX, Webull ZA, or Webull EU customers.

Webull OpenAPI aims to provide quantitative trading investors with convenient, fast and secure services. Webull aims to help every quant traders achieve flexible and changeable trading or market strategies.

The main function:

Trading management: create, modify, cancel orders, etc.

Market information: You can query stocks/ETFs and other related market information through the HTTP interface.

Account Information: Query account balance and position information.

Subscription to real-time information: Subscribe to order status changes, market information, etc.

## Requirements

- Please first generate the app key and app secret on the Webull official website.

| Broker    | Link                                            |
|-----------|-------------------------------------------------|
| Webull HK | https://www.webull.hk/open-api                  |
| Webull US | https://www.webull.com/center#openApiManagement |
| Webull JP | https://www.webull.co.jp/center/openapi/manage |
| Webull SG | https://www.webull.com.sg/open-api-management|
| Webull TH | https://www.webull.co.th/open-api-management |
| Webull AU | https://www.webull.com.au/open-api-management   |
| Webull MY | https://www.webull.com.my/open-api-management   |
| Webull UK | https://www.webull-uk.com/open-api-management   |
| Webull BR | https://www.webull.com.br/open-api-management   |
| Webull MX | https://www.webull.com.mx/open-api-management   |
| Webull ZA | https://www.webull.co.za/open-api-management    |
| Webull EU | https://www.webull.eu/open-api-management       |
- Requires Python 3.8 through 3.13.

## Interface Protocol

The bottom layer of Webull OpenAPI provides three protocols, HTTP / GRPC / MQTT, to support functions and features like trading, subscriptions for changes of order status and real-time market quotes.

| Protocol | Description                                                                                                    |
|----------|----------------------------------------------------------------------------------------------------------------|
| HTTP     | It mainly provides interface services for data such as tradings, accounts, candlestick charts, snapshots, etc. |
| GRPC	    | 1. Provide real-time push messages for order status changes.                                                   |
| MQTT	    | Provides data services for real-time market conditions.                                                        |

## Developer documentation

| Broker    | Link                                     |
|-----------|------------------------------------------|
| Webull HK | https://developer.webull.hk/apis/docs    |
| Webull US | https://developer.webull.com/apis/docs   |
| Webull JP | https://developer.webull.co.jp/apis/docs |
| Webull SG | https://developer.webull.com.sg/apis/docs |
| Webull TH | https://developer.webull.co.th/apis/docs |
| Webull AU | https://developer.webull.com.au/apis/docs |
| Webull MY | https://developer.webull.com.my/apis/docs |
| Webull UK | https://developer.webull-uk.com/apis/docs |
| Webull BR | https://developer.webull.com.br/apis/docs |
| Webull MX | https://developer.webull.com.mx/apis/docs |
| Webull ZA | https://developer.webull.co.za/apis/docs |
| Webull EU | https://developer.webull.eu/apis/docs |