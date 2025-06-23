from network import Network

def test():
    network = Network("192.168.156.3", "/21")

    assert network.network_id == "192.168.152.0"
    assert network.mask == "/21"
    assert network.binary_mask == "11111111.11111111.11111000.00000000"
    assert network.broadcast_ip == "192.168.159.255"
    assert network.first_host_ip == "192.168.152.1"
    assert network.last_host_ip == "192.168.159.254"
    assert network.number_of_hosts == 2046
    assert network.next_network_id == "192.168.160.0"

