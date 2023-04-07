#!/usr/bin/env python3
"""
SNMPv1
++++++

Send SNMP GET request using the following options:

  * with SNMPv1, community 'public'
  * over IPv4/UDP
  * to an Agent at localhost:161
  * for an instance of SNMPv2-MIB::sysDescr.0 MIB object
  * Based on asyncio I/O framework

Functionally similar to:

| $ snmpget -v1 -c public localhost SNMPv2-MIB::sysDescr.0

"""  #
import asyncio
from pysnmp.hlapi.asyncio import *


async def run():
    snmpEngine = SnmpEngine()
    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(
        snmpEngine,
        CommunityData("public", mpModel=0),
        UdpTransportTarget(("localhost", 161)),
        ContextData(),
        ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
    )

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))

    snmpEngine.transportDispatcher.closeDispatcher()


asyncio.run(run())
