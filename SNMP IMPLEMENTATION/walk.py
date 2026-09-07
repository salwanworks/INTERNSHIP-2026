import asyncio

from pysnmp.hlapi.v3arch.asyncio import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    walk_cmd
)


HOST = "127.0.0.1"
PORT = 1161

COMMUNITY = "public"

BASE_OID = "1.3.6.1.4.1.99999.1"


async def main():

    print("=" * 60)
    print("SNMP WALK")
    print("=" * 60)

    print(
        f"Walking: {BASE_OID}"
    )

    print()


    async for (
        error_indication,
        error_status,
        error_index,
        var_binds
    ) in walk_cmd(

        SnmpEngine(),

        CommunityData(COMMUNITY),

        await UdpTransportTarget.create(
            (HOST, PORT)
        ),

        ContextData(),

        ObjectType(
            ObjectIdentity(BASE_OID)
        )
    ):

        if error_indication:

            print(
                "Error:",
                error_indication
            )

            break


        if error_status:

            print(
                "Error:",
                error_status.prettyPrint()
            )

            break


        for oid, value in var_binds:

            print(
                f"{oid} = {value.prettyPrint()}"
            )


asyncio.run(main())