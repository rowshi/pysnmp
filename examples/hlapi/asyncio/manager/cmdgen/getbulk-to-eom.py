#!/usr/bin/env python3
"""
Bulk walk MIB
+++++++++++++

Send a series of SNMP GETBULK requests using the following options:

* with SNMPv3, user 'usr-none-none', no authentication, no privacy
* over IPv4/UDP
* to an Agent at localhost:161
* for all OIDs past SNMPv2-MIB::system
* run till end-of-mib condition is reported by Agent
* based on asyncio I/O framework

Functionally similar to:

| $ snmpbulkwalk -v3 -lnoAuthNoPriv -u public -Cn0 -Cr50 \
|                localhost  SNMPv2-MIB::system

"""  #
import asyncio
from pysnmp.hlapi.asyncio import *


async def run(varBinds):
    snmpEngine = SnmpEngine()
    while True:
        errorIndication, errorStatus, errorIndex, varBindTable = await bulkCmd(
            snmpEngine,
            CommunityData("public"),
            UdpTransportTarget(("localhost", 161)),
            ContextData(),
            0,
            50,
            *varBinds
        )
        if errorIndication:
            print(errorIndication)
            break
        elif errorStatus:
            print(
                "{} at {}".format(
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                )
            )
        else:
            for varBindRow in varBindTable:
                for varBind in varBindRow:
                    print(" = ".join([x.prettyPrint() for x in varBind]))

        varBinds = varBindTable[-1]
        if isEndOfMib(varBinds):
            break
    return


asyncio.run(
    run([ObjectType(ObjectIdentity("TCP-MIB")), ObjectType(ObjectIdentity("IP-MIB"))])
)
