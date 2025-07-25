aloha_slot_tcl="""
set ns [new Simulator]
set nf [open aloha_slotted.tr w]
$ns trace-all $nf

set node1 [$ns node]
set node2 [$ns node]

$ns duplex-link $node1 $node2 1Mb 10ms DropTail

set udp [new Agent/UDP]
$ns attach-agent $node1 $udp

set null [new Agent/Null]
$ns attach-agent $node2 $null
$ns connect $udp $null

set slot_time 0.2
for {set i 0.5} {$i < 5.0} {set i [expr $i + $slot_time]} {
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
"""

aloha_unslot_tcl="""
set ns [new Simulator]
set nf [open aloha.tr w]
$ns trace-all $nf

set node1 [$ns node]
set node2 [$ns node]

$ns duplex-link $node1 $node2 1Mb 10ms DropTail

set udp [new Agent/UDP]
$ns attach-agent $node1 $udp

set null [new Agent/Null]
$ns attach-agent $node2 $null

$ns connect $udp $null

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
"""

csma_tcl="""
set ns [new Simulator]
set nf [open csma.tr w]
$ns trace-all $nf

set topo [new Topography]
$topo load_flatgrid 500 500

create-god 2

$ns node-config -adhocRouting DSDV \
    -llType LL \
    -macType Mac/802_11 \
    -ifqType Queue/DropTail \
    -ifqLen 50 \
    -antType Antenna/OmniAntenna \
    -propType Propagation/TwoRayGround \
    -phyType Phy/WirelessPhy \
    -channelType Channel/WirelessChannel \
    -topoInstance $topo \
    -agentTrace ON \
    -routerTrace ON \
    -macTrace ON

set n1 [$ns node]
set n2 [$ns node]

$n1 set X_ 100; $n1 set Y_ 100; $n1 set Z_ 0
$n2 set X_ 150; $n2 set Y_ 100; $n2 set Z_ 0

$ns initial_node_pos $n1 20
$ns initial_node_pos $n2 20

set udp [new Agent/UDP]
$ns attach-agent $n1 $udp

set null [new Agent/Null]
$ns attach-agent $n2 $null
$ns connect $udp $null

set cbr [new Application/Traffic/CBR]
$cbr set packetSize_ 512
$cbr set interval_ 0.1
$cbr attach-agent $udp

$ns at 0.5 "$cbr start"
$ns at 5.0 "$cbr stop"
$ns at 6.0 "finish"

proc finish {} {
    puts "CSMA simulation done"
    exit 0
}

$ns run
"""