# API

API commands documentation

@verify: the specified command need login permission token

### CONFIG

config_controller.py "/config" requests interact with the configuration file or the linux system.

@reboot: the specified configuration need a system reboot for the configuration to take effect.

-	Put_memory_type, @verify @reboot, [PUT]

change the measure database memory storage choice (SD or RAM).
```
/config/memory_type/<mem_type>
```

-	Get_memory_type, [GET]:

return the measure database memory storage choice.
```
/config/memory_type
```
-	Put_log_ip, @verify @reboot, [PUT] : 

change the IP address of the log server in the configuration file. 
```
/config/log_ip/<log_ip>
```
-	Put_log_port, @verify @reboot, [PUT] :

change the port of the log server in the configuration file.
```
/config/log_port/<log_port>
```
-	Put_password, @verify, [PUT]: 
     
change the API login password in the configuration file.
```
 /config/password/<password>
```
-	Put_reference_voltage, @verify, [PUT]: 
     
change the Pi reference voltage in the configuration file.
```
/config/reference_voltage/<reference_voltage>
```
-	Reboot_pi, @verify, [PUT]: 
     
reboot the Raspberry Pi.
```
/config/reboot
```

-   Get_pcu_ip, @verify, [GET]:

return the IP address of the Raspberry Pi
```
/config/ip
```    



### LOGIN

Login_controller.py "/login" route handles login.

-   Login, [GET]:
     
verifies the password and returns a token if password is valid. The token has to be in the "Authorization" Header of the @verify requests.
```
/login/<password>
```    
### PORTS

ports_controller.py "/port" handles port states.

-	Get_port_state, [GET]:
     
return the port state.

```
/port/<port_id>/state
```    

- Put_port_state, @verify, [PUT]:

receives a JSON and changes the port state
```
/port/state

# input json exemple
{
	"port_id": 1,       # 0 to 7
	"port_state": 1     # 0 or 1
}
```   
### RECORD

Record_controller.py "/record" route handles the record data :


-   Get_port_records, [GET]: 
```
/record/<port_id>/start_time/<start_time>/end_time/<end_time>/<period>

# return json exemple
{
	"measures": {
		"2022-04-14T20:49:14.893989Z": {
			"current": 0.01630756318508095,
			"voltage": 119.00038592375367,
			"power": 0.015100892019149938
		},
		"2022-04-14T20:49:15.914380Z": {
			"current": 0.017104905456638505,
			"voltage": 119.00038592375367,
			"power": 0.007641579016450932
		},
		"2022-04-14T20:49:16.933433Z": {
			"current": 0.017297118863946647,
			"voltage": 119.00038592375367,
			"power": 0.09825660908048378
		},
		"2022-04-14T20:49:17.953706Z": {
			"current": 0.015603764771220432,
			"voltage": 119.68429618768327,
			"power": 0.004059237898173001
		}
	},
	"avg_measure": {
		"current": 0.016578338069221633,
		"voltage": 119.17136348973607,
		"power": 0.03126457950356441
	},
	"max_measure": {
		"current": 0.017297118863946647,
		"voltage": 119.68429618768327,
		"power": 0.09825660908048378
	},
	"min_measure": {
		"current": 0.015603764771220432,
		"voltage": 119.00038592375367,
		"power": 0.004059237898173001
	},
	"port_states": [
		[
			"2022-04-14T20:49:14.893989Z",
			0
		]
	]
}
```   

return the port measures per period and port state changes in time frame.

-   Get_instant_measures, [GET]: 

```
/record/instant

# return json exemple
{
	"datetime": "2022-04-29T11:08:09.882849Z",
	"port_0": {
		"port_state": 0,
		"port_current": 0.03838840369475273,
		"port_voltage": 123.21909090909091,
		"port_power": 0.7118000659700394
	},
	"port_1": {
		"port_state": 1,
		"port_current": 1.8563432072500627,
		"port_voltage": 123.21909090909091,
		"port_power": 220.5533777565071
	},
	"port_2": {
		"port_state": 0,
		"port_current": 0.04269762812746883,
		"port_voltage": 123.21909090909091,
		"port_power": 0.14462408891909959
	},
	"port_3": {
		"port_state": 0,
		"port_current": 0.0438580331596468,
		"port_voltage": 123.21909090909091,
		"port_power": 0.3787969555206999
	},
	"port_4": {
		"port_state": 0,
		"port_current": 0.04597178313137518,
		"port_voltage": 123.21909090909091,
		"port_power": 0.23081556134829226
	},
	"port_5": {
		"port_state": 0,
		"port_current": 0.0502040618999249,
		"port_voltage": 123.21909090909091,
		"port_power": 0.2106722321288209
	},
	"port_6": {
		"port_state": 0,
		"port_current": 0.04785599379314861,
		"port_voltage": 123.21909090909091,
		"port_power": 0.09875260342551694
	},
	"port_7": {
		"port_state": 0,
		"port_current": 0.035106942607775485,
		"port_voltage": 123.21909090909091,
		"port_power": 0.0
	}
}
``` 
   
return the last measures and port states.
