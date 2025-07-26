class Axes:
    def __init__(self):
        print("jo")
    def Xaxis(self):
        return """set ns [new Simulator]
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
    
    def Yaxis(self):
        return """
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
    def Zaxis(self):
        return """
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

    def setAxisScale(self):
        return """
set ns [new Simulator]
set tracefile [open "star.tr" w]
$ns trace-all $tracefile

set numNodes 5
set rootNode [$ns node]

for {set i 0} {$i < $numNodes} {incr i} {
    set node($i) [$ns node]
    $ns duplex-link $node($i) $rootNode 10ms 1Mb DropTail

    set udp($i) [new Agent/UDP]
    set null($i) [new Agent/Null]

    $ns attach-agent $node($i) $udp($i)
    $ns attach-agent $rootNode $null($i)

    $ns connect $udp($i) $null($i)

    set cbr($i) [new Application/Traffic/CBR]
    $cbr($i) set packetSize_ 500
    $cbr($i) set interval_ 0.05
    $cbr($i) attach-agent $udp($i)

    $ns at 0.5 "$cbr($i) start"
    $ns at 5.0 "$cbr($i) stop"
}

proc finish {} {
    puts "Star topology simulation finished"
    global tracefile ns
    $ns flush-trace
    close $tracefile
    exit 0
}
$ns at 6.0 "finish"
$ns run
"""
    def setAxisTicks(self):
        return """
set ns [new Simulator]
set tracefile [open "ring.tr" w]
$ns trace-all $tracefile
set namfile [open "ring.nam" w]
$ns namtrace-all $namfile

set numNodes 100

for {set i 0} {$i < $numNodes} {incr i} {
    set node($i) [$ns node]
}

for {set i 0} {$i < $numNodes} {incr i} {
    $ns duplex-link $node($i) $node([expr ($i+1)%$numNodes]) 10ms 1Mb DropTail
}


for {set i 0} {$i < $numNodes} {incr i} {
    set tcp($i) [new Agent/UDP]
    set NullNode($i) [new Agent/Null]
    
    $ns attach-agent $node(0) $tcp($i)
    $ns attach-agent $node($i) $NullNode($i)
    $ns connect $tcp($i) $NullNode($i)

    set cbr($i) [new Application/Traffic/CBR]
    $cbr($i) set packetSize_ 200
    $cbr($i) set interval_ 0.01
    $cbr($i) attach-agent $tcp($i)
    
    $ns at 0.5 "$cbr($i) start"
    $ns at 5.0 "$cbr($i) stop"
}


proc finish {} {
    puts "ring finish"
    global tracefile ns
    global namfile ns
    $ns flush-trace
    close $tracefile
    close $namfile 
    exit 0 
}

$ns at 6.0 "finish"
$ns run 
"""