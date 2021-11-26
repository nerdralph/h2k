#!/usr/bin/perl

# globals
$indent="    ";
$crlf = "\r\n";
$FTPERM=3.28084;
$SFPERSM=$FTPERM**2;

sub cat {
    open(FH, '<', shift(@_));
    while ($line = <FH>) {print ("$line")}
}

cat("header.ghw");

chomp($evaldate=`date -I --date='7 days ago'`);
print("$indent<File evaluationDate=\"$evaldate\">$crlf");

cat("fileid.ghw");

print("$indent<FacingDirection code=\"$ARGV[0]\" />$crlf");
print("$indent<YearBuilt code=\"1\" value=\"$ARGV[1]\" />$crlf");

$operim=$ARGV[2]; $oarea=$ARGV[3];

# calculate foundation and main floor area converted to metric
$marea=($oarea-$operim/2+1)/$SFPERSM;
$farea=($oarea-$operim+4)/$SFPERSM;
=pod comment
print("marea: $marea");
=cut
print($indent . '<HeatedFloorArea aboveGrade="' . $marea);
print('" belowGrade="' . $farea . '" />' . $crfl);

cat("specs.ghw");

# calculate volume 7.75ft bsmt + header + 8ft main flr
$volume=(7.75/$FTPERM * $farea) + (1 + 8)/$FTPERM * $marea;

print($indent . '<House volume="' . $volume . '" />' . $crfl);
cat("ach.ghw");

# use 12ft (3.66m) for now
print($indent . '<BuildingSite highestCeiling="3.66">' . $crfl);

cat("hvac.ghw");

#interior perimeter in m
$iperimm=($operim-4)/$FTPERM;

# ceiling
print($indent . '<Measurements length="' . $iperim/2);
print('" area="' . $marea . '" heelHeight="0.1311">' . $crlf);

cat("mwall.ghw");
print($indent . '<Measurements height="2.4384" perimeter="' . $iperimm . '" />' . $crlf);

cat("bsmt.ghw");
#1.22m = 4ft
print($indent . '<Measurements height="2.3622" perimeter="' . ($iperimm -1.22) . '" />' . $crlf);

cat("bwall.ghw");
cat("dhw.ghw");
cat("codes.ghw");
cat("fuel.ghw");

