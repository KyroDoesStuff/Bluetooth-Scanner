
import asyncio
from bleak import BleakScanner

devices_found = {}


def get_manufacturer_names(manufacturer_data):
    company_names = {
        6: "Microsoft",
        76: "Apple",
        16972: "Unknown / unverified",
        3275: "Nothing Technology Limited",
    }

    names = []

    for company_id in manufacturer_data:
        company = company_names.get(
            company_id,
            "Unknown manufacturer"
        )
        names.append(company)

    return ", ".join(names) if names else "Unknown"


def identify_device(name, manufacturers, services):
    if name != "Unknown":
        return f"Name advertised: {name}"

    if manufacturers:
        return "Manufacturer data available; model unknown"

    if services:
        return "Services available; model unknown"

    return "Insufficient advertising data"



def detect(device, ad_data):
    name = ad_data.local_name or device.name or "Unknown"

    devices_found[device.address] = {
        "name": name,
        "rssi": ad_data.rssi,
        "manufacturers": list(ad_data.manufacturer_data.keys()),
        "possible_manufacturer": get_manufacturer_names(
            ad_data.manufacturer_data
        ),
        "manufacturer_data": ad_data.manufacturer_data.copy(),
        "services": sorted(set(ad_data.service_uuids)),
    }



async def main():
    devices_found.clear()

    print("=" * 48)
    print("          BLUETOOTH SCANNER")
    print("=" * 48)
    print("Scanning for 8 seconds...\n")

    scanner = BleakScanner(detect)

    await scanner.start()
    await asyncio.sleep(8.0)
    await scanner.stop()

    sorted_devices = sorted(
        devices_found.items(),
        key=lambda item: (
            item[1]["rssi"]
            if item[1]["rssi"] is not None else -999
        ),
        reverse=True
    )

    print("SCAN RESULTS")
    print("-" * 48)

    if not sorted_devices:
        print("No BLE devices discovered.")
    else:
        for index, (address, info) in enumerate(sorted_devices, start=1):
            print(f"[{index}] {info['name']}")
            print(f"    Address      : {address}")

            rssi = info["rssi"]
            signal = f"{rssi} dBm" if rssi is not None else "Unknown"
            print(f"    Signal       : {signal}")

            manufacturers = info["manufacturers"]
            manufacturer_text = (
                ", ".join(str(company_id) for company_id in manufacturers)
                if manufacturers else "Not advertised"
            )
            print(f"    Company IDs  : {manufacturer_text}")

            print(
                f"    Possible device manufacturer: "
                f"{info['possible_manufacturer']}"
            )

            print(
                f"    Identification: "
                f"{identify_device(info['name'], info['manufacturers'], info['services'])}"
            )

            services = info["services"]
            service_text = (
                ", ".join(services) if services else "None advertised"
            )
            print(f"    Service UUIDs: {service_text}")
            print("-" * 48)

    print(f"Total unique addresses: {len(devices_found)}")
    print("=" * 48)


if __name__ == "__main__":
    asyncio.run(main())
