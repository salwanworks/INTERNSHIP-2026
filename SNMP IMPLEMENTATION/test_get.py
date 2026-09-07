import asyncio

from pysnmp.hlapi.v3arch.asyncio import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    get_cmd
)


async def main():

    oid = "1.3.6.1.4.1.99999.1.1.0"

    print("Testing:")
    print(oid)
    print()

    (
        error_indication,
        error_status,
        error_index,
        var_binds
    ) = await get_cmd(

        SnmpEngine(),

        CommunityData("public"),

        await UdpTransportTarget.create(
            ("127.0.0.1", 1161)
        ),

        ContextData(),

        ObjectType(
            ObjectIdentity(oid)
        )
    )


    print("error_indication =", error_indication)
    print("error_status     =", error_status)
    print("error_index      =", error_index)

    print()

    for var_bind in var_binds:

        print(
            var_bind[0],
            "=",
            var_bind[1]
        )


asyncio.run(main())