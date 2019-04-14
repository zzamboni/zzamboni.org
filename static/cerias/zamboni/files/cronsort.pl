eval 'exec perl -x $0 ${1+"$@"}' # -*-perl-*-
  if 0;
#!perl -w
# Sort a crontab by time
# Each entry (possibly commented) is moved as a block with all the
# comment lines before it.
# Diego Zamboni, March 21, 2001. Happy Spring!

use strict;
use vars qw($curblock $tf @fields @db);

# Regex for a time field in crontab, which can be a number, sequence of numbers
# or an asterisk
$tf='(?:[*]|(?:\d+(?:-\d+)?)(?:,\d+(?:-\d+)?)*)';

while (<>) {
  $curblock.=$_;
  if (@fields=(/^\#?($tf)\s+($tf)\s+($tf)\s+($tf)\s+($tf)\s+(.*)/)) {
    push @db, [[@fields], $curblock];
    $curblock="";
  }
}

foreach (sort compare_crons @db) {
  print "$_->[1]";
  warn "-----------\n" . join(" | ", @{$_->[0]})."\n";
}

# compare by month, day, hour and minute. Ignore weekday
sub compare_crons {
  my @fa=@{$a->[0]};
  my @fb=@{$b->[0]};

  return compare_tf($fa[3],$fb[3]) ||
         compare_tf($fa[2],$fb[2]) ||
	 compare_tf($fa[1],$fb[1]) ||
	 compare_tf($fa[0],$fb[0]);
}

# Compare two cron fields. Asterisk considered as zero, otherwise
# compare by the first number
sub compare_tf {
  my ($na,$nb);
  $na=($_[0]=~/^(\d*)/)[0]||0;
  $nb=($_[1]=~/^(\d*)/)[0]||0;
  return ($na <=> $nb);
}
