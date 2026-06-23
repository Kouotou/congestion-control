from typing import List, Dict


def get_kpi_definitions() -> List[Dict[str, str]]:
    return [
        {
            "name": "Traffic Load",
            "description": "Total incoming request intensity across the platform.",
            "acceptable_range": "0 - 70% of system capacity",
            "critical_threshold": "> 90% of system capacity",
            "qoe_impact": "High load increases response time and may trigger congestion, hurting QoE."
        },
        {
            "name": "Bandwidth",
            "description": "Available transport capacity for network traffic.",
            "acceptable_range": ">= expected traffic throughput",
            "critical_threshold": "< traffic demand",
            "qoe_impact": "Insufficient bandwidth causes packet queuing and increased latency."
        },
        {
            "name": "Throughput",
            "description": "Successful data transfer rate over time.",
            "acceptable_range": ">= 85% of provisioned capacity",
            "critical_threshold": "< 60% of provisioned capacity",
            "qoe_impact": "Low throughput slows page loads and session progress."
        },
        {
            "name": "Latency",
            "description": "Delay for a packet to traverse the network.",
            "acceptable_range": "< 100 ms",
            "critical_threshold": "> 200 ms",
            "qoe_impact": "High latency feels slow and can break interactive sessions."
        },
        {
            "name": "Delay",
            "description": "End-to-end packet delivery delay including processing time.",
            "acceptable_range": "< 120 ms",
            "critical_threshold": "> 250 ms",
            "qoe_impact": "Large delay degrades responsiveness and user experience."
        },
        {
            "name": "Jitter",
            "description": "Variation in packet inter-arrival times.",
            "acceptable_range": "< 30 ms",
            "critical_threshold": "> 75 ms",
            "qoe_impact": "High jitter disrupts streaming and interactive services."
        },
        {
            "name": "Packet Loss",
            "description": "Percentage of dropped packets in transmission.",
            "acceptable_range": "< 0.5%",
            "critical_threshold": "> 2%",
            "qoe_impact": "Packet loss causes retransmissions, slowdowns, and errors."
        },
        {
            "name": "Bit Error Rate (BER)",
            "description": "Ratio of received bits that have errors.",
            "acceptable_range": "<= 10^-6",
            "critical_threshold": "> 10^-4",
            "qoe_impact": "High BER degrades link quality and reduces throughput."
        },
        {
            "name": "Network Utilization",
            "description": "Share of network resources currently in use.",
            "acceptable_range": "< 70%",
            "critical_threshold": "> 90%",
            "qoe_impact": "Overutilization causes congestion and packet delays."
        },
        {
            "name": "Queue Length",
            "description": "Number of packets or requests waiting for service.",
            "acceptable_range": "Low to moderate",
            "critical_threshold": "Large growing queue",
            "qoe_impact": "Long queues increase latency and timeouts."
        },
        {
            "name": "Server CPU Utilization",
            "description": "Percentage of CPU capacity consumed on servers.",
            "acceptable_range": "< 75%",
            "critical_threshold": "> 90%",
            "qoe_impact": "High CPU usage slows application processing."
        },
        {
            "name": "Server Memory Utilization",
            "description": "RAM usage on application servers.",
            "acceptable_range": "< 80%",
            "critical_threshold": "> 95%",
            "qoe_impact": "Memory pressure can cause swapping and instability."
        },
        {
            "name": "Connection Failure Rate",
            "description": "Ratio of failed connection attempts.",
            "acceptable_range": "< 1%",
            "critical_threshold": "> 5%",
            "qoe_impact": "Failure rate directly impacts accessibility and user trust."
        },
        {
            "name": "Session Timeout Rate",
            "description": "Percentage of sessions ending due to timeout.",
            "acceptable_range": "< 2%",
            "critical_threshold": "> 8%",
            "qoe_impact": "Timeouts frustrate users and disrupt workflows."
        },
        {
            "name": "Request Success Rate",
            "description": "Ratio of successful requests to total requests.",
            "acceptable_range": "> 98%",
            "critical_threshold": "< 90%",
            "qoe_impact": "Low success rate means more errors and poor UX."
        },
        {
            "name": "Network Availability",
            "description": "Percentage of time the network is accessible.",
            "acceptable_range": "> 99.5%",
            "critical_threshold": "< 98%",
            "qoe_impact": "Low availability causes service outages and unhappy users."
        },
    ]


def get_kpi_interactions() -> List[Dict[str, str]]:
    return [
        {
            "source": "Bandwidth",
            "target": "Throughput",
            "relationship": "direct",
            "description": "Insufficient bandwidth limits achievable throughput."
        },
        {
            "source": "Latency",
            "target": "QoE",
            "relationship": "inverse",
            "description": "Higher latency reduces QoE."
        },
        {
            "source": "Jitter",
            "target": "QoE",
            "relationship": "inverse",
            "description": "Higher jitter harms real-time experience."
        },
        {
            "source": "Packet Loss",
            "target": "Throughput",
            "relationship": "inverse",
            "description": "Packet loss reduces effective throughput."
        },
        {
            "source": "Server CPU Utilization",
            "target": "Response Time",
            "relationship": "direct",
            "description": "High CPU utilization increases response time."
        },
        {
            "source": "Queue Length",
            "target": "Latency",
            "relationship": "direct",
            "description": "Long queues raise application latency."
        },
        {
            "source": "Request Success Rate",
            "target": "QoE",
            "relationship": "direct",
            "description": "Higher success rates improve QoE."
        },
    ]
