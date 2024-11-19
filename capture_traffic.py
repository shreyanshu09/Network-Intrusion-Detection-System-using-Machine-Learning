import scapy.all as scapy
import pandas as pd
from scapy.layers import http

def extract_features(packet):
    # Initialize feature dictionary
    features = {
        'duration': 0, 'protocol_type': '', 'service': '', 'flag': '',
        'src_bytes': 0, 'dst_bytes': 0, 'land': 0, 'wrong_fragment': 0,
        'urgent': 0, 'hot': 0, 'num_failed_logins': 0, 'logged_in': 0,
        'num_compromised': 0, 'root_shell': 0, 'su_attempted': 0, 'num_root': 0,
        'num_file_creations': 0, 'num_shells': 0, 'num_access_files': 0,
        'num_outbound_cmds': 0, 'is_host_login': 0, 'is_guest_login': 0,
        'count': 0, 'srv_count': 0, 'serror_rate': 0, 'srv_serror_rate': 0,
        'rerror_rate': 0, 'srv_rerror_rate': 0, 'same_srv_rate': 0,
        'diff_srv_rate': 0, 'srv_diff_host_rate': 0, 'dst_host_count': 0,
        'dst_host_srv_count': 0, 'dst_host_same_srv_rate': 0,
        'dst_host_diff_srv_rate': 0, 'dst_host_same_src_port_rate': 0,
        'dst_host_srv_diff_host_rate': 0, 'dst_host_serror_rate': 0,
        'dst_host_srv_serror_rate': 0, 'dst_host_rerror_rate': 0,
        'dst_host_srv_rerror_rate': 0
    }

    if packet.haslayer(scapy.IP):
        features['protocol_type'] = packet[scapy.IP].proto
        features['src_bytes'] = len(packet[scapy.IP])
        features['dst_bytes'] = len(packet[scapy.IP].payload)

    if packet.haslayer(scapy.TCP):
        features['service'] = packet[scapy.TCP].dport
        features['flag'] = packet[scapy.TCP].flags

    # Add more feature extraction logic here based on your specific requirements

    return features

def capture_traffic(duration, output_file):
    print(f"Capturing traffic for {duration} seconds...")
    packets = scapy.sniff(timeout=duration)
    
    data = []
    for packet in packets:
        features = extract_features(packet)
        data.append(features)
    
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Captured traffic saved to {output_file}")

# if __name__ == "__main__":
#     capture_duration = 60  # Capture for 60 seconds
#     output_file = "captured_traffic.csv"
#     capture_traffic(capture_duration, output_file)