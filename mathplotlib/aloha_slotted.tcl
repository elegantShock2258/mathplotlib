# aloha_slotted.tcl

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

# Simulate slotted aloha by aligning start times with time slots
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
