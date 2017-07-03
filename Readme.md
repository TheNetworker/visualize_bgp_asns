BGP_Visualize
============
Python Module to beautifully visualize the connections between BGP Autonomous System with capability to identify the service providers (operators) and downstream, upstream for each AS or for specific country
 
## Installation

### CLI

```py
pip install bgp_visualize
```

### GUI (using Pycharm)

![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/Pycharm.png)

## Examples:

### Example 1
Visualize ASN #8452 (Telecom Egypt) and ASN #24835(Vodafone Egypt)

![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/8452.png)

```py

from bgp_visualize import bgp_visualize_asn

ASNs= bgp_visualize_asn.bgp_visualize(asns=[8452,24835],dark=True)
ASNs.Draw()

```

### Example 2
Visualize All Autonomous Systems in specific country by providing the **country code** to the module 

![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/KSA.png)

| ASN Number   :| Operator                           |
|--------------:|-------------------------------------|
| 39386        :| Saudi Telecom Communications (STC)|
| 25019        :| Saudi Telecom Communications (STC)|
| 25233        :| AwalNet ISP                       |
| 35819        :| Mobily                             | 
| 47794        :| GO Telecom                         |
| 34397        :| Cyberia Riyadh Autonomous System |



```py

from bgp_visualize import bgp_visualize_asn

country= bgp_visualize_asn.bgp_visualize(country='sa')
country.Draw()

```

More Screenshots
----------------
1. **Visualize Autonomous Systems in UAE**

  ![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/UAE_BLACK_Zoom2.png)


  ![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/UAE_Zoom1.png)

| ASN Number    | Operator                   |
|--------------:|----------------------------|
| 8966         :| Emirates Telecom           |
| 5384         :| Emirates Telecom           |
| 15802        :| DU                        | 
| 20612        :| SwissIX Internet Exchange |




2. **Visualize Autonomous Systems in Poland**
  
  ![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/Poland_Zoom2.png)

3. **Visualize Autonomous Systems in Egypt**

  ![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/EG.png)

| ASN Number    | Operator                |
|--------------:|---------------------   |
| 8452         :| Telecom Egypt(TEData)   |
| 24835        :| Vodafone Egypt          | 
| 24863        :| Orange Egypt            |
| 36992        :| Etisalat Egypt          |
| 20928        :| Noor ISP                |


Color Map
-------------
**bgp_visualize** module use different colors to represent the Autonomous System role in the graph. below is the list of colors and meaning of each in the generated graph

1. AS is **Upstream** ![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/Upstream_Icon.png)

1. AS is **Downstream** ![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/Downstream_Icon.png)

1. AS is **Transit or unidentified yet** ![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/Transiet_or_unidentified_icon.png)

1. AS is **Service Provider (Operator) or IXP (Internet Exchange Point) ** ![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/operators_icons.png)

Customizing the Graph
---------------------
By default, You don't need to provide any additional parameters to draw and visualize the AS (either a set of autonomous systems or an entire country), However if you would like to have your own colors, then provide the below options during object instantiation and they will override the default behavior 


| Parameter     | Default       |
| ------------- |:-------------:|
| u_color      :| #009999       |
| d_color      :| #ED9236       | 
| default_color | #999999       |


## In-Development
1. Support Threading for faster processing
2. Support IPv6 peers graph

## Questions/Discussion

If you find an issue with BGP_Visualize, then you can open an issue on this projects issue page here: [https://github.com/TheNetworker/visualize_bgp_asns/issues](https://github.com/TheNetworker/visualize_bgp_asns/issues)

## Ideas/Suggestion
You're welcomed to send you suggestion or ideas to [basim.alyy@gmail.com](mailto:basim.alyy@gmail.com)

---    
Bassim Aly  
The Networker

[http://basimaly.wordpress.com/](http://basimaly.wordpress.com/)

![alt text](https://raw.githubusercontent.com/TheNetworker/visualize_bgp_asns/master/Small%20Logo.png)