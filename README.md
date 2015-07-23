# dnsprox

A small, simple and configurable DNS server written in Python

## Overview

dnsprox is a small DNS server with the express intent of intercepting and modifying DNS queries. dnsprox will read rules, in zone format, from both command line and a config file, and respond to any matching queries with the provided response, or proxy the request to a "real" name server. This is mostly helpful for security and application testing.

## Usage

*	Start the server
``
$ ./dnsprox -p 1053 "*.google.com IN A 1.2.3.4"
``

*	Query the server
``
$ dig @localhost -p 1053 www.google.com +short
1.2.3.4
$ dig @localhost -p 1053 www.facebook.com +short
star.c10r.facebook.com.
31.13.74.1
``