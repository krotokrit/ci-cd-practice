import re

# network_id         DONE
# binary_network_id  DONE
# mask               DONE
# binary_mask        DONE
# broadcast_ip       DONE
# first_host_ip      DONE
# last_host_ip       DONE
# number_of_hosts    DONE
# next_network_id    DONE

class Network:
    def __init__(self, ip: str, mask_prefix: str):
        self.mask = mask_prefix
        try:
            self.binary_network_id = self.submask_network(ip, mask_prefix)
        except ValueError as e:
            raise ValueError("Invalid input: IP must be in format ***.***.***.***, mask format must be /<number>") from e

    def check_ip_mask_format(self, ip: str, mask_prefix: str):
        mask_pattern = r"^/(?:[1-9]|[12][0-9]|3[0-2])$"

        ip_pattern = (
            r"^(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\."
            r"(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\."
            r"(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})\."
            r"(25[0-5]|2[0-4][0-9]|1?[0-9]{1,2})$"
        )
        if not (re.match(ip_pattern, ip) and re.match(mask_pattern, mask_prefix)):
            raise ValueError
        prefix = int(mask_prefix[1:])
        self.number_of_hosts = 2 ** (32 - prefix) - 2

    def decimal_to_binary(self, number: int):
        binary_number = ""
        while number > 0:
            binary_number += str(number % 2)
            number //= 2
        if binary_number == "":
            binary_number = "0"
        for i in range(0, 8 - len(binary_number)):
            binary_number += "0"
        return binary_number[::-1]

    def binary_to_decimal(self, number: str):
        result_num = 0
        for i in range(len(number)):
            result_num += (2 ** (7 - i)) if number[i] == "1" else 0
        return result_num

    def prefix_to_binary(self, mask: int):
        binary_mask = '1' * mask + '0' * (32 - mask)
        parts = [binary_mask[i:i+8] for i in range(0, 32, 8)]
        self.binary_mask = ".".join(parts)
        return parts


    def get_network_id(self, binary_prefix_parts, binary_ip_parts):
        network_id = ""
        for i in range(4):
            temp = ""
            for j in range(8):
                temp += "1" if (binary_prefix_parts[i][j] == "1" and binary_ip_parts[i][j] == "1") else "0"
            network_id += temp + "."
        return network_id[:-1]

    def binary_parts_to_decimal_ip(self, binary_parts):
        decimal_parts = []
        for part in binary_parts:
            decimal_parts.append(str(self.binary_to_decimal(part)))
        return ".".join(decimal_parts)

    def get_broadcast_ip(self, binary_network_id, prefix):
        flat_bin = "".join(binary_network_id.split("."))
        broadcast_bin = flat_bin[:prefix] + '1' * (32 - prefix)
        broadcast_parts = [broadcast_bin[i:i+8] for i in range(0, 32, 8)]
        return self.binary_parts_to_decimal_ip(broadcast_parts)

    def add_one_to_binary_ip(self, binary_ip):
        bin_str = "".join(binary_ip.split("."))
        int_ip = int(bin_str, 2) + 1
        padded_bin = bin(int_ip)[2:].zfill(32)
        return [padded_bin[i:i+8] for i in range(0, 32, 8)]

    def subtract_one_from_binary_ip(self, binary_ip):
        bin_str = "".join(binary_ip.split("."))
        int_ip = int(bin_str, 2) - 1
        padded_bin = bin(int_ip)[2:].zfill(32)
        return [padded_bin[i:i+8] for i in range(0, 32, 8)]

    def submask_network(self, ip: str, mask_prefix: str):
        self.check_ip_mask_format(ip, mask_prefix)
        ip_parts = ip.split(".")
        binary_ip_parts = []

        for i in ip_parts:
            binary_ip_parts.append(self.decimal_to_binary(int(i)))

        binary_prefix_parts = self.prefix_to_binary(int(mask_prefix[1:]))
        binary_network_id = self.get_network_id(binary_prefix_parts, binary_ip_parts)
        splited_binary_network_id = binary_network_id.split(".")

        decimal_network_id = []
        for i in splited_binary_network_id:
            decimal_network_id.append(self.binary_to_decimal(i))

        self.network_id = ".".join(str(i) for i in decimal_network_id)

        broadcast_parts = self.get_broadcast_ip(binary_network_id, int(mask_prefix[1:])).split(".")
        self.broadcast_ip = ".".join(broadcast_parts)

        first_host_bin = self.add_one_to_binary_ip(binary_network_id)
        self.first_host_ip = self.binary_parts_to_decimal_ip(first_host_bin)

        broadcast_binary_parts = [self.decimal_to_binary(int(part)) for part in broadcast_parts]
        last_host_bin = self.subtract_one_from_binary_ip(".".join(broadcast_binary_parts))

        self.last_host_ip = self.binary_parts_to_decimal_ip(last_host_bin)

        broadcast_bin_str = "".join(broadcast_binary_parts)
        next_network_int = int(broadcast_bin_str, 2) + 1
        next_network_bin = bin(next_network_int)[2:].zfill(32)

        next_network_parts = [next_network_bin[i:i+8] for i in range(0, 32, 8)]
        self.next_network_id = self.binary_parts_to_decimal_ip(next_network_parts)

        return binary_network_id
