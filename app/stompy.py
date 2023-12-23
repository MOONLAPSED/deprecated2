
"""
STOMP
STOMP is a frame based protocol, with frames modelled on HTTP. A frame consists of a command, a set of optional headers and an optional body. STOMP is text based but also allows for the transmission of binary messages. The default encoding for STOMP is UTF-8, but it supports the specification of alternative encodings for message bodies.

Destinations
In STOMP, the concept of a "destination" is central to where messages are sent and from where they are received. A destination is a general term that can refer to different things depending on the message broker's implementation. For example, in some brokers, a destination might be a queue where messages are stored until a consumer retrieves them. In others, it might be a topic used for publish-subscribe messaging, where messages are immediately broadcast to all subscribed consumers.

Opaque Strings
STOMP treats destination identifiers as "opaque strings," meaning that the protocol doesn't assign any structure or inherent meaning to these strings. They are just sequences of characters that are meaningful to the server. For instance, one server could use a destination string like "/queue/orders" to represent a queue for order messages, while another server might have a different naming convention or hierarchy.

Server Implementation Specific Syntax
Because STOMP doesn't enforce any particular structure for destinations, each server can define its own syntax for them. This means that the format of the destination strings can vary widely from one STOMP server to another. For instance, one server might use a URL-like structure while another might use a filesystem-like path.

Delivery Semantics
Delivery semantics, or "message exchange" semantics, define the rules or behaviors associated with message delivery when using a destination. STOMP itself does not specify what these semantics should be. Therefore, it is up to each STOMP server to implement its own semantics for handling messages.

For example, some possible delivery semantics include:

Retaining messages in a queue until they are explicitly acknowledged by a consumer.
Broadcasting messages to all active subscribers of a topic.
Storing messages persistently so they can be retrieved later, even if the consumer is not currently connected.
Flexibility for Server Implementations
Because STOMP does not strictly define destination syntax and delivery semantics, STOMP servers have the flexibility to support a variety of behaviors. This flexibility allows STOMP to be used in creative and varied ways that suit the needs of different applications.

For example, a broker could implement a destination that behaves like a topic for some clients and like a queue for others. Or it might support more advanced scenarios like message prioritization, delayed delivery, or filtering based on content or headers.



"""

"""rfc2616_stomp_client.py
A STOMP client is a user-agent which can act in two (possibly simultaneous) modes:

    as a producer, sending messages to a destination on the server via a SEND frame

    as a consumer, sending a SUBSCRIBE frame for a given destination and receiving messages from the server as MESSAGE frames.
"""

"""
Value Encoding

The commands and headers are encoded in UTF-8. All frames except the CONNECT and CONNECTED frames will also escape any carriage return, line feed or colon found in the resulting UTF-8 encoded headers.

Escaping is needed to allow header keys and values to contain those frame header delimiting octets as values. The CONNECT and CONNECTED frames do not escape the carriage return, line feed or colon octets in order to remain backward compatible with STOMP 1.0.

C style string literal escapes are used to encode any carriage return, line feed or colon that are found within the UTF-8 encoded headers. When decoding frame headers, the following transformations MUST be applied:

    \r (octet 92 and 114) translates to carriage return (octet 13)
    \n (octet 92 and 110) translates to line feed (octet 10)
    \c (octet 92 and 99) translates to : (octet 58)
    \\ (octet 92 and 92) translates to \ (octet 92)

Undefined escape sequences such as \t (octet 92 and 116) MUST be treated as a fatal protocol error. Conversely when encoding frame headers, the reverse transformation MUST be applied.
"""