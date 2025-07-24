import statistics
from collections import defaultdict

class FlowStatsParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.flows = defaultdict(lambda: {
            'sent': 0,
            'recv': 0,
            'drop': 0,
            'send_time': {},
            'recv_time': {},
            'sizes': [],
            'delays': []
        })
        self.stats = {}

    def parse(self):
        with open(self.filepath, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 12:
                    continue

                event, time, layer, pkt_type, size, fid, pid = (
                    parts[0],
                    float(parts[1]),
                    parts[3],
                    parts[4],
                    int(parts[5]),
                    parts[7],
                    parts[11],
                )

                # Destination node from addr field
                addr = parts[10].strip("[]")
                dst_node = addr.split()[1].split(":")[0]
                flow = self.flows[dst_node]

                if event == 's' and layer == 'AGT':
                    flow['sent'] += 1
                    flow['send_time'][pid] = time
                elif event == 'r' and layer == 'AGT':
                    flow['recv'] += 1
                    flow['recv_time'][pid] = time
                    flow['sizes'].append(size)
                    if pid in flow['send_time']:
                        delay = time - flow['send_time'][pid]
                        flow['delays'].append(delay)
                elif event == 'd':
                    flow['drop'] += 1

    def compute(self):
        for flow_id, data in self.flows.items():
            sent = data['sent']
            recv = data['recv']
            drop = data['drop']

            pdr = recv / sent if sent else 0
            drop_rate = drop / sent if sent else 0

            bits = sum(data['sizes']) * 8
            duration = (
                max(data['recv_time'].values()) - min(data['recv_time'].values())
                if data['recv_time']
                else 1
            )
            throughput = (bits / 1000) / duration if duration else 0

            delays = data['delays']
            avg_delay = sum(delays) / len(delays) if delays else 0
            jitter = statistics.stdev(delays) if len(delays) > 1 else 0

            self.stats[flow_id] = {
                "Packets Sent": sent,
                "Packets Received": recv,
                "Packets Dropped": drop,
                "PDR": round(pdr, 3),
                "Drop Rate": round(drop_rate, 3),
                "Throughput (kbps)": round(throughput, 2),
                "Average Delay (s)": round(avg_delay, 5),
                "Jitter (s)": round(jitter, 5),
            }

    def get_stats(self):
        return self.stats

    def print_summary(self):
        print(f"\n{'Flow':<6} {'Sent':<6} {'Recv':<6} {'Drop':<6} {'PDR':<6} {'DropR':<7} {'Thru(kbps)':<12} {'AvgDelay(s)':<14} {'Jitter(s)':<10}")
        for fid, s in self.stats.items():
            print(f"{fid:<6} {s['Packets Sent']:<6} {s['Packets Received']:<6} {s['Packets Dropped']:<6} {s['PDR']:<6} {s['Drop Rate']:<7} "
                  f"{s['Throughput (kbps)']:<12} {s['Average Delay (s)']:<14} {s['Jitter (s)']:<10}")
