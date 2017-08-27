#!/usr/bin/perl -w

use DB_File;

$addrdb=$ARGV[0]
    || "$ENV{HOME}/.evolution/addressbook/local/system/addressbook.db";
print "* Examining $addrdb\n";

tie %h, 'DB_File', $addrdb, O_RDWR, 0777, $DB_HASH
  or die "Error opening file: $!\n";

# Keep track of names we've seen
%names=();

for $k (keys %h) {
    $card=$h{$k};
    if ($card =~ /^FN:(.*)$/m) {
        $name=$1;
        $name=~s/\r//g;
        chomp $name;
        if (exists($names{$name})) {
            print "* Previously found $name, removing\n";
            delete $h{$k};
        }
        $names{$name}++;
    }
}

print "* Done. Duplicate statistics:\n";
print join("\n", map { "$_: $names{$_} times" } 
           sort { $names{$b} <=> $names{$a} } 
           grep { $names{$_} > 1 } keys %names
          )."\n";
