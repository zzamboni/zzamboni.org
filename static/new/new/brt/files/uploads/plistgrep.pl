#!/usr/bin/perl
# Usage: plistgrep regex file.plist [...]

use strict;

my $regex=qr($ARGV[0]);

shift @ARGV;

foreach my $i (@ARGV) {
  plistgrep($regex, $i);
}

sub plistgrep {
  my $r=shift;
  my $file=shift;
  my @text=plistread($file);
  print map { "$file: $_" } grep(/$r/, @text);
}

sub plistread {
  my $file=shift;
  my $type=`/usr/bin/file "$file"`;
  my @result;
  if ($type =~ /Apple binary property list/) {
    open F, "plutil -convert xml1 -o - '$file' |"
      or die "Error running plutil command: $!\n";
  }
  else {
    open F, "<$file"
      or die "Error opening file $file: $!\n";
  }
  @result=<F>;
  close F;
  return @result;
}
