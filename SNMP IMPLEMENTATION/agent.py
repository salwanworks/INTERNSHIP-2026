from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import cmdrsp, context
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.proto import rfc1902
from pysnmp.smi import instrum
from pysnmp.smi import builder
from pysnmp.smi import view
from pysnmp.smi import exval


HOST = "127.0.0.1"
PORT = 1161
COMMUNITY = "public"


# ------------------------------------------------------------
# OIDs
# ------------------------------------------------------------

TEMPERATURE = (1, 3, 6, 1, 4, 1, 99999, 1, 1, 0)
RF_POWER = (1, 3, 6, 1, 4, 1, 99999, 1, 2, 0)
ACU_CURRENT = (1, 3, 6, 1, 4, 1, 99999, 1, 3, 0)
BTR_VOLTAGE = (1, 3, 6, 1, 4, 1, 99999, 1, 4, 0)


# ------------------------------------------------------------
# SNMP engine
# ------------------------------------------------------------

snmpEngine = engine.SnmpEngine()


# ------------------------------------------------------------
# UDP transport
# ------------------------------------------------------------

config.add_transport(
    snmpEngine,
    udp.DOMAIN_NAME,
    udp.UdpTransport().open_server_mode(
        (HOST, PORT)
    )
)


# ------------------------------------------------------------
# SNMPv2c
# ------------------------------------------------------------

config.add_v1_system(
    snmpEngine,
    "my-area",
    COMMUNITY
)


# ------------------------------------------------------------
# VACM
# ------------------------------------------------------------

config.add_vacm_user(
    snmpEngine,
    2,
    "my-area",
    "noAuthNoPriv",
    (1, 3, 6, 1, 4, 1, 99999)
)


# ------------------------------------------------------------
# SNMP context
# ------------------------------------------------------------

snmpContext = context.SnmpContext(snmpEngine)


# ------------------------------------------------------------
# Get the MIB instrumentation
# ------------------------------------------------------------

mibInstrum = snmpContext.get_mib_instrum()


# ------------------------------------------------------------
# Create our own simple value store
# ------------------------------------------------------------

values = {

    TEMPERATURE: 725,

    RF_POWER: 3100,

    ACU_CURRENT: 65,

    BTR_VOLTAGE: 278
}


# ------------------------------------------------------------
# Custom instrumentation
# ------------------------------------------------------------

class SimpleMibInstrum:

    def readVars(self, varBinds, acInfo=(None, None)):

        result = []

        for oid, value in varBinds:

            oid_tuple = tuple(oid)

            if oid_tuple in values:

                result.append(
                    (
                        oid,
                        rfc1902.Integer32(
                            values[oid_tuple]
                        )
                    )
                )

            else:

                result.append(
                    (
                        oid,
                        exval.noSuchInstance
                    )
                )

        return result


# ------------------------------------------------------------
# NOTE:
# Use PySNMP's existing instrumentation for the SNMP
# framework. We will register a simple MIB below.
# ------------------------------------------------------------

mibBuilder = (
    snmpContext
    .get_mib_instrum()
    .get_mib_builder()
)


MibScalar, MibScalarInstance = mibBuilder.import_symbols(
    "SNMPv2-SMI",
    "MibScalar",
    "MibScalarInstance"
)


# ------------------------------------------------------------
# Create static MIB objects
# ------------------------------------------------------------

objects = [

    (
        TEMPERATURE,
        725
    ),

    (
        RF_POWER,
        3100
    ),

    (
        ACU_CURRENT,
        65
    ),

    (
        BTR_VOLTAGE,
        278
    )
]


for oid, value in objects:

    scalar = MibScalar(
        oid[:-1],
        rfc1902.Integer32()
    ).setMaxAccess("read-only")


    instance = MibScalarInstance(
        oid[:-1],
        (oid[-1],),
        rfc1902.Integer32(value)
    )


    mibBuilder.export_symbols(
        "__CUSTOM_MIB",
        scalar,
        instance
    )


# ------------------------------------------------------------
# Command responders
# ------------------------------------------------------------

cmdrsp.GetCommandResponder(
    snmpEngine,
    snmpContext
)

cmdrsp.NextCommandResponder(
    snmpEngine,
    snmpContext
)

cmdrsp.BulkCommandResponder(
    snmpEngine,
    snmpContext
)


# ------------------------------------------------------------
# Start
# ------------------------------------------------------------

print("=" * 60)
print("SNMP AGENT")
print("=" * 60)

print(f"Address  : {HOST}:{PORT}")
print(f"Community: {COMMUNITY}")

print()
print("Telemetry:")

print(
    "Temperature : "
    "1.3.6.1.4.1.99999.1.1.0"
)

print(
    "RF Power    : "
    "1.3.6.1.4.1.99999.1.2.0"
)

print(
    "ACU Current : "
    "1.3.6.1.4.1.99999.1.3.0"
)

print(
    "BTR Voltage : "
    "1.3.6.1.4.1.99999.1.4.0"
)

print()
print("SNMP Agent is running...")
print("Press CTRL+C to stop.")

print("=" * 60)


snmpEngine.transport_dispatcher.job_started(1)

try:

    snmpEngine.open_dispatcher()

except KeyboardInterrupt:

    print("\nStopping agent...")

    snmpEngine.close_dispatcher()