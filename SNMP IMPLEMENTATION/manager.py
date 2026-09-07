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


HOST = "127.0.0.1"
PORT = 1161

COMMUNITY = "public"


# ============================================================
# OIDs
# ============================================================

TEMPERATURE_OID = "1.3.6.1.4.1.99999.1.1.0"

RF_POWER_OID = "1.3.6.1.4.1.99999.1.2.0"

ACU_CURRENT_OID = "1.3.6.1.4.1.99999.1.3.0"

BTR_VOLTAGE_OID = "1.3.6.1.4.1.99999.1.4.0"


# ============================================================
# SNMP GET
# ============================================================

async def get_value(oid):

    error_indication, error_status, error_index, var_binds = (
        await get_cmd(

            SnmpEngine(),

            CommunityData(COMMUNITY),

            await UdpTransportTarget.create(
                (HOST, PORT)
            ),

            ContextData(),

            ObjectType(
                ObjectIdentity(oid)
            )
        )
    )


    if error_indication:

        print("SNMP Error:", error_indication)
        return None


    if error_status:

        print(
            "SNMP Error:",
            error_status.prettyPrint()
        )

        return None


    for var_bind in var_binds:

        return int(var_bind[1])


# ============================================================
# Main
# ============================================================

async def main():

    print("=" * 60)
    print("SNMP MANAGER")
    print("=" * 60)

    print(
        f"Connecting to {HOST}:{PORT}"
    )

    print()


    # Temperature

    temperature = await get_value(
        TEMPERATURE_OID
    )


    # RF Power

    rf_power = await get_value(
        RF_POWER_OID
    )


    # ACU Current

    acu_current = await get_value(
        ACU_CURRENT_OID
    )


    # BTR Voltage

    btr_voltage = await get_value(
        BTR_VOLTAGE_OID
    )


    # ========================================================
    # Display telemetry
    # ========================================================

    print("Telemetry:")
    print("-" * 60)


    if temperature is not None:

        print(
            f"HPA Temperature : "
            f"{temperature / 10:.1f} °C"
        )


    if rf_power is not None:

        print(
            f"RF Power        : "
            f"{rf_power} W"
        )


    if acu_current is not None:

        print(
            f"ACU Current     : "
            f"{acu_current / 10:.1f} A"
        )


    if btr_voltage is not None:

        print(
            f"BTR Voltage     : "
            f"{btr_voltage / 10:.1f} V"
        )


    print("-" * 60)


asyncio.run(main())