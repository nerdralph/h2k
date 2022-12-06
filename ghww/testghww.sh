#!/bin/sh

export QUERY_STRING=`cat QUERY_STRING`

./ghww.py | diff - 1E43D12345.h2k

