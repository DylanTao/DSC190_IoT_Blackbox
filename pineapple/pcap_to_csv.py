import socket
import dpkt
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pcap_to_csv.py <pcap_file>")
        sys.exit(1)

    with open(sys.argv[1], "rb") as f:
        pcap = dpkt.pcap.Reader(f)
        print(
            "timestamp,type,source_ip,source_port,destination_ip,destination_port,protocol,packet_size"
        )

        for ts, buf in pcap:
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                ip = eth.data
                if not isinstance(ip, dpkt.ip.IP):
                    continue
                src_ip = socket.inet_ntoa(ip.src)
                dst_ip = socket.inet_ntoa(ip.dst)
                protocol = ip.p

                if isinstance(ip.data, dpkt.tcp.TCP):
                    src_port = ip.data.sport
                    dst_port = ip.data.dport
                    packet_size = len(ip.data.data)
                    print(
                        f"{ts},IP,{src_ip},{src_port},{dst_ip},{dst_port},{protocol},{packet_size}"
                    )

                elif isinstance(ip.data, dpkt.udp.UDP):
                    src_port = ip.data.sport
                    dst_port = ip.data.dport
                    packet_size = len(ip.data.data)
                    print(
                        f"{ts},IP,{src_ip},{src_port},{dst_ip},{dst_port},{protocol},{packet_size}"
                    )

            except:
                continue
