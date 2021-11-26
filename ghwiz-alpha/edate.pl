#!/usr/bin/perl

# globals
$indent="    ";
$ftperm=3.28084;
$sfpersm=$ftperm**2;

sub cat {
    open(FH, '<', shift(@_));
    while ($line = <FH>) {print ("$line")}
}

cat("header.ghw");

chomp($evaldate=`date -I --date='7 days ago'`);
print("$indent<File evaluationDate=\"$evaldate\">");
