



```
$ container-versions `docker ps --format '{{ .Image}}' | xargs`
library/redis                 	 Latest:             4.0,   1 days old	Running:    4.0.6-alpine,  14 days old
google/cadvisor               	 Latest:         v0.27.4,  28 days old	Running:         v0.28.3,  62 days old
library/chronograf            	 Latest:         1.4.0.1,  26 days old	Running: 1.3.10.0-alpine,  28 days old
prom/prometheus               	 Latest:          v2.1.0,  19 days old	Running:          v2.0.0,  91 days old
library/kapacitor             	 Latest:          alpine,  28 days old	Running:    1.4.0-alpine,  28 days old
library/telegraf              	 Latest:           1.5.2,   6 days old	Running:    1.5.0-alpine,  28 days old
grafana/grafana               	 Latest:          latest,   2 days old	Running:           4.6.3,  55 days old
homeassistant/home-assistant  	 Latest:          0.62.1,   8 days old	Running:          0.61.1,  21 days old
library/mysql                 	 Latest:          5.6.39,  23 days old	Running:          5.7.20,  57 days old
library/influxdb              	 Latest:          latest,   6 days old	Running:    1.4.2-alpine,  29 days old
library/haproxy               	 Latest:             1.7,   9 days old	Running:    1.8.3-alpine,  14 days old
library/traefik               	 Latest:      1.5-alpine,   8 days old	Running:          latest,   8 days old
```
