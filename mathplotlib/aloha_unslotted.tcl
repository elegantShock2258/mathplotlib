# aloha_unslotted.tcl

set ns [new Simulator]
set nf [open aloha.tr w]
$ns trace-all $nf

set node1 [$ns node]
set node2 [$ns node]

$ns duplex-link $node1 $node2 1Mb 10ms DropTail

# Attach UDP to node1
set udp [new Agent/UDP]
$ns attach-agent $node1 $udp

# Null agent at node2
set null [new Agent/Null]
$ns attach-agent $node2 $null

$ns connect $udp $null

# Create CBR traffic, simulate unslotted aloha using random start times
for {set i 0.1} {$i <= 5.0} {set i [expr $i + [expr rand() * 0.5]]} {
    set cbr [new Application/Traffic/CBR]
    $cbr set packetSize_ 500
    $cbr set interval_ 0.05
    $cbr attach-agent $udp
    $ns at $i "$cbr start"
}

$ns at 6.0 "finish"

proc finish {} {
    puts "Simulation done"
    exit 0
}

$ns run
