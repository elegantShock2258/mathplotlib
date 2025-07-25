# Get arguments from command line
if {$argc != 2} {
    puts "Usage: ns test_configurable.tcl <protocol: 0=TCP, 1=UDP> <packet_size>"
    exit 1
}

set protocol [lindex $argv 0]
set packet_size [lindex $argv 1]

# Validate
if {![string is integer -strict $protocol] || ($protocol != 0 && $protocol != 1)} {
    puts "Error: protocol must be 0 (TCP) or 1 (UDP)"
    exit 1
}

if {![string is integer -strict $packet_size] || $packet_size <= 0} {
    puts "Error: packet_size must be a positive integer"
    exit 1
}

# Setup
set ns [new Simulator]
set proto_str [expr {$protocol == 0 ? "tcp" : "udp"}]
set trace_file "test.${proto_str}_${packet_size}bytes.tr"
set tf [open $trace_file w]
$ns trace-all $tf

# Nodes
set n0 [$ns node]
set n1 [$ns node]

$ns duplex-link $n0 $n1 1Mb 10ms DropTail

# Agents
if {$protocol == 0} {
    set src [new Agent/TCP]
    set dst [new Agent/TCPSink]
} else {
    set src [new Agent/UDP]
    set dst [new Agent/Null]
}

$ns attach-agent $n0 $src
$ns attach-agent $n1 $dst
$ns connect $src $dst

# CBR App
set app [new Application/Traffic/CBR]
$app set packetSize_ $packet_size
$app set interval_ 0.05
$app attach-agent $src

# Schedule
$ns at 0.5 "$app start"
$ns at 5.0 "$app stop"
$ns at 6.0 "finish"

proc finish {} {
    global tf ns
    $ns flush-trace
    close $tf
    exit 0
}

$ns run
