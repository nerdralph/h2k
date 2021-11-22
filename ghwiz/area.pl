#!/usr/bin/perl

$operim=$ARGV[0];
$oarea=$ARGV[1];

$marea=($oarea-$operim/2+1)/3.28**2;
$farea=$oarea-$operim+4;
print "marea: $marea\n";
print "farea: $farea\n";

system("cat header.ghw");

