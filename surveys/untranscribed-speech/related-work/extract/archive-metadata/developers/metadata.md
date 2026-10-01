**Source:** *Item Metadata API* — [original page](https://archive.org/developers/metadata.html)

__

  * [ __ .md ](https://archive.org/developers/_sources/metadata.md "Download source file")
  * __ .pdf



__

# Item Metadata API

##  On this page 

  * [Introduction](https://archive.org/developers/metadata.html#introduction)
  * [Item identifiers](https://archive.org/developers/metadata.html#item-identifiers)
  * [Authentication](https://archive.org/developers/metadata.html#authentication)
  * [Compression](https://archive.org/developers/metadata.html#compression)
  * [Metadata Read](https://archive.org/developers/metadata.html#metadata-read)
  * [Metadata Write](https://archive.org/developers/metadata.html#metadata-write)



# Item Metadata API[#](https://archive.org/developers/metadata.html#item-metadata-api "Link to this heading")

## Introduction[#](https://archive.org/developers/metadata.html#introduction "Link to this heading")

Internet Archive organizes its holdings into [items](https://archive.org/developers/items.html), directories of files containing content and metadata. These items are located across a distributed cluster of data nodes.

The Metadata API (MDAPI) permits callers to fetch an item’s various metadata in a single transaction. With the appropriate permissions, a user may also add or update the item’s metadata, and may even store _ad hoc_ JSON data in a transaction-safe manner. MDAPI may be thought of as a digital card catalog for Internet Archive’s holdings.

The API is broken into two conceptual operations: Read and Write. The documentation here mostly focuses on using these operations via its HTTP RESTful endpoint. Details about the internal MDAPI PHP library are explained as well.

## Item identifiers[#](https://archive.org/developers/metadata.html#item-identifiers "Link to this heading")

MDAPI requires a single **item identifier** for all operations. This identifier is a unique string naming the item. (More information on item identifiers may be found [here](https://archive.org/developers/items.html).)

MDAPI cannot operate on more than one item at a time. There is no wildcarding of item identifiers.

## Authentication[#](https://archive.org/developers/metadata.html#authentication "Link to this heading")

Although most information returned by Metadata Read is publicly available, certain [User JSON fields](https://archive.org/developers/md-record.html#md-record-user-json-fields) fields require authorization.

All Metadata Write operations require authorization.

In both cases, the caller may supply either the user’s [S3](https://archive.org/developers/ias3.html) access/secret keys or their Internet Archive HTTP cookies (obtained at interactive login).

Internet Archive’s S3 keys can be sent using the `Authorization: LOW` header. See [S3 Authentication](https://archive.org/developers/iarest.html#iarest-authentication) for more information.

Internet Archive cookies (in particular, `logged-in-user` and `logged-in-sig`) should be sent using the standard HTTP `Cookie:` header.

In general, cookies should only be used by browsers and S3 keys for programmatic access.

## Compression[#](https://archive.org/developers/metadata.html#compression "Link to this heading")

Metadata Read supports response compression to reduce bandwidth.

Clients which support compression should include an `Accept-Encoding: deflate, gzip` header in requests. The client should be prepared to accept compressed or uncompressed content.

See [RFC 7230 Section 4.2](https://tools.ietf.org/html/rfc7230#section-4.2) for more information.

## Metadata Read[#](https://archive.org/developers/metadata.html#metadata-read "Link to this heading")

The Item Metadata Read API is described [here](https://archive.org/developers/md-read.html).

## Metadata Write[#](https://archive.org/developers/metadata.html#metadata-write "Link to this heading")

The Item Metadata Write API is described [here](https://archive.org/developers/md-write.html).

Applications writing metadata should be mindful of concurrency problems when writing metadata. That topic is covered [here](https://archive.org/developers/md-write-adv.html).

[ __ previous ias3 Internet archive S3-like API ](https://archive.org/developers/ias3.html "previous page") [ next Item Metadata API: Read __](https://archive.org/developers/md-read.html "next page")

__On this page

  * [Introduction](https://archive.org/developers/metadata.html#introduction)
  * [Item identifiers](https://archive.org/developers/metadata.html#item-identifiers)
  * [Authentication](https://archive.org/developers/metadata.html#authentication)
  * [Compression](https://archive.org/developers/metadata.html#compression)
  * [Metadata Read](https://archive.org/developers/metadata.html#metadata-read)
  * [Metadata Write](https://archive.org/developers/metadata.html#metadata-write)



By Internet Archive 

© Copyright 2018-2026, Internet Archive.   

