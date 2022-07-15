#!/usr/bin/perl
# Ralph Doncaster 2022
# add Prev. File ID from parsed mailbot warnings 

while (<STDIN>) {
    if (/suspected duplicate/) {
        $d = (split / /)[2]; <STDIN>;
        $prev_id = (split /\(/,<STDIN>)[0];
        $cmd = 'sed -i \'s/sFileID value="/sFileID value="';
        system( $cmd . $prev_id . "/' $d.h2k\n"); 
        print ("$d - added prev. ID $prev_id\n");
    }
}

