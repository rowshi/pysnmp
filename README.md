
SNMP library for Python
-----------------------

[![PyPI](https://img.shields.io/pypi/v/pysnmplib.svg?maxAge=2592000)](https://pypi.python.org/pypi/pysnmplib)
[![Python Versions](https://img.shields.io/pypi/pyversions/pysnmplib.svg)](https://pypi.python.org/pypi/pysnmplib/)
[![CI](https://github.com/pysnmp/pysnmp/actions/workflows/build-test-release.yml/badge.svg)](https://github.com/pysnmp/pysnmp/actions/workflows/build-test-release.yml)
[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/pysnmp/pysnmp/master/LICENSE.rst)

This is a pure-Python, open source and free implementation of v1/v2c/v3
SNMP engine distributed under 2-clause [BSD license](http://snmplabs.com/pysnmp/license.html).

The PySNMP project was initially sponsored by a [PSF](http://www.python.org/psf/) grant.
Thank you!

This version is a fork of Ilya Etingof's project [etingof/pysnmp](https://github.com/etingof/pysnmp). Ilya sadly passed away on 10-Aug-2022. Announcement [here](https://lists.openstack.org/pipermail/openstack-discuss/2022-August/030062.html).  His work is still of great use to the Python community and he will be missed.

Features
--------

* Complete SNMPv1/v2c and SNMPv3 support
* SMI framework for resolving MIB information and implementing SMI
  Managed Objects
* Complete SNMP entity implementation
* USM Extended Security Options support (3DES, 192/256-bit AES encryption)
* Extensible network transports framework (UDP/IPv4, UDP/IPv6)
* Asynchronous socket-based IO API support
* [Asyncio](https://docs.python.org/3/library/asyncio.html) integration
* [PySMI](http://snmplabs.com/pysmi/) integration for dynamic MIB compilation
* Built-in instrumentation exposing protocol engine operations
* Python eggs and py2exe friendly
* 100% Python, works with Python 2.4 though 3.7
* MT-safe (if SnmpEngine is thread-local)

Features, specific to SNMPv3 model include:

* USM authentication (MD5/SHA-1/SHA-2) and privacy (DES/AES) protocols (RFC3414, RFC7860)
* View-based access control to use with any SNMP model (RFC3415)
* Built-in SNMP proxy PDU converter for building multi-lingual
  SNMP entities (RFC2576)
* Remote SNMP engine configuration
* Optional SNMP engine discovery
* Shipped with standard SNMP applications (RC3413)


Download & Install
------------------

The PySNMP software is freely available for download from [PyPI](https://pypi.python.org/pypi/pysnmplib)
and [GitHub](https://github.com/pysnmp/pysnmp.git).

Just run:

```bash
$ pip install pysnmplib
```

To download and install PySNMP along with its dependencies:

<!-- Need to find an alternate location for the links to snmplabs.com -->
* [PyASN1](http://snmplabs.com/pyasn1/)
* [PyCryptodomex](https://pycryptodome.readthedocs.io) (required only if SNMPv3 encryption is in use)
* [PySMI](http://snmplabs.com/pysmi/) (required for MIB services only)

Besides the library, command-line [SNMP utilities](https://github.com/etingof/snmpclitools)
written in pure-Python could be installed via:

```bash
$ pip install snmpclitools
```

and used in the very similar manner as conventional Net-SNMP tools:

```bash
$ snmpget.py -v3 -l authPriv -u usr-md5-des -A authkey1 -X privkey1 demo.snmplabs.com sysDescr.0
SNMPv2-MIB::sysDescr.0 = STRING: Linux zeus 4.8.6.5-smp #2 SMP Sun Nov 13 14:58:11 CDT 2016 i686
```

Examples
--------

PySNMP is designed in a layered fashion. Top-level and easiest to use API is known as
*hlapi*. Here's a quick example on how to SNMP GET:

```python
from pysnmp.hlapi import *

iterator = getCmd(SnmpEngine(),
                  CommunityData('public'),
                  UdpTransportTarget(('demo.snmplabs.com', 161)),
                  ContextData(),
                  ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

if errorIndication:  # SNMP engine errors
    print(errorIndication)
else:
    if errorStatus:  # SNMP agent errors
        print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
    else:
        for varBind in varBinds:  # SNMP response contents
            print(' = '.join([x.prettyPrint() for x in varBind]))
```

This is how to send SNMP TRAP:

```python
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    sendNotification(
        SnmpEngine(OctetString(hexValue='8000000001020304')),
        UsmUserData('usr-sha-aes128', 'authkey1', 'privkey1',
                    authProtocol=usmHMACSHAAuthProtocol,
                    privProtocol=usmAesCfb128Protocol),
        UdpTransportTarget(('demo.snmplabs.com', 162)),
        ContextData(),
        'trap',
        NotificationType(ObjectIdentity('SNMPv2-MIB', 'authenticationFailure'))
    )
)

if errorIndication:
    print(errorIndication)
```

> We maintain publicly available SNMP Agent and TRAP sink at
> [demo.snmplabs.com](http://snmplabs.com/snmpsim/public-snmp-agent-simulator.html). You are
> welcome to use it while experimenting with whatever SNMP software you deal with.

:warning: ***This is no longer the case as the snmplabs.com site is now defunct***

```bash
$ python3 examples/hlapi/asyncore/sync/manager/cmdgen/usm-sha-aes128.py
SNMPv2-MIB::sysDescr.0 = SunOS zeus.snmplabs.com 4.1.3_U1 1 sun4m
$
$ python3 examples//hlapi/asyncore/sync/agent/ntforg/v3-inform.py
SNMPv2-MIB::sysUpTime.0 = 0
SNMPv2-MIB::snmpTrapOID.0 = SNMPv2-MIB::warmStart
SNMPv2-MIB::sysName.0 = system name
```

Other than that, PySNMP is capable to automatically fetch and use required MIBs from HTTP, FTP sites
or local directories. You could configure any MIB source available to you (including
[this one](https://pysnmp.github.io/mibs/asn1/)) for that purpose.

For more example scripts please refer to ~~[examples section](http://snmplabs.com/pysnmp/examples/contents.html#high-level-snmp)~~
at pysnmp web site.

Documentation
-------------

Library documentation and examples can be found at the ~~[pysnmp project site](http://snmplabs.com/pysnmp/)~~.

If something does not work as expected, please
[open an issue](https://github.com/pysnmp/pysnmp/issues) at GitHub or
post your question [on Stack Overflow](http://stackoverflow.com/questions/ask) or try browsing pysnmp
[mailing list archives](https://sourceforge.net/p/pysnmp/mailman/pysnmp-users/).

Bug reports and PRs are appreciated! ;-)

Copyright (c) 2005-2019, [Ilya Etingof](https://lists.openstack.org/pipermail/openstack-discuss/2022-August/030062.html). All rights reserved.
