#!/bin/sh

export QUERY_STRING=`cat QUERY_STRING`

echo diff:
./ghww.py | diff - 0000D12345.h2k

