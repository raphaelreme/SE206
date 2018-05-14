#!/bin/sh

PACKAGES='satispy funcparserlib'

for PACK in $PACKAGES; do
    echo $PACK
    pip3 install --user $PACK
done
