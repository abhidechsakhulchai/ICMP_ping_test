# ICMP_ping_test
<p>
In this lab, you will gain a better understanding of Internet Control Message Protocol (ICMP). You
will learn to implement a Ping application using ICMP request and reply messages.
Ping is a computer network application used to test whether a particular host is reachable across an IP
network. It is also used to self-test the network interface card of the computer or as a latency test. It
works by sending ICMP “echo reply” packets to the target host and listening for ICMP “echo reply”
replies. The "echo reply" is sometimes called a pong. Ping measures the round-trip time, records packet
loss, and prints a statistical summary of the echo reply packets received (the minimum, maximum, and
the mean of the round-trip times and in some versions the standard deviation of the mean).
Your task is to develop your own Ping application in Python. Your application will use ICMP but, in
order to keep it simple, will not exactly follow the official specification in RFC 1739. Note that you will
only need to write the client side of the program, as the functionality needed on the server side is built
into almost all operating systems.
You should complete the Ping application so that it sends ping requests to a specified host separated by
approximately one second. Each message contains a payload of data that includes a timestamp. After
sending each packet, the application waits up to one second to receive a reply. If one second goes by
without a reply from the server, then the client assumes that either the ping packet or the pong packet
was lost in the network (or that the server is down).   
</p>
<h3>Credit by <em>https://files.transtutors.com/cdn/uploadassignments/429178_1_socket5-icmppinger.pdf</em> </h3>

# Internet Control Message Protocol (ICMP)
ICMP Header
The ICMP header starts after bit 160 of the IP header (unless IP options are used).
<ul>
  <li>Type : ICMP type. </li>
  <li>Code : Subtype to the given ICMP type.</li>
  <li>Checksum : Error checking data calculated from the ICMP header + data, with value 0 for this field.</li>
  <li>ID - An ID value, should be returned in the case of echo reply.</li>
  <li>Sequence - A sequence value, should be returned in the case of echo reply.</li>
</ul>

# Echo Request
The echo request is an ICMP message whose data is expected to be received back in an echo reply ("pong"). The host must respond to all echo requests with an echo reply containing the exact data received in the request message.
<ul>
  <li>Type must be set to 8.</li>
  <li>Code must be set to 0.</li>
  <li>The Identifier and Sequence Number can be used by the client to match the reply with the request that caused the reply. In practice, most Linux systems use a unique identifier for every ping process, and sequence number is an increasing number within that process. Windows uses a fixed identifier, which varies between Windows versions, and a sequence number that is only reset at boot time.</li>
  <li>The data received by the echo request must be entirely included in the echo reply.</li>
</ul>

# Echo Reply
The echo reply is an ICMP message generated in response to an echo request, and is mandatory for all hosts and routers.
<ul>
  <li>Type and code must be set to 0.</li>
  <li>The identifier and sequence number can be used by the client to determine which echo requests are associated with the echo replies.</li>
  <li>The data received in the echo request must be entirely included in the echo reply.</li>
</ul>

