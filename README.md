# huawei_b890_api

## Get started

```python
import huawei_b890_api

# fill your username and password
b890 = huawei_b890_api.HuaweiB890API('user', 'password')
```

From there, you can call a number of endpoints, e.g.

```python
b890.status() # returns the status of the current user (if there is one)

b890.login() # manual login; whenever needed, authentication is done automatically

b890.diagnosis() # returns a dict of diagnosis values like RSSI, NetworkBand, etc.

b890.logout() # logout; releasing the user and clearing cookies
```

For quick access to other endpoints you can use the `custom_endpoint` method:
```python
b890.custom_endpoint('/api/connection/lanstatus') # returns connected devices, etc.
```
(Note the leading slash.)

## More
I'm sure you'll figure out whatever API endpoints you require - if not, feel free to create an issue ;)

For a little example of a simple CSV logger see `diagnosis_logger.py`.
